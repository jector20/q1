from pymodbus.client import ModbusTcpClient
from datetime import datetime as dt
import time
import os

class State:

    def __init__(self):
        self.reset()

    def set(self, value, time):
        if not self.t_time:
            self.t_time = time
            self.prev = self.curr
            self.curr = value
            return

        if self.curr != value and (dt.now() - self.t_time).total_seconds() >= 1:
            self.t_time = time
            self.prev = self.curr
            self.curr = value

            if self.curr == 0:
                if self.prev == 1:
                    self.ok_count += 1
                elif self.prev == 2:
                    self.ng_count += 1

    def reset(self):
        self.ok_count = 0
        self.ng_count = 0
        self.t_time = None
        self.curr = 0
        self.prev = None

def read_product(client : ModbusTcpClient):
    state_list = {address: State() for address in range(40001, 40012, 2)}
    report_rate = 1
    report_time = dt.now()
    sample_rate = 0.5       #  second per times
    sample_time = dt.now()

    while True:
        # read registers
        for address in range(40001, 40012, 2):
            r = client.read_holding_registers(address=address)
            state_list[address].set(r.registers[0], dt.now())
        sample_time = dt.now()
        # save result
        ok_count = 0
        ng_count = 0
        for address, state in state_list.items():
            ok_count += state.ok_count
            ng_count += state.ng_count
        # sample rate
        time_used = (dt.now() - sample_time).total_seconds()
        if time_used < sample_rate:
            time.sleep(sample_rate-time_used)

            # report rate
        if (dt.now() - report_time).total_seconds()*1000 >= (1000 / report_rate):
            print("===")
            print(f"total:  OK/NG: ({ok_count:>10}/{ng_count:>10})")
            report_time = dt.now()
 

def cmdUI():
    ip = os.getenv("MODBUS_SERVER", "127.0.0.1")
    print(f"Connecting to {ip} ... ")
    with ModbusTcpClient(ip) as client:
        client.connect()
        try:
            read_product(client)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    cmdUI()