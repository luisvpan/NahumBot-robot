import io

import serial 
import time
import string
import pynmea2
from constants import is_simulation_mode
import random
from gps.new_gps import get_orientation


last_known_location={
	'lat': 8.35122,
	'lng': -62.64102,
	'orientation': 0,
	'speed': 0
}

def generate_simulated_gps_update():
    # Variación controlada
    latitude_variance = (random.random() - 0.5) * 0.0005  # Variación controlada para latitud
    longitude_variance = (random.random() - 0.5) * 0.0005  # Variación controlada para longitud
    orientation_variance = (random.random() - 0.5) * 5  # Variación controlada para orientación
    speed_variance = (random.random() - 0.5) * 0.1  # Variación controlada para velocidad

    # Actualiza las coordenadas y la velocidad con una variación suave
    last_known_location['lat'] += latitude_variance
    last_known_location['lng'] += longitude_variance
    last_known_location['orientation'] += orientation_variance
    last_known_location['speed'] += speed_variance

    # Asegúrate de que los valores sean razonables
    last_known_location['speed'] = max(0, last_known_location['speed'])
    last_known_location['orientation'] = (last_known_location['orientation'] + 360) % 360  # Mantén la orientación entre 0 y 360

    return last_known_location

def get_gps_location():
	if (is_simulation_mode):
		return generate_simulated_gps_update()

	port="/dev/ttyACM0"
	ser=serial.Serial(port, baudrate=9600, timeout=0.5)
	sio= io.TextIOWrapper(io.BufferedRWPair(ser, ser))

	try:
		line=sio.readline()
		msg=pynmea2.parse(line)
		global last_known_location

		orientation = get_orientation()
		print("Orientation: ", orientation)
		if msg.sentence_type == 'RMC':
			print('Mensaje: ' + msg)
		dic={
			'lat': msg.latitude,
			'lng': msg.longitude,
			'orientation': orientation if orientation else last_known_location['orientation'],
			'speed': msg.spd_over_grnd if msg.sentence_type == 'RMC' else last_known_location['speed']
		}
		print(dic)
		last_known_location=dic
		return dic
	except serial.SerialException as e:
		print("Device error: {}".format(e))
	except pynmea2.ParseError as e:
		print("Parse error: {}".format(e))
	except Exception as e:
		print("Unknown error: {}".format(e))

	return last_known_location
