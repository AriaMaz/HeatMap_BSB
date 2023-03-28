#Using the SCD30 NDIR CO2, temperature, and humidity sensor to output a carbon dioxide value at some x and y position given by the RPLidar A1M8 LiDAR sensor

#Input the following into the terminal to install and update the necessary libraries/installations (Works for Python 3.7.3 on macOS 10.15.7)
#pip3 install --upgrade pip
#/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
#sudo apt-get install pigpio
#pip3 install pigpio
#pip3 install scd30_i2c
#pip3 install rplidar
#pip3 install rplidar-roboticia
#pip3 install sensirion-i2c-scd

# Import necessary libraries
import math
import time
import board
import busio
import pigpio
from rplidar import RPLidar
from sensirion_i2c_scd.scd30 import SCD30I2cDevice

# Function to get x and y position from LiDAR sensor
def get_lidar_xy(lidar, max_distance=2000):
    # Iterate through LiDAR measurements
    for measurements in lidar.iter_measurments():
        # Extract angle and distance from measurements
        angle = math.radians(measurements[2])
        distance = measurements[3]

        # Check if the distance is within the specified range
        if distance < max_distance:
            # Convert polar coordinates to Cartesian coordinates
            x = distance * math.cos(angle)
            y = distance * math.sin(angle)
            return x, y
    return None, None

# Main function to read CO2, temperature, and humidity values and print them with x and y positions
def main(lidar, sensor):
    # Start periodic measurement on the SCD30 sensor
    sensor.start_periodic_measurement()
    time.sleep(2)

    # Main loop
    while True:
        # Get x and y positions from LiDAR sensor
        x_position, y_position = get_lidar_xy(lidar)
        if x_position is not None and y_position is not None:
            # Check if data is ready from the SCD30 sensor
            if sensor.get_data_ready():
                # Read CO2, temperature, and humidity values
                co2, temp, humidity = sensor.read_measurement()
                if co2 is not None:
                    # Print x, y, and CO2 values
                    print("X: {:.2f}, Y: {:.2f}, CO2: {:.2f} ppm".format(x_position, y_position, co2))
                time.sleep(2)
            else:
                time.sleep(0.2)
        else:
            print("No valid LiDAR measurement found.")
            time.sleep(1)

# Entry point for the script
if __name__ == "__main__":
    # Initialize I2C bus for SCD30 sensor
    i2c = busio.I2C(board.SCL, board.SDA)
    # Create SCD30 sensor object
    sensor = SCD30I2cDevice(i2c)
    # Create RPLidar object
    lidar = RPLidar('/dev/ttyUSB0') # Replace with the correct port for LiDAR sensor

    #Can use the following command to list available serial ports on your Raspberry Pi:
    #ls /dev/tty*
    #Look for a port similar to /dev/ttyUSB0 or /dev/ttyACM0

    # Run the main function
    try:
        main(lidar, sensor)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        # Clean LiDAR resources
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
