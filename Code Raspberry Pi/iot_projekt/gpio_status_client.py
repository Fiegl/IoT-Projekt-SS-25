import requests
import time

API_URL = "http://[2001:7c0:2320:2:f816:3eff:fef8:f5b9]:8000/api/status/get/"

while True:
    try:
        response = requests.get(API_URL)
        daten = response.json()

        arbeitsplaetze = daten.get("arbeitsplaetze", [])

        for ap in arbeitsplaetze:
            desk_id = ap.get("id")
            status = ap.get("status")
            gpio_red = ap.get("gpio_red")
            gpio_green = ap.get("gpio_green")

            print(f"{desk_id}: Status = {status} | RED: {gpio_red} | GREEN: {gpio_green}")
            time.sleep(10)
            
            
