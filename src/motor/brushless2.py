from gpiozero import AngularServo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory(host='localhost', port=8888)
# Configuración del pin GPIO donde se conectará el ESC
ESC_PIN = 18


servo360 = AngularServo(ESC_PIN, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000,        pin_factory=factory)

for i in range(-90, 90):
    print(i)
    servo360.angle = i
    sleep(1)
servo360.angle = 42