# HeatMap For BSB

Using the SCD30 NDIR CO2, temperature, and humidity sensor to output a carbon dioxide value at some x and y position given by the RPLidar A1M8 LiDAR sensor <br>

Input the following into the terminal to install and update the necessary libraries/installations (Works for Python 3.7.3 on macOS 10.15.7) <br>
pip3 install --upgrade pip <br>
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" <br>
sudo apt-get install pigpio <br>
pip3 install pigpio <br>
pip3 install scd30_i2c <br>
pip3 install rplidar <br>
pip3 install rplidar-roboticia <br>
pip3 install sensirion-i2c-scd <br>
