from gpiozero import AngularServo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
from keyboard import is_pressed

factory = PiGPIOFactory(host='localhost', port=8888)
# Configuración del pin GPIO donde se conectará el ESC
ESC_PIN = 18

# Inicializar el servo con el rango de pulsos adecuado
servo360 = AngularServo(ESC_PIN, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)

# Inicializar el ángulo actual
current_angle = 0
servo360.angle = current_angle

print("Usa las flechas del teclado para mover el servo.")
print("Flecha arriba: +90 grados, Flecha abajo: -90 grados. Pulsa 'q' para salir.")

try:
    while True:
        if is_pressed('up'):
            current_angle += 90
            if current_angle > 90:  # Asegurar que no exceda el rango
                current_angle = 90
            servo360.angle = current_angle
            print(f"Ángulo actual: {current_angle}")
            sleep(0.5)  # Evitar múltiples detecciones rápidas

        if is_pressed('down'):
            current_angle -= 90
            if current_angle < -90:  # Asegurar que no exceda el rango
                current_angle = -90
            servo360.angle = current_angle
            print(f"Ángulo actual: {current_angle}")
            sleep(0.5)

        if is_pressed('q'):  # Salir con la tecla 'q'
            print("Saliendo del control del servo.")
            break

except KeyboardInterrupt:
    print("Interrupción manual. Saliendo...")

finally:
    servo360.angle = None  # Desactivar el servo
