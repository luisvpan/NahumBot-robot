from gpiozero import AngularServo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

# Configuración de la fábrica PiGPIO para el control remoto del GPIO
factory = PiGPIOFactory(host='localhost', port=8888)  # Aquí se corrigió el apóstrofo extra

# Configuración del pin GPIO donde se conectará el ESC
ESC_PIN = 13

# Inicializar el servo con el rango de pulsos adecuado
servo360 = AngularServo(ESC_PIN, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)

# Inicializar el ángulo actual
current_angle = 0
servo360.angle = current_angle

print("Controla el servo ingresando comandos:")
print("'w': +90 grados, 's': -90 grados, 'q': salir.")

try:
    while True:
        command = input("Ingresa un comando: ").lower()

        if command == 'w':  # Aumentar ángulo
            current_angle += 10
            if current_angle > 90:  # Limitar al máximo de 90 grados
                current_angle = 90
            servo360.angle = current_angle
            print(f"Ángulo actual: {current_angle}")
            sleep(0.5)

        elif command == 's':  # Disminuir ángulo
            current_angle -= 10
            if current_angle < -90:  # Limitar al mínimo de -90 grados
                current_angle = -90
            servo360.angle = current_angle
            print(f"Ángulo actual: {current_angle}")
            sleep(0.5)

        elif command == 'q':  # Salir del bucle
            print("Saliendo del control del servo.")
            break

        else:
            print("Comando no válido. Usa 'w', 's' o 'q'.")

except KeyboardInterrupt:
    print("Interrupción manual. Saliendo...")

finally:
    servo360.angle = None  # Desactivar el servo
