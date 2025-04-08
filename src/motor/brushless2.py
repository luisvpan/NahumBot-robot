import RPi.GPIO as GPIO
from time import sleep

# Configuración de los pines GPIO para los ESCs
ESC_PIN_1 = 18  # Motor 1
ESC_PIN_2 = 13  # Motor 2

# Configuración del GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ESC_PIN_1, GPIO.OUT)
GPIO.setup(ESC_PIN_2, GPIO.OUT)

# Configuración de PWM para ambos motores
servo_pwm_1 = GPIO.PWM(ESC_PIN_1, 50)  # Frecuencia de 50 Hz
servo_pwm_2 = GPIO.PWM(ESC_PIN_2, 50)
servo_pwm_1.start(0)  # Inicializar motor 1
servo_pwm_2.start(0)  # Inicializar motor 2

# Función para establecer el ángulo de un motor
def set_angle(servo_pwm, angle):
    duty_cycle = (0.5 + (angle + 90) / 180 * 2) / 20 * 100  # Calcular ciclo de trabajo
    servo_pwm.ChangeDutyCycle(duty_cycle)

# Inicializar ángulos actuales para ambos motores
current_angle_1 = 0
current_angle_2 = 0
set_angle(servo_pwm_1, current_angle_1)
set_angle(servo_pwm_2, current_angle_2)

print("Usa las teclas para mover los motores:")
print("W/S: Motor 1 (+/- 10 grados), I/K: Motor 2 (+/- 10 grados). Pulsa 'q' para salir.")

try:
    while True:
        key = input("Introduce una tecla: ").lower()  # Capturar entrada del teclado
        print(key)
        if key == 'w':
            current_angle_1 += 10
            if current_angle_1 > 90:  # Limitar rango
                current_angle_1 = 90
            set_angle(servo_pwm_1, current_angle_1)
            print(f"Motor 1, ángulo actual: {current_angle_1}")

        elif key == 's':
            current_angle_1 -= 10
            if current_angle_1 < -90:  # Limitar rango
                current_angle_1 = -90
            set_angle(servo_pwm_1, current_angle_1)
            print(f"Motor 1, ángulo actual: {current_angle_1}")

        elif key == 'i':
            current_angle_2 += 10
            if current_angle_2 > 90:  # Limitar rango
                current_angle_2 = 90
            set_angle(servo_pwm_2, current_angle_2)
            print(f"Motor 2, ángulo actual: {current_angle_2}")

        elif key == 'k':
            current_angle_2 -= 10
            if current_angle_2 < -90:  # Limitar rango
                current_angle_2 = -90
            set_angle(servo_pwm_2, current_angle_2)
            print(f"Motor 2, ángulo actual: {current_angle_2}")

        elif key == 'q':  # Salir
            print("Saliendo del control de los motores.")
            break

        else:
            print("Tecla inválida. Usa W, S, I, K o 'q'.")

except KeyboardInterrupt:
    print("Interrupción manual. Saliendo...")

finally:
    set_angle(servo_pwm_1, 0)  # Desactivar motor 1
    set_angle(servo_pwm_2, 0)  # Desactivar motor 2
    servo_pwm_1.stop()
    servo_pwm_2.stop()
    GPIO.cleanup()
