import serial
import json

def read_gps_from_serial(port="/dev/ttyACM0", baudrate=115200):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        last_known_location = {
            'lat': 0.0,
            'lng': 0.0,
            'orientation': 0.0,
            'speed': 0.0
        }
        print("Entro en read GPS from Serial")
        while True:
            line = ser.readline().decode('ascii', errors='replace').strip()
            if not line:
                continue

            # El Arduino envía JSON en texto plano, por ejemplo:
            # {"lat":20.123456,"lng":-100.123456,"orientation":90.00,"speed":5.00}
            try:
                msg = json.loads(line)

                # Obtener datos con fallback a valores previos
                location = {
                    'lat': msg.get('lat', last_known_location['lat']),
                    'lng': msg.get('lng', last_known_location['lng']),
                    'orientation': msg.get('orientation', last_known_location['orientation']),
                    'speed': msg.get('speed', last_known_location['speed'])
                }

                # Actualizar ubicación conocida
                last_known_location = location

                # Aquí retornas la info o la procesas según necesitas
                print(location)  # Por ahora solo lo imprime en consola

            except json.JSONDecodeError:
                # Si la línea no es JSON válido, la ignoramos
                continue

    except serial.SerialException as e:
        print(f"No se pudo abrir el puerto serial: {e}")
