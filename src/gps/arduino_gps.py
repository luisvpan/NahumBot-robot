import serial
import json
import pynmea2
import re

def extract_lat_lng(line):
    """Extrae manualmente latitud y longitud si la línea es imperfecta."""
    match = re.search(r"(\d{4}\.\d+),([NS]),(\d{5}\.\d+),([EW])", line)
    if match:
        lat_deg = int(match.group(1)[:2])
        lat_min = float(match.group(1)[2:])
        lat = lat_deg + (lat_min / 60.0)
        if match.group(2) == 'S':
            lat *= -1

        lng_deg = int(match.group(3)[:3])
        lng_min = float(match.group(3)[3:])
        lng = lng_deg + (lng_min / 60.0)
        if match.group(4) == 'W':
            lng *= -1

        return lat, lng
    return None, None

def read_gps_from_serial(port="/dev/ttyACM0", baudrate=115200):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        last_known_location = {
            'lat': 0.0,
            'lng': 0.0,
            'orientation': 0.0,
            'speed': 0.0
        }

        try:
            line = ser.readline().decode('ascii', errors='replace').strip()
            print("Línea recibida:", line)

            try:
                msg = pynmea2.parse(line)
                print("Mensaje NMEA válido:", msg)
                if hasattr(msg, 'latitude') and hasattr(msg, 'longitude'):
                    lat, lng = msg.latitude, msg.longitude
                else:
                    lat, lng = extract_lat_lng(line)  # Intentar extraer manualmente

                if lat is not None and lng is not None:
                    location = {
                        'lat': lat,
                        'lng': lng,
                        'orientation': 0.0,
                        'speed': 0.0  # Velocidad fija en 0
                    }
                    last_known_location = location
                    print(json.dumps(location, indent=4))

            except pynmea2.ParseError:
                print("Error al analizar la frase NMEA, intentando extracción manual...")
                lat, lng = extract_lat_lng(line)
                if lat is not None and lng is not None:
                    location = {
                        'lat': lat,
                        'lng': lng,
                        'orientation': 0.0,
                        'speed': 0.0
                    }
                    last_known_location = location
                    print(json.dumps(location, indent=4))

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
