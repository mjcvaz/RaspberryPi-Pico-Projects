# 💧 Rega na Varanda - Raspberry Pi Pico W

Projeto desenvolvido por **Mario Vaz**, que utiliza o **Raspberry Pi Pico W** para automatizar a rega de uma varanda de forma inteligente e programada.

---

## 📋 Descrição

Este script conecta-se a uma rede Wi-Fi, sincroniza o relógio interno do microcontrolador com um servidor NTP e ativa automaticamente uma bomba de água em horários pré-definidos. A bomba é acionada por um pino GPIO, e um LED embutido no Pico W fornece feedback visual sobre o estado do sistema.

---

## ⚙️ Funcionalidades

- 📶 Conexão à rede Wi-Fi com IP estático
- ⏰ Sincronização de horário via NTP (com fuso horário configurável)
- 🕒 Agendamento de horários para rega
- 🚿 Acionamento de bomba de água por tempo determinado
- 💡 Feedback visual com LED
- 🧼 Monitoramento contínuo do tempo para execução da rega

---

## 🔌 Requisitos

- Raspberry Pi Pico W
- Bomba de água 5V (ou compatível)
- Fonte de alimentação adequada
- Módulo de relé ou transistor para acionar a bomba
- Acesso a rede Wi-Fi

---

## 🧠 Lógica de Funcionamento

1. Liga e pisca o LED para indicar o início do processo.
2. Conecta-se à rede Wi-Fi com IP estático.
3. Sincroniza a hora com um servidor NTP.
4. Entra num loop infinito onde:
   - Verifica a hora atual.
   - Se for um dos horários programados, ativa a bomba durante `X` segundos.
   - Fora dos horários, garante que a bomba esteja desligada.
   - Regista cada ação no terminal via `print()`.

---

## ⏲️ Horários Programados

```python
scheduled_times = [
    (8, 15),
    (11, 45),
    (14, 15),
    (17, 30),
    (18, 45),
    (19, 15),
    (20, 30)
]
