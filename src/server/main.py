from typing import Union
import asyncio

from fastapi import FastAPI, WebSocket, HTTPException

from fastapi.testclient import TestClient
from geojson import Point
from pydantic import BaseModel
from gps.arduino_gps import read_gps_from_serial
from camera.main import get_image
from constants import is_simulation_mode, simulated_base64_image
from motor.brushless_movement import backward, forward, turn_left, turn_right, stop
from motor.ball_follower import dogStep
from server.map_mode import calculate_distance, calculate_bearing
import random
import cv2
import json
from arduino.main import ArduinoSensorInterface
from waterbomb.waterbomb import bomb_mode_empty, bomb_mode_fill, bomb_mode_none

app = FastAPI()
camera = cv2.VideoCapture(0)

arduino = ArduinoSensorInterface()


class Command(BaseModel):
    action: str

class WaterBombMode(BaseModel):
    mode: str

class CommandSpeed(BaseModel):
    movement_speed: int

class CommandMode(BaseModel):
    movement_mode: str

class CommandChangeTarget(BaseModel):
    data: str # {longitude,latitude} in JSON

@app.get("/")
def read_root():
    return {"Hello": "World"}

import threading
import time
import math

# Global variable to control the motor state

running = False
motor_thread = None
aux_thread = None
movement_mode = "control" # control, dog, map, path
movement_speed = 100 # esta es la velocidad teorica a la que podemos ajustar el robot desde el frontend
# haz un objeto para las coordenadas target para pasrlo por referencia a un hilo de ejecusion posteriormente
target_coords = {
    "latitude": 0,
    "longitude": 0
}
bomb_mode = "none"  # Estado inicial de las bombas

target_orientation = 0

current_coords = {
    "latitude": 0,
    "longitude": 0
}
aux_running = False # for de bug porpuses
current_orientation = 0

def control_motors(action):
    global running
    running = True

    #print(f"Running state before loop: {running}", flush=True)
    while running:
        #print(f"Starting motor control with action: {action}")
        '''
        if (movement_mode == "dog"):
            print("antes del dog step")
            dogStep()
            print("despues del dog step")
    
        else:
        '''          
        if action == "forward":
            forward()
        elif action == "backward":
            backward()
        elif action == "turn_left":
            turn_left()
        elif action == "turn_right":
            turn_right()
        elif action == "stop":
            stop()
            print("Entro en stop del command")

        else:
            stop_motors()
        time.sleep(0.1)  # Adjust the sleep time as needed

def dog_control(camera):
    global running
    running = True

    print("running dog_control")
  
    while running:
      print("runnign dog_control")  
      aux = dogStep(camera)
      if (aux == False):
        stop_motors()
        break

def other_threat_to_generate_random_points():
    global target_coords
    global current_coords
    global aux_running
    aux_running = True

    while aux_running:
        target_coords = {
            "latitude": random.uniform(-90, 90),
            "longitude": random.uniform(-180, 180)
        }
        current_coords = {
            "latitude": random.uniform(-90, 90),
            "longitude": random.uniform(-180, 180)
        }
        if (aux_running == False):
            break

def move_in_direction_simulation(current_coords, bearing, distance):
    # Convert bearing to radians
    bearing_rad = math.radians(bearing)
    velocity_in_meters = 5  # 5 m/s velocity in simulation mode

    # Calculate new latitude and longitude in meters
    new_latitude = current_coords["latitude"] + (velocity_in_meters * math.cos(bearing_rad) / 111320)  # 1 degree latitude ~ 111320 meters
    new_longitude = current_coords["longitude"] + (velocity_in_meters * math.sin(bearing_rad) / (111320 * math.cos(math.radians(current_coords["latitude"]))))  # Adjust for longitude
    
    return {
        "latitude": new_latitude,
        "longitude": new_longitude
    }

def mapStep(target_coords, _current_coords, current_orientation):
    global movement_speed
    global current_coords

    distance = calculate_distance(current_coords, target_coords)
    bearing = calculate_bearing(current_coords, target_coords)
    #bearing print
    print("Bearing: ", bearing)

    if distance < 5:  # ESTA ES LA DISTANCIA DE ERROR EN METROSSSSs
        return None

    angle_diff = (bearing - current_orientation + 360) % 360
    if angle_diff > 180:
        angle_diff -= 360

    if abs(angle_diff) > 25:  # Threshold angle in degrees
        if angle_diff > 0:
            turn_right(0, movement_speed)
        else:
            turn_left(movement_speed, 0)
    else:
        forward(movement_speed, movement_speed)
        if is_simulation_mode:
            # Move in the direction of the current orientation
            current_coords = move_in_direction_simulation(current_coords, current_orientation, movement_speed)

    if (is_simulation_mode):
        current_orientation = bearing

    time.sleep(6)

    return current_orientation

def map_control():
    global running
    global target_coords
    global current_coords
    global current_orientation
    running = True

    print("running map_control")
  
    while running:
      print("runnign map_control")  
      print("---> target", target_coords)
      print("---> current", current_coords)
      print("---> orientation", current_orientation)
      aux = mapStep(target_coords, current_coords, current_orientation)
      if (aux == None):
        stop_motors()
        break
      else:
        if (is_simulation_mode):
            current_orientation = aux

def stop_motors():
    global running
    running = False
    stop()  # Ensure motors are stopped when exiting

def stop_aux():
    global aux_running
    aux_running = False


def get_current_status():
    global bomb_mode  # Acceder a la variable global bomb_mode
    return {
        "movement_mode": movement_mode,
        "running": running,
        "movement_speed": movement_speed,
        "target_coords": {
            "latitude": target_coords["latitude"],
            "longitude": target_coords["longitude"]
        },
        "bomb_mode": bomb_mode,  # Agregar el estado de las bombas
        "target_orientation": target_orientation
    }

# Example usage in your FastAPI endpoint
@app.get("/current-status")
async def current_status():
    return {
        "status": "success",
        "current_status": get_current_status()
    }

# Change speed endpoint
@app.put("/change-speed")
async def change_speed(command: CommandSpeed):
    print("movement_speed")
    print(command)

    global movement_speed
    movement_speed = command.movement_speed

    return {
            "status": "success",
            "speed": movement_speed,
            "current_status": get_current_status()
        }

# Change movementMode endpoint
@app.put("/change-mode")
async def change_movement_mode(command: CommandMode):
    global camera
    print("movement_mode")
    print(command)
    global motor_thread
    global aux_thread
    global target_coords
    
    # validate its control, dog or map
    if command.movement_mode not in ["control", "dog", "map", "path"]:
        return {
            "status": "error",
            "message": "Invalid movement mode"
        }

    global movement_mode
    movement_mode = command.movement_mode

    # Stop any ongoing motor control before starting a new one
    if motor_thread is not None and motor_thread.is_alive():
        stop_motors()
        motor_thread.join()  # Wait for the thread to finish

    if aux_thread is not None and aux_thread.is_alive():
        stop_aux()
        aux_thread.join()  # Wait for the thread to finish

    if (movement_mode == "dog"):
        # Start a new thread to control the motors
        motor_thread = threading.Thread(target=dog_control, args=(camera,))
        motor_thread.start()

    # map mode
    if (movement_mode == "map"):
        # Start a new thread to control the motors
        # Crea unac oordenad alteatoria para que sea el nuevo target
        #target_coords = {
        #    "latitude": random.uniform(-90, 90),
        #    "longitude": random.uniform(-180, 180)
        #}
        motor_thread = threading.Thread(target=map_control)
        motor_thread.start()
        #aux_thread = threading.Thread(target=other_threat_to_generate_random_points)
        #aux_thread.start()

    return {
            "status": "success",
            "mode": movement_mode,
            "current_status": get_current_status()
        }

@app.put("/change-target")
async def change_target(command: CommandChangeTarget):
    print("change_target")
    print(command)

    global target_coords
    new_target = json.loads(command.data)
    target_coords = {
        "latitude": new_target["latitude"],
        "longitude": new_target["longitude"]
    }

    return {
            "status": "success",
            "target_coords": target_coords,
            "current_status": get_current_status()
        }

# Control bot endpoint
@app.post("/control-robot")
async def control_robot(command: Command):
    print("control_robot")
    print(command)

    global motor_thread
    action = command.action.lower()

    '''
    if (is_simulation_mode):
        return {
            "status": "success",
            "action": action,
            "current_status": get_current_status()
        }
    '''

    # Stop any ongoing motor control before starting a new one
    if motor_thread is not None and motor_thread.is_alive():
        stop_motors()
        motor_thread.join()  # Wait for the thread to finish

    if (movement_mode == "control"):
        # Start a new thread to control the motors
        motor_thread = threading.Thread(target=control_motors, args=(action,))
        motor_thread.start()

    return {
            "status": "success",
            "action": action,
            "current_status": get_current_status()
        }


# Control bot endpoint
@app.post("/control-robot")
async def control_robot(command: Command):
    print("control_robot")
    print(command)

    global motor_thread
    action = command.action.lower()

    '''
    if (is_simulation_mode):
        return {
            "status": "success",
            "action": action,
            "current_status": get_current_status()
        }
    '''

    # Stop any ongoing motor control before starting a new one
    if motor_thread is not None and motor_thread.is_alive():
        stop_motors()
        motor_thread.join()  # Wait for the thread to finish

    if (movement_mode == "control"):
        # Start a new thread to control the motors
        motor_thread = threading.Thread(target=control_motors, args=(action,))
        motor_thread.start()

    return {
            "status": "success",
            "action": action,
            "current_status": get_current_status()
        }

@app.websocket('/current-location')
async def current_location(websocket: WebSocket):
    global current_coords
    global current_orientation
    await websocket.accept()

    while True:
        try:
            gps_location = read_gps_from_serial()        
            try:
                gps_point = Point((gps_location['lng'], gps_location['lat']))
                current_coords = {
                    "latitude": gps_location['lat'],
                    "longitude": gps_location['lng']
                }
                current_orientation = gps_location['orientation']

                await websocket.send_json({
                    "coordinates": gps_point,
                    "orientation": current_orientation,
                    "speed": gps_location['speed'],
                })

            except TypeError:
                # Si gps_location es None, simplemente saltamos la iteración sin enviar mensaje
                print("GPS no devolvió datos válidos, omitiendo esta iteración.")

        except Exception as e:
            print(f"Error inesperado en WebSocket: {e}")

        await asyncio.sleep(1)  # Pequeña pausa antes de repetir el bucle



@app.websocket("/socket-camera")
async def websocket_kamavinga(websocket: WebSocket):
    global camera
    await websocket.accept()
    
    width, height = 640, 500

    try:
        while True:
            image = get_image(camera)
            await websocket.send_text(image)
            await asyncio.sleep(0.05)  # Controla la tasa de envío
    except Exception as e:
        print(f"Error: {e}")                


@app.get("/sensors")
async def get_sensor_data():
    """
    Endpoint para obtener datos de un sensor específico.
    
    Args:
        sensor_type (str): Tipo de sensor ('tds', 'turbidez', 'todos')
        
    Returns:
        dict: Valores del sensor
  
    valid_types = ['tds', 'turbidez', 'todos']
    if sensor_type.lower() not in valid_types:
        raise HTTPException(status_code=400, detail=f"Tipo de sensor no válido. Opciones: {', '.join(valid_types)}")
    """

    try:
        print("hola")
        data = arduino.get_sensor_data('todos')
        print(data)
        if data:
            class SensorData:
                def __init__(self, **kwargs):
                    for key, value in kwargs.items():
                        setattr(self, key, value)
                        
            sensor_data = SensorData(**data)
            
            return {
                "status": "success",
                "data": {
                    "turbidez": sensor_data.turbidez,
                    "tds": sensor_data.tds,
                    "ph": sensor_data.ph,
                    "temperaturaMuestra": sensor_data.temp1,
                    "temperaturaSumergido": sensor_data.temp2,
                    "rayosUV": random.uniform(0, 100),
                    "latitud": random.uniform(-90, 90),
                    "longitud": random.uniform(-180, 180),
                }
            }
        else:
            raise HTTPException(status_code=500, detail="No se pudieron obtener los datos del sensor")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/change-water-bomb-mode")
async def change_water_bomb_mode(mode: WaterBombMode):
    global bomb_mode  # Acceder a la variable global bomb_mode
    try:
        if mode.mode not in ["none", "empty", "fill"]:
            return {
                "status": "error",
                "message": "Modo de bomba no válido. Opciones: none, empty, fill"
            }
        # Cambiar el modo de las bombas
        if mode.mode == "none":
            bomb_mode_none()
        elif mode.mode == "empty":
            bomb_mode_empty()
        elif mode.mode == "fill":
            bomb_mode_fill()
        # Actualizar el estado de las bombas
        bomb_mode = mode.mode
        return {
            "status": "success",
            "mode": bomb_mode,
            "current_status": get_current_status()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))