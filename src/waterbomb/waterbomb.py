from gpiozero import DigitalOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
import sys
import threading

# Configuración de la fábrica PiGPIO para el control remoto del GPIO
factory = PiGPIOFactory(host='localhost', port=8888)

# Configuración de los pines GPIO donde se conectarán los motores
ESC_PIN1 = 23  # Bomba de llenado
ESC_PIN2 = 24  # Bomba de vaciado

# Inicialización de pines como dispositivos de salida con la fábrica remota
pump_fill = DigitalOutputDevice(ESC_PIN1, pin_factory=factory)
pump_empty = DigitalOutputDevice(ESC_PIN2, pin_factory=factory)

def bomb_mode_none():
    """
    Modo NONE: Apaga ambas bombas.
    """
    pump_fill.on()   # Set pin 23 HIGH
    pump_empty.on()  # Set pin 24 HIGH
    print("Bomb mode set to NONE: both pumps OFF")

def bomb_mode_empty():
    """
    Modo EMPTY: Activa la bomba de vaciado y apaga la de llenado.
    """
    pump_fill.on()   # Set pin 23 HIGH
    pump_empty.off()   # Set pin 24 LOW
    print("Bomb mode set to EMPTY: empty pump ON, fill pump OFF")

def bomb_mode_fill():
    """
    Modo FILL: Activa la bomba de llenado y apaga la de vaciado.
    """
    pump_fill.off()    # Set pin 23 LOW
    pump_empty.on()  # Set pin 24 HIGH
    print("Bomb mode set to FILL: fill pump ON, empty pump OFF")

def print_usage():
    print("Uso: python bomb_control_terminal.py [none|empty|fill]")
    print("  none  -> Apaga ambas bombas")
    print("  empty -> Enciende la bomba de vaciado")
    print("  fill  -> Enciende la bomba de llenado")

def command_listener():
    """
    Escucha los comandos del usuario en un hilo separado.
    """
    while True:
        command = input("Ingrese comando (none|empty|fill): ").lower()
        if command == "none":
            bomb_mode_none()
        elif command == "empty":
            bomb_mode_empty()
        elif command == "fill":
            bomb_mode_fill()
        else:
            print(f"Comando desconocido: {command}")
            print_usage()

if __name__ == "__main__":
    # Iniciar el hilo para escuchar comandos
    listener_thread = threading.Thread(target=command_listener)
    listener_thread.daemon = True  # Permitir que el hilo se cierre al finalizar el programa
    listener_thread.start()

    # Mantener el programa en ejecución
    try:
        while True:
            pass  # El programa principal puede hacer otras tareas aquí
    except KeyboardInterrupt:
        print("Programa terminado.")
        sys.exit(0)
