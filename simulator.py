import requests
import random
import time
import uuid

BASE_URL = "http://127.0.0.1:8002/api"
DEVICE_ID = "0bdf1259-cfad-4530-9844-5a8dd20e3c8e"

def generate_reading():
    return {
        "device": DEVICE_ID,
        "battery_level": round(random.uniform(5, 100), 2),
        "solar_input": round(random.uniform(0, 300), 2),
        "power_consumption": round(random.uniform(50, 250), 2),
    }

def send_reading(data):
    try:
        response = requests.post(f"{BASE_URL}/readings/", json=data)
        print(f"[{response.status_code}] Sent: battery={data['battery_level']}% | solar={data['solar_input']}W | consumption={data['power_consumption']}W")
    except requests.exceptions.ConnectionError:
        print("Connection failed -> Check if the server is running")

if __name__ == "__main__":
    print(f" Simulator started for device {DEVICE_ID}")
    while True:
        reading = generate_reading()
        send_reading(reading)
        time.sleep(3)