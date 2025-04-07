from machine import Pin
import time
from servo import Servo

# Configuración del pin
ESC_PIN = 18  # Pin GPIO que se usará para el ESC

# Configuración del servo
servo = Servo(Pin(ESC_PIN))

def set_motor_speed(value):
    if value < 90:
        # Mover en una dirección (0 a 90)
        duty_cycle = map(value, 0, 90, 0, 180)  # Mapea a 0-180 para el servo
        servo.angle(duty_cycle)
    elif value > 90:
        # Mover en la dirección opuesta (90 a 180)
        duty_cycle = map(value, 90, 180, 0, 180)  # Mapea a 0-180 para el servo
        servo.angle(duty_cycle)
    else:
        # Detener el motor (90)
        servo.angle(90)

def map(value, from_low, from_high, to_low, to_high):
    return int((value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low)

try:
    while True:
        # Aquí puedes reemplazar con la lógica para obtener el valor de entrada
        input_value = float(input("Introduce un valor entre 0 y 180: "))  # Simulación de entrada

        if 0 <= input_value <= 180:
            set_motor_speed(input_value)
        else:
            print("Por favor, introduce un valor entre 0 y 180.")

        time.sleep(0.1)  # Pequeña pausa para evitar sobrecarga

except KeyboardInterrupt:
    pass

finally:
    servo.angle(90)  # Detener el motor al final