import smbus2
import time
import threading

sensor_threads = {}
stop_events = {}
luxwerte = {}

def dauerhafte_messung(arbeitsplatz_id, i2c_bus, i2c_address):
    bus = smbus2.SMBus(i2c_bus)
    mode = 0x10
    stop_event = stop_events[arbeitsplatz_id]

    while not stop_event.is_set():
        try:
            bus.write_byte(i2c_address, mode)
            time.sleep(0.15)
            data = bus.read_i2c_block_data(i2c_address, 0x00, 2)
            lux = ((data[0] << 8) + data[1]) / 1.2
            luxwerte[arbeitsplatz_id] = round(lux, 2)
            print(f"[{arbeitsplatz_id}] {lux:.2f} Lux")
        except Exception as e:
            print(f"[{arbeitsplatz_id}] Sensorfehler:", e)
            luxwerte[arbeitsplatz_id] = -1
        time.sleep(5)

    bus.close()

def start_sensor(arbeitsplatz_id, i2c_bus=1, i2c_address=0x23):
    if arbeitsplatz_id in sensor_threads and sensor_threads[arbeitsplatz_id].is_alive():
        return  

    stop_events[arbeitsplatz_id] = threading.Event()
    thread = threading.Thread(
        target=dauerhafte_messung,
        args=(arbeitsplatz_id, i2c_bus, i2c_address),
        daemon=True
    )
    sensor_threads[arbeitsplatz_id] = thread
    thread.start()

def stop_sensor(arbeitsplatz_id):
    if arbeitsplatz_id in stop_events:
        stop_events[arbeitsplatz_id].set()
    if arbeitsplatz_id in sensor_threads:
        sensor_threads[arbeitsplatz_id].join()
        del sensor_threads[arbeitsplatz_id]
        del stop_events[arbeitsplatz_id]
        luxwerte.pop(arbeitsplatz_id, None)

def get_luxwert(arbeitsplatz_id):
    wert = luxwerte.get(arbeitsplatz_id)
    if wert is None:
        return "kein Sensor angeschlossen"
    elif wert == -1:
        return "Sensorfehler"
    else:
        return f"{wert} Lux"



