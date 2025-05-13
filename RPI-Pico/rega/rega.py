###############################################################################################
# Rega na varanda by Mario Vaz
###############################################################################################
import network
import socket
import time
import struct
from machine import Pin

###############################################################################################
# SETTINGS
###############################################################################################
# Configurações de rede
ssid = 'ZON-C050'
password = 'f80bccf0bd2a'

# Configuração de IP estático
static_ip = "192.168.1.240"
subnet_mask = "255.255.255.0"
gateway = "192.168.1.1"
dns_server = "8.8.8.8"  # Servidor DNS (ex.: Google DNS)

# Lista de horários programados no formato (hora, minuto)
scheduled_times = [
    (8, 15),    # Exemplo: 08:15
    (11, 45),   # Exemplo: 11:45
    (14, 15),   # Exemplo: 14:15
    (17, 30),   # Exemplo: 17:30
    (18, 45),   # Exemplo: 18:45
    (19, 15),   # Exemplo: 19:15
    (20, 30)    # Exemplo: 20:30
]

duration = 15                # Duração em segundos para ativar a bomba

# Configuração do LED
led = Pin("LED", Pin.OUT)
pump_pin = Pin(16, Pin.OUT)  # Pino para ativar a bomba
###############################################################################################
# END SETTINGS
###############################################################################################

###############################################################################################
# Função para piscar o LED
def blink_led(times=3, delay=0.5):
    """
    Faz o LED piscar um número específico de vezes.
    :param times: Número de vezes que o LED deve piscar.
    :param delay: Intervalo entre cada piscada (em segundos).
    """
    for _ in range(times):
        led.on()      # Liga o LED
        time.sleep(delay)  # Aguarda
        led.off()     # Desliga o LED
        time.sleep(delay)  # Aguarda
###############################################################################################
# END LED BLINK FUNCTION
###############################################################################################

###############################################################################################
# WLAN AND NTP CODE
###############################################################################################
# Ajuste de fuso horário (UTC+1 para Portugal Continental)
TIMEZONE_OFFSET = 1  # Altere este valor conforme necessário (ex.: UTC+2 para Horário de Verão)

# Configurações do NTP
NTP_DELTA = 2208988800  # Diferença entre NTP epoch (1900) e Unix epoch (1970)
host = "185.228.163.139"  # Endereço IP direto do servidor NTP "0.pt.pool.ntp.org"

# Função para conectar à rede Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Configurar IP estático
    wlan.ifconfig((static_ip, subnet_mask, gateway, dns_server))
    
    if not wlan.isconnected():
        print("Conectando à rede Wi-Fi...")
        wlan.connect(ssid, password)
        
        max_wait = 20
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print('Aguardando conexão...')
            time.sleep(1)
        
        if not wlan.isconnected():
            raise RuntimeError("Falha na conexão Wi-Fi")
    
    print("Conectado à rede!")
    status = wlan.ifconfig()
    print(f"IP estático configurado: {status[0]}")

# Função para configurar o horário usando NTP
def set_time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(5)  # Timeout de 5 segundos
        print("Conectando ao servidor NTP...")
        s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
        print("Resposta recebida do servidor NTP.")
    except OSError as e:
        print(f"Falha na conexão com o servidor NTP: {e}")
        return False  # Indica falha
    finally:
        s.close()

    # Processa a resposta do servidor NTP
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA

    # Converte para tempo local ajustando o fuso horário
    local_time = time.gmtime(t + TIMEZONE_OFFSET * 3600)

    # Exibe a hora recebida do servidor NTP ajustada para o fuso horário local
    print(f"Hora recebida do NTP (UTC): {time.gmtime(t)}")
    print(f"Hora ajustada para o fuso horário local: {local_time}")

    # Define o RTC interno com a hora ajustada
    machine.RTC().datetime((
        local_time[0], 
        local_time[1], 
        local_time[2], 
        local_time[6] + 1, 
        local_time[3], 
        local_time[4], 
        local_time[5], 
        0
    ))
    return True  # Indica sucesso

# Programa principal
try:
    # Passo 1: Pisca o LED para indicar o início do programa
    blink_led(times=5, delay=0.2)  # Pisca 5 vezes rapidamente

    # Passo 2: Conectar ao Wi-Fi
    connect_wifi()

    # Passo 3: Sincronizar o horário usando NTP
    if set_time():
        led.on()  # Acende o LED para indicar sucesso
        print("Horário sincronizado com sucesso!")
        time.sleep(10)
    else:
        led.off()  # Apaga o LED para indicar falha
        print("Falha ao sincronizar o horário.")

except Exception as e:
    print(f"Erro geral: {e}")
    led.off()  # Apaga o LED em caso de erro

# Obtém a data e hora atual após a sincronização
t = time.localtime()
print(f"Data e hora atuais: {t[0]}-{t[1]:02d}-{t[2]:02d} {t[3]:02d}:{t[4]:02d}:{t[5]:02d}")
led.off()  # Apaga o LED para indicar estado da bomba
###############################################################################################
# END WLAN AND NTP CODE
###############################################################################################

###############################################################################################
# PUMP FUNCTION
###############################################################################################
def pump():    
    led.on()              # LIGA O LED
    pump_pin.value(0)     # Liga a bomba (inverte o valor para ligar)
    time.sleep(duration)  # Mantém a bomba ligada durante a duração
    pump_pin.value(1)     # Desliga a bomba (inverte o valor para desligar)
    led.off()             # DESLIGA O LED
###############################################################################################
# END PUMP FUNCTION
###############################################################################################

###############################################################################################
# TIME CHECK
###############################################################################################
while True:
    t = time.localtime()
    current_hour = t[3]      # Hora atual
    current_minute = t[4]    # Minuto atual
    current_second = t[5]    # Segundo atual

    # Formata a hora, minutos e segundos com dois dígitos
    formatted_time = f"{t[0]}-{t[1]:02d}-{t[2]:02d} {t[3]:02d}:{t[4]:02d}:{t[5]:02d}"

    # Verifica se o horário atual corresponde a algum dos horários programados
    for scheduled_hour, scheduled_minute in scheduled_times:
        if current_hour == scheduled_hour and current_minute == scheduled_minute and current_second == 0:
            print(f"Ativou a bomba   às {formatted_time}")
            pump()

    # Garante que a bomba esteja desligada fora dos horários programados
    pump_pin.value(1)  # Desliga a bomba (inverte o valor para desligar)
    print(f"Bomba desativada às {formatted_time}")

    # Aguarda 1 segundo antes de verificar novamente
    time.sleep(1)
###############################################################################################
# END TIME CHECK
###############################################################################################

###############################################################################################
# Rega na varanda by Mario Vaz - 2025-05-05
###############################################################################################
