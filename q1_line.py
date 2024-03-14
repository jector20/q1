from pymodbus.client import ModbusTcpClient
import random
import time
import os

def write_state(client : ModbusTcpClient):
    prod_count = 0
    try:
        while True:
            for address in range(40001, 40012, 2):
                r = client.write_register(address=address, value=0)
            time.sleep(1)
            for address in range(40001, 40012, 2):
                ok = random.choices(range(1000))[0] <= 989
                r = client.write_register(address=address, value=1 if ok else 2)
            time.sleep(1)
            prod_count = prod_count + 1
    except KeyboardInterrupt:
        pass
    finally:
        print(f"produce {prod_count}x6 items")

def cmdUI():
    ip = os.getenv("MODBUS_SERVER", "127.0.0.1")
    print(f"production line started.")
    with ModbusTcpClient(ip) as client:
        client.connect()
        write_state(client)

if __name__ == "__main__":
    cmdUI()