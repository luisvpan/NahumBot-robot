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
print("'w': +10° ambos motores, 's': -10° ambos motores, 'a': izquierda, 'd': derecha, 'stop': detener, 'q': salir.")

try:
    while True:
        command = input("Ingresa un comando: ").lower()

        if command == 'forward':  # Aumentar ángulo de ambos motores
            current_angle = 50
            servo1.angle = current_angle
            servo2.angle = current_angle
            print(f"Ángulo actual ambos motores: {current_angle}")
            sleep(0.5)

        elif command == 'backward':  # Disminuir ángulo de ambos motores
            current_angle = -50        
            servo1.angle = current_angle
            servo2.angle = current_angle
            print(f"Ángulo actual ambos motores: {current_angle}")
            sleep(0.5)

        elif command == 'stop':  # Detener ambos motores
            current_angle = 0
            servo1.angle = current_angle
            servo2.angle = current_angle
            print(f"Ángulo actual ambos motores: {current_angle}")
            sleep(0.5)

        elif command == 'left':  # Mover a la izquierda
            current_angle = -30  # Ajusta el ángulo según necesidad
            servo1.angle = current_angle
            servo2.angle = -current_angle  # Dirección opuesta
            print("Moviendo a la izquierda")
            sleep(0.5)

        elif command == 'right':  # Mover a la derecha
            current_angle = 30  # Ajusta el ángulo según necesidad
            servo1.angle = current_angle
            servo2.angle = -current_angle  # Dirección opuesta
            print("Moviendo a la derecha")
            sleep(0.5)

        elif command == 'q':  # Salir del bucle
            print("Saliendo del control de los servos.")
            break

        else:
            print("Comando no válido. Usa 'w', 's', 'a', 'd', 'stop' o 'q'.")

except KeyboardInterrupt:
    print("Interrupción manual. Saliendo...")

finally:
    servo1.angle = None  # Desactivar el motor 1
    servo2.angle = None  # Desactivar el motor 2
