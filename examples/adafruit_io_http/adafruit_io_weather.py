"""
Example of getting weather
from the Adafruit IO Weather Service
NOTE: This example is for Adafruit IO
Plus subscribers only.
"""
import time
import board
import busio
from digitalio import DigitalInOut
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_requests as requests
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError

# Add a secrets.py to your filesystem that has a dictionary called secrets with "ssid" and
# "password" keys with your WiFi credentials. DO NOT share that file or commit it into Git or other
# source control.
# pylint: disable=no-name-in-module,wrong-import-order
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

# If you have an externally connected ESP32:
# esp32_cs = DigitalInOut(board.D9)
# esp32_ready = DigitalInOut(board.D10)
# esp32_reset = DigitalInOut(board.D5)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e:
        print("could not connect to AP, retrying: ", e)
        continue
print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)

socket.set_interface(esp)
requests.set_socket(socket, esp)

# Set your Adafruit IO Username and Key in secrets.py
# (visit io.adafruit.com if you need to create an account,
# or if you need your Adafruit IO key.)
aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]

# Initialize an Adafruit IO HTTP API object
io = IO_HTTP(aio_username, aio_key, requests)

# Weather Location ID
# (to obtain this value, visit
# https://io.adafruit.com/services/weather
# and copy over the location ID)
location_id = 2127

print("Getting forecast from IO...")
# Fetch the specified record with current weather
# and all available forecast information.
forecast = io.receive_weather(location_id)

# Get today's forecast
current_forecast = forecast["current"]
print(
    "It is {0} and {1}*F.".format(
        current_forecast["summary"], current_forecast["temperature"]
    )
)
print("with a humidity of {0}%".format(current_forecast["humidity"] * 100))

# Get tomorrow's forecast
tom_forecast = forecast["forecast_days_1"]
print(
    "\nTomorrow has a low of {0}*F and a high of {1}*F.".format(
        tom_forecast["temperatureLow"], tom_forecast["temperatureHigh"]
    )
)
print("with a humidity of {0}%".format(tom_forecast["humidity"] * 100))
