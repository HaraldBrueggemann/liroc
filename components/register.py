
from .bitfield import BitFieldArray, BitField
from ..i2c.i2c import I2C


class Register():
    def __init__(self, address: int, bitfields: BitFieldArray) -> None:
        self.group = None
        self.address = address
        self.fields = bitfields

    @property
    def i2c_address(self) -> list:
        r0 = (self.group & 0x07) << 5 | self.address & 0x1F
        r1 = self.group & 0xF8 >> 3
        return [r0, r1]

    def load(self, value: int):
        for field in self.fields:
            field.update(value)

    def save(self) -> dict:
        value = 0
        for field in self.fields:
            value |= field.value & field.bitmask
        return {"group": self.group,
                "address": self.address,
                "value": value}

    def update(self, i2c: I2C, field: BitField, value: int) -> None:
        # update field
        field.update(value)

        # update hardware
        reg_value = i2c.read(self.i2c_address(), 1)[0]
        reg_value &= ~field.bitmask
        reg_value |= field.value << field.start_bit

        i2c.write(self.i2c_address, reg_value)

    def to_json(self) -> dict:
        return {
            "group": self.group,
            "address": self.address,
            "fields": [field.to_json() for field in self.fields]
        }


class RegisterGroup(list):
    def __init__(self, index: int, registers: list) -> None:
        super().__init__(registers)
        self.index = index
        for register in self:
            register.group = self.index

    def get(self, address: int) -> Register | None:
        for register in self:
            if register.address == address:
                return register
        return None

    def save(self) -> dict:
        configuration = {"index": self.index,
                         "registers": [register.save() for register in self]}
        return configuration

    def load(self, group_config: dict):
        for register in self:
            register.load(group_config["registers"][register.address]["value"])

    def to_json(self) -> dict:
        return {"index": self.index,
                "registers": [register.to_json() for register in self]}


class RegisterGroupArray(list):
    def __init__(self, registergroups: list) -> None:
        super().__init__(registergroups)

    def get_register(self, index: int) -> Register | None:
        for group in self:
            if group.index == index:
                return group
        return None

    def get_field(self, name: str) -> tuple[Register, BitField] | None:
        for group in self:
            for register in group:
                for field in register.fields:
                    if field.name == name:
                        return register, field
        return None

    def load(self, group_config: dict):
        for config in group_config:
            index = config["index"]
            if len(self) > index:
                self[index].load(group_config[index])

    def to_json(self) -> dict:
        return [group.to_json() for group in self]
