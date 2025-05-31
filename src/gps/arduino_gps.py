import serial
import json
import pynmea2

def read_gps_from_serial(port="/dev/ttyACM0", baudrate=115200):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        last_known_location = {
            'lat': 0.0,
            'lng': 0.0,
            'orientation': 0.0,
            'speed': 0.0
        }

        while True:
            try:
                line = ser.readline().decode('ascii', errors='replace').strip()
                if line.startswith("$GP"):  # Captura cualquier sentencia NMEA de GPS
                    try:
                        msg = pynmea2.parse(line)
                        if hasattr(msg, 'latitude') and hasattr(msg, 'longitude'):
                            location = {
                                'lat': msg.latitude,
                                'lng': msg.longitude,
                                'orientation': 0.0,
                                'speed': 0.0  # Velocidad fija en 0
                            }
                            last_known_location = location
                            print(json.dumps(location, indent=4))

                    except pynmea2.ParseError:
                        print("Error al analizar la frase NMEA")

            except Exception as e:
                print(f"Error al leer datos: {e}")

    except serial.SerialException as e:
        print(f"No se pudo abrir el puerto serial: {e}")

    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
        print("Puerto serial cerrado.")

if __name__ == "__main__":
    read_gps_from_serial()
