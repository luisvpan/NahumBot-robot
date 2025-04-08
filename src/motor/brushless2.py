from gpiozero import AngularServo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()
# Configuración del pin GPIO donde se conectará el ESC
ESC_PIN = 18
servo = AngularServo(ESC_PIN, min_pulse_width=0.0006, max_pulse_width=0.0023, pin_factory=factory)

for i in range(-90, 90):
    print(i)
    servo.angle = i
    sleep(0.5)
    
servo.angle = 42