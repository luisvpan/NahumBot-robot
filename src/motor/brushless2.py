import RPi.GPIO as GPIO
from time import sleep

# Configuración del pin GPIO donde se conectará el ESC
ESC_PIN = 18

# Configuración del GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ESC_PIN, GPIO.OUT)
servo_pwm = GPIO.PWM(ESC_PIN, 50)  # Frecuencia de 50 Hz para el servo
servo_pwm.start(0)  # Inicializar el servo en posición neutral

# Función para establecer el ángulo del servo
def set_angle(angle):
    duty_cycle = (0.5 + (angle + 90) / 180 * 2) / 20 * 100  # Calcular ciclo de trabajo basado en el rango de pulsos
    servo_pwm.ChangeDutyCycle(duty_cycle)

# Inicializar ángulo actual
current_angle = 0
set_angle(current_angle)

print("Usa las teclas WASD para mover el servo:")
print("W: +10 grados, S: -10 grados, A: -45 grados, D: +45 grados. Pulsa 'q' para salir.")

try:
    while True:
        key = input("Introduce una tecla: ").lower()  # Capturar entrada del teclado
        print(key)
        if key == 'w':
            current_angle += 10
            if current_angle > 90:  # Limitar el rango
                current_angle = 90
            set_angle(current_angle)
            print(f"Ángulo actual: {current_angle}")

        elif key == 's':
            current_angle -= 10
            if current_angle < -90:  # Limitar el rango
                current_angle = -90
            set_angle(current_angle)
            print(f"Ángulo actual: {current_angle}")

        elif key == 'a':
            current_angle -= 45
            if current_angle < -90:
                current_angle = -90
            set_angle(current_angle)
            print(f"Ángulo actual: {current_angle}")

        elif key == 'd':
            current_angle += 45
            if current_angle > 90:
                current_angle = 90
            set_angle(current_angle)
            print(f"Ángulo actual: {current_angle}")

        elif key == 'q':  # Salir del programa
            print("Saliendo del control del servo.")
            break

        else:
            print("Tecla inválida. Usa W, A, S, D o 'q'.")

except KeyboardInterrupt:
    print("Interrupción manual. Saliendo...")

finally:
    set_angle(0)  # Desactivar el servo
    servo_pwm.stop()
    GPIO.cleanup()
