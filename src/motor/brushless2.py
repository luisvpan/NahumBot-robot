from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# Use the pigpio pin factory
factory = PiGPIOFactory()

# Configuración del pin GPIO donde se conectará el ESC
ESC_PIN = 18
servo = AngularServo(ESC_PIN, min_pulse_width=0.0006, max_pulse_width=0.0023, pin_factory=factory)

try:
    while True:
        servo.angle = 0
        sleep(2)

        servo.angle = 90
        sleep(2)

        servo.angle = 0
        sleep(2)

        servo.angle = -90
        sleep(2)

except KeyboardInterrupt:
    print("Programa detenido")
