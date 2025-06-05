import smbus
import math

# Dirección I2C del HMC5883L
HMC5883L_ADDRESS = 0x1E
# Registros del HMC5883L
CONFIG_A = 0x00
CONFIG_B = 0x01
MODE = 0x02
X_MSB = 0x03

def read_orientation():
    bus = smbus.SMBus(1)

    # Configurar el sensor (modo continuo, ganancia, tasa de muestreo)
    bus.write_byte_data(HMC5883L_ADDRESS, CONFIG_A, 0x70)  # 8-average, 15 Hz default, normal measurement
    bus.write_byte_data(HMC5883L_ADDRESS, CONFIG_B, 0xA0)  # Gain = 5
    bus.write_byte_data(HMC5883L_ADDRESS, MODE, 0x00)      # Continuous measurement mode

    # Leer 6 bytes desde el registro X_MSB
    data = bus.read_i2c_block_data(HMC5883L_ADDRESS, X_MSB, 6)

    # Convertir bytes a valores 16-bit con signo
    x = data[0] << 8 | data[1]
    z = data[2] << 8 | data[3]
    y = data[4] << 8 | data[5]

    if x > 32767:
        x -= 65536
    if y > 32767:
        y -= 65536
    if z > 32767:
        z -= 65536

    # Calcular heading en radianes y luego a grados
    heading_rad = math.atan2(y, x)
    heading_deg = math.degrees(heading_rad)
    if heading_deg < 0:
        heading_deg += 360

    return heading_deg