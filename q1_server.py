from pymodbus.server import ModbusTcpServer, StartTcpServer
from pymodbus.datastore.context import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSparseDataBlock
from pymodbus.device import ModbusDeviceIdentification
import asyncio
import os


id = ModbusDeviceIdentification(info_name={"VendorName": "test",
        "ProductCode": "00001",
        "MajorMinorRevision": 1,
        "VendorUrl": "https://www.test.com",
        "ProductName": "product",
        "ModelName": "model",
        "UserApplicationName": "product"})

async def Device(context, id):
    ip = os.getenv("MODBUS_SERVER", "127.0.0.1")
    print(f"Start server at {ip}")
    server = ModbusTcpServer(context, address=(ip, 502), identity=id)
    await server.serve_forever()
    
async def Server(id):
    #context = ModbusSlaveContext(hr=ModbusSparseDataBlock({40001: 100, 40003: 99, 40005: 98, 40007: 97, 40009: 96, 40011: 95}), zero_mode=True)
    context = ModbusSlaveContext(hr=ModbusSparseDataBlock({40001: 0, 40003: 1, 40005: 0, 40007: 1, 40009: 0, 40011: 0}), zero_mode=True)
    context = ModbusServerContext(slaves=context, single=True)

    async with asyncio.TaskGroup() as tg:
        device1 = tg.create_task(Device(context, id))

def main():
    pass

if __name__ == "__main__":
    #main()

    asyncio.run(Server(id))