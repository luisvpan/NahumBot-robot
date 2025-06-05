import smbus2 as smbus
import math

def read_orientation():
    bus = smbus.SMBus(1)
    address = 0x1E  # Dirección I2C del HMC5883L

    # Configurar el modo de operación
    bus.write_byte_data(address, 0x02, 0x00)

    # Leer datos del magnetómetro
    data = bus.read_i2c_block_data(address, 0x03, 6)
    x = (data[0] << 8) | data[1]
    z = (data[2] << 8) | data[3]
    y = (data[4] << 8) | data[5]

    # Calcular la orientación en grados
    heading = math.atan2(y, x) * (180 / math.pi)
    if heading < 0:
        heading += 360  # Ajuste para valores negativos

    return heading
