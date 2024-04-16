from smbus2 import SMBus, i2c_msg

from ..components.bitfield import BitField


class I2C:
    def __init__(self, bus: SMBus, dev_address: int):
        self.bus = bus
        self.address = dev_address

    def _write(self, registers: list, value: int):
        registers.append(value)
        write_msg = i2c_msg.write(self.address, registers)
        self.bus.i2c_rdwr(write_msg)

    def _read(self, registers:list, length: int) -> list:
        write_msg = i2c_msg.write(self.address, registers)
        read_msg = i2c_msg.read(self.address, length)
        self.bus.i2c_rdwr(write_msg, read_msg)
        return list(read_msg)
    
    def write(self, field: BitField) -> None:
        value = self._read(self.i2c_address(), 1)[0]
        value &= ~field.bitmask
        value |= field.value << field.start_bit
        self._write(self.i2c_address, value)
