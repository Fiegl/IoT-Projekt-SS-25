import smbus2
import time
import threading


sensor_thread = None
stop_event = threading.Event()

def dauerhafte_messung():
    bus = smbus2.SMBus(1)
    device = 0x23
    mode = 0x10

    while not stop_event.is_set():
        try:
            bus.write_byte(device, mode)
            time.sleep(0.15)
            data = bus.read_i2c_block_data(device, 0x00, 2)
            lux = ((data[0] << 8) + data[1]) / 1.2
            print(f"{lux:.2f} Lux")
        except Exception as e:
            print("Sensorfehler:", e)
        time.sleep(5)

    bus.close()

def start_sensor():
    global sensor_thread
    if sensor_thread and sensor_thread.is_alive():
        return
    stop_event.clear()
    sensor_thread = threading.Thread(target=dauerhafte_messung, daemon=True)
    sensor_thread.start()

def stop_sensor():
    global stop_event, sensor_thread
    stop_event.set()
    if sensor_thread:
        sensor_thread.join()

