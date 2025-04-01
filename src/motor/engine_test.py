from time import sleep
from constants import is_simulation_mode

#import keyboard
# TODO: Dividir en funciones para avanzar,
# retroceder, girar y detenerse
# TODO: Regular velocidad
# TODO: Funcion de hacer trompito
# TODO: Escuchar desde las peticiones de un socket
# con los movimientos que ejecutaran las funciones
# Puede ser via memoria compartida, sockets etc [Sockets de preferencia]
# Include the motor control pins
# Motor A LADO DERECHO


ENA = 17
IN1 = 27
IN2 = 22
# Motor B LADO IZQUIERDO
ENB = 11
IN3 = 10
IN4 = 9

if (is_simulation_mode == False):
    import RPi.GPIO as GPIO
    # Set up GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)  # Disable warnings
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(ENB, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    # Configuración del PWM para cada motor
    pwm_A = GPIO.PWM(ENA, 100)  # Frecuencia de 100 Hz para el motor A
    pwm_B = GPIO.PWM(ENB, 100)  # Frecuencia de 100 Hz para el motor B
    pwm_A.start(0)  # Iniciar el PWM del motor A con velocidad 0%
    pwm_B.start(0)  # Iniciar el PWM del motor B con velocidad 0%
else:
    class MockPWM:
        def __init__(self, pin, frequency):
            self.pin = pin
            self.frequency = frequency

        def start(self, duty_cycle):
            pass

        def ChangeDutyCycle(self, duty_cycle):
            pass

    class MockGPIO:
        BCM = None
        HIGH = True
        LOW = False

        @staticmethod
        def setmode(mode):
            pass

        @staticmethod
        def setwarnings(flag):
            pass

        @staticmethod
        def setup(pin, mode):
            pass

        @staticmethod
        def output(pin, state):
            pass

        @staticmethod
        def cleanup():
            pass

    GPIO = MockGPIO()
    pwm_A = MockPWM(ENA, 100)
    pwm_B = MockPWM(ENB, 100)
    print("Modo simulación activado: no se inicializan los pines GPIO.")

def set_speed(motor_pwm, speed):
    """Configurar la velocidad del motor."""
    motor_pwm.ChangeDutyCycle(speed)
def forward(speed_A=100, speed_B=100):
    """Set motors to move forward."""
    print('motors move forward')
    set_speed(pwm_A, speed_A)
    set_speed(pwm_B, speed_B)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
def backward(speed_A=100, speed_B=100):
    """Set motors to move backward."""
    print('motors move backward')
    set_speed(pwm_A, 100)
    set_speed(pwm_B, 100)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
def stop():
    """Stop the motors."""
    print('motors stop')
    set_speed(pwm_A, 0)
    set_speed(pwm_B, 0)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    
def turn_right(speed_A=0, speed_B=100):
    print('motors turn right')
    set_speed(pwm_A, speed_A)
    set_speed(pwm_B, speed_B)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def turn_left(speed_A=100, speed_B=0):
    print('motors turn left')
    set_speed(pwm_A, speed_A)
    set_speed(pwm_B, speed_B)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def turn_right_dog(speed_A=50, speed_B=100):
    print('motors turn right dog')
    set_speed(pwm_A, speed_A)
    set_speed(pwm_B, speed_B)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def turn_left_dog(speed_A=100, speed_B=50):
    print('motors turn left dog')
    set_speed(pwm_A, speed_A)
    set_speed(pwm_B, speed_B)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

print("FIUMMMMMMMMMMMMMMMMMMBA")

'''
try:
    #print("Usa las flechas del teclado para controlar el robot. Presiona 'q' para salir.")
    while True:
        sleep(0.1)  # Pequeña pausa para evitar sobrecargar la CPU
        forward()
except KeyboardInterrupt:
    pass  # Allow exit with Ctrl+C
finally:
    GPIO.cleanup()  # Clean up GPIO settings

'''
