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
current_angle1 = 0
current_angle2 = 0
servo1.angle = current_angle1
servo2.angle = current_angle2

print("Controla los servos ingresando comandos:")
print("'w': +10° motor 1, 's': -10° motor 1")
print("'e': +10° motor 2, 'd': -10° motor 2")
print("'q': salir.")

try:
    while True:
        command = input("Ingresa un comando: ").lower()

        if command == 'w':  # Aumentar ángulo del motor 1
            current_angle1 += 10
            if current_angle1 > 90:
                current_angle1 = 90
            servo1.angle = current_angle1
            print(f"Ángulo actual motor 1: {current_angle1}")
            sleep(0.5)

        elif command == 's':  # Disminuir ángulo del motor 1
            current_angle1 -= 10
            if current_angle1 < -90:
                current_angle1 = -90
            servo1.angle = current_angle1
            print(f"Ángulo actual motor 1: {current_angle1}")
            sleep(0.5)

        elif command == 'e':  # Aumentar ángulo del motor 2
            current_angle2 += 10
            if current_angle2 > 90:
                current_angle2 = 90
            servo2.angle = current_angle2
            print(f"Ángulo actual motor 2: {current_angle2}")
            sleep(0.5)

        elif command == 'd':  # Disminuir ángulo del motor 2
            current_angle2 -= 10
            if current_angle2 < -90:
                current_angle2 = -90
            servo2.angle = current_angle2
            print(f"Ángulo actual motor 2: {current_angle2}")
            sleep(0.5)

        elif command == 'q':  # Salir del bucle
            print("Saliendo del control de los servos.")
            break

        else:
            print("Comando no válido. Usa 'w', 's', 'e', 'd' o 'q'.")

except KeyboardInterrupt:
    print("Interrupción manual. Saliendo...")

finally:
    servo1.angle = None  # Desactivar el motor 1
    servo2.angle = None  # Desactivar el motor 2
