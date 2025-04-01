import smbus2
import time
import math
from constants import is_simulation_mode

# HMC5883L register addresses
ADDRESS = 0x1E
CONFIG_A = 0x00
CONFIG_B = 0x01
MODE = 0x02
STATUS = 0x09
X_MSB = 0x03
Z_MSB = 0x05
Y_MSB = 0x07

def setup():
    bus.write_byte_data(ADDRESS, CONFIG_A, 0x70, True)  # Set to 8 samples @ 15Hz
    bus.write_byte_data(ADDRESS, CONFIG_B, 0x20, True)  # 1.3 gain LSb / Gauss 1090 (default)
    bus.write_byte_data(ADDRESS, MODE, 0x01, True)  # Single measurement mode

def measure():
    bus.write_byte_data(ADDRESS, MODE, 0x01, True)  # Single measurement mode

    # Wait for the measurement to be ready
    while bus.read_byte_data(ADDRESS, STATUS) & 0x01 == 0:
        time.sleep(0.01)

    bus.write_byte_data(ADDRESS, MODE, 0x02, True)  # Still mode forced

    # Read the data
    x = read_raw_data(X_MSB)
    z = read_raw_data(Z_MSB)
    y = read_raw_data(Y_MSB)

    return x, y, z

def read_raw_data(addr):
    # Read raw 16-bit value
    high = bus.read_byte_data(ADDRESS, addr)
    low = bus.read_byte_data(ADDRESS, addr + 1)
    
    # Combine them to get a 16-bit value
    value = (high << 8) + low
    if value > 32768:  # Adjust for 2's complement
        value = value - 65536
    return value

def compute_heading(x, y):
    # Calculate heading in radians
    heading_rad = math.atan2(y, x)
    
    # Adjust for declination angle (e.g. 0.22 for ~13 degrees)
    declination_angle = 0.22
    heading_rad += declination_angle
    
    # Correct for when signs are reversed.
    if heading_rad < 0:
        heading_rad += 2 * math.pi

    # Check for wrap due to addition of declination.
    if heading_rad > 2 * math.pi:
        heading_rad -= 2 * math.pi

    # Convert radians to degrees for readability.
    heading_deg = heading_rad * (180.0 / math.pi)
    
    return heading_deg

def get_orientation():
    if (is_simulation_mode):
        return 0
    
    x, y, _ = measure()
    
    heading = compute_heading(x, y)
    
    print(f"Heading: {heading:.2f}°")

    return heading


if (is_simulation_mode == False):
    bus = smbus2.SMBus(1)
    setup()