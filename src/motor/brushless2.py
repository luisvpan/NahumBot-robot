from gpiozero import PWMOutputDevice
from time import sleep

# Configuración del pin GPIO donde se conectará el ESC
ESC_PIN = 18
esc = PWMOutputDevice(ESC_PIN, frequency=50)

def set_esc_speed(speed):
    print(esc)
    # Convertir el rango de velocidad de 0-100% a 0-180 (similar al Arduino)
    duty_cycle = speed / 100  # Escala a un valor entre 0.0 y 1.0
    esc.value = duty_cycle

def read_potentiometer():
    # Aquí deberías leer el valor analógico del potenciómetro
    # Este código es genérico, necesitarás una biblioteca como `gpiozero` y un ADC (convertidor analógico-digital) para leer el potenciómetro.
    pot_value = 1023  # Suponiendo un valor fijo como ejemplo
    return pot_value

try:
    while True:
        pot_value = read_potentiometer()  # Leer el valor del potenciómetro
        scaled_value = (pot_value / 1023) * 100
        print(scaled_value,"%")  # Escalar el valor a un rango de 0-100%
        set_esc_speed(scaled_value)  # Configurar la velocidad del ESC
        sleep(0.1)

except KeyboardInterrupt:
    print("Programa detenido")
    esc.value = 0  # Apagar el ESC