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
print("'w': +10° ambos motores, 's': -10° ambos motores, 'q': salir.")

try:
    while True:
        command = input("Ingresa un comando: ").lower()

        if command == 'w':  # Aumentar ángulo de ambos motores
            current_angle += 5
            if current_angle > 90:
                current_angle = 90
            servo1.angle = current_angle
            servo2.angle = current_angle
            print(f"Ángulo actual ambos motores: {current_angle}")
            sleep(0.5)

        elif command == 's':  # Disminuir ángulo de ambos motores
            current_angle -= 5
            if current_angle < -90:
                current_angle = -90
            servo1.angle = current_angle
            servo2.angle = current_angle
            print(f"Ángulo actual ambos motores: {current_angle}")
            sleep(0.5)

        elif command == 'q':  # Salir del bucle
            print("Saliendo del control de los servos.")
            break

        else:
            print("Comando no válido. Usa 'w', 's' o 'q'.")

except KeyboardInterrupt:
    print("Interrupción manual. Saliendo...")

finally:
    servo1.angle = None  # Desactivar el motor 1
    servo2.angle = None  # Desactivar el motor 2
