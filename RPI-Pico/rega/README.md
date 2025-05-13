# 🌿 Rega na Varanda — Raspberry Pi Pico W

Este é um sistema de **rega automática** controlado por uma **Raspberry Pi Pico W**, que ativa uma bomba de água de 12V nos horários programados. Ideal para quem quer automatizar a rega de vasos ou pequenas hortas em varandas ou jardins.

---

## 📷 Esquema da Solução

![Esquema da solução](Diagram_of_an_automatic_irrigation_system_using_a_.png)

> Diagrama ilustrativo: a Pico W controla um relé ligado à bomba de 12V, alimentada por uma bateria. As ligações seguem o GPIO 16 para controlo do relé.

---

## 🛠 Componentes Utilizados

- Raspberry Pi Pico W  
- Módulo relé 1 canal (compatível com 3.3V)  
- Bomba de água 12V  
- Bateria de 12V (ou fonte de alimentação)  
- Resistores de proteção (opcional)  
- Cabos Dupont e protoboard (ou solda)  
- Conexão Wi-Fi com internet  

---

## ⚙️ Funcionalidades do Script

- Conexão à rede Wi-Fi com IP estático  
- Sincronização horária via NTP  
- Ativação da bomba de água em horários programados  
- LED da Pico W indica estado de atividade  
- Lógica de segurança: bomba desativa-se automaticamente fora dos horários  

---

## 🕒 Horários Programados

Os horários para rega são definidos como pares de hora e minuto no código:

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
