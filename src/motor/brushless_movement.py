from gpiozero import AngularServo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

# Configuración de la fábrica PiGPIO para el control remoto del GPIO
factory = PiGPIOFactory(host='localhost', port=8888)

# Configuración de los pines GPIO donde se conectarán los motores
ESC_PIN1 = 18  # Primer motor
ESC_PIN2 = 13  # Segundo motor

# Inicializar los servos con el rango de pulsos adecuado
servo1 = AngularServo(ESC_PIN1, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
servo2 = AngularServo(ESC_PIN2, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)

# Inicializar los ángulos actuales
current_angle = 0
servo1.angle = current_angle
servo2.angle = current_angle

print("Controla ambos servos ingresando comandos:")
print("'forward': avanzar, 'backward': retroceder, 'left': girar a la izquierda, 'right': girar a la derecha, 'stop': detener, 'q': salir.")

def forward():
    global current_angle
    current_angle = 50
    servo1.angle = current_angle
    servo2.angle = current_angle
    print(f"Ángulo actual ambos motores: {current_angle}")

def backward():
    global current_angle
    current_angle = -50        
    servo1.angle = current_angle
    servo2.angle = current_angle
    print(f"Ángulo actual ambos motores: {current_angle}")

def stop():
    global current_angle
    print("STOP EN BRUSHLESS MOVEMENT")
    current_angle = 0
    servo1.angle = current_angle
    servo2.angle = current_angle
    print(f"Ángulo actual ambos motores: {current_angle}")

def turn_left():
    servo1.angle = 0
    servo2.angle = 50  # Dirección opuesta
    print("Moviendo a la izquierda")

def turn_right():
    servo1.angle = 50
    servo2.angle = 0  # Dirección opuesta
    print("Moviendo a la derecha")


