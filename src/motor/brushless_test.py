import RPi.GPIO as GPIO
import time

# Configuración del pin
ESC_PIN = 12  # Pin GPIO que se usará para el ESC

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ESC_PIN, GPIO.OUT)

# Configuración de PWM
pwm = GPIO.PWM(ESC_PIN, 50)  # 50 Hz
pwm.start(0)  # Iniciar con 0% de ciclo de trabajo

def set_motor_speed(value):
    if value < 90:
        # Mover en una dirección (0 a 90)
        duty_cycle = map(value, 0, 90, 0, 100)  # Mapea a 0-100%
        pwm.ChangeDutyCycle(duty_cycle)
    elif value > 90:
        # Mover en la dirección opuesta (90 a 180)
        duty_cycle = map(value, 90, 180, 0, 100)  # Mapea a 0-100%
        pwm.ChangeDutyCycle(duty_cycle)
    else:
        # Detener el motor (90)
        pwm.ChangeDutyCycle(0)

def map(value, from_low, from_high, to_low, to_high):
    return (value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low

try:
    while True:
        # Aquí puedes reemplazar con la lógica para obtener el valor de entrada
        # Por ejemplo, puedes usar un sensor, un botón, o simplemente un valor fijo para pruebas.
        input_value = float(input("Introduce un valor entre 0 y 180: "))  # Simulación de entrada

        if 0 <= input_value <= 180:
            set_motor_speed(input_value)
        else:
            print("Por favor, introduce un valor entre 0 y 180.")

        time.sleep(0.1)  # Pequeña pausa para evitar sobrecarga

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()  # Detener PWM
    GPIO.cleanup()  # Limpiar la configuración de GPIO