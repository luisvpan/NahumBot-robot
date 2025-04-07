from gpiozero import AngularServo
from time import sleep

# Configuración del pin GPIO donde se conectará el ESC
ESC_PIN = 18
servo = AngularServo(ESC_PIN, min_pulse_width=0.0006, max_pulse_width=0.0023)

try:
    while True:
        servo.angle = 0
        sleep(3)

        servo.angle = 90
        sleep(3)


except KeyboardInterrupt:
    print("Programa detenido")
