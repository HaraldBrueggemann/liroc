
from ..components.register import Register, RegisterGroup, RegisterGroupArray
from ..components.bitfield import BitField

from ..i2c.i2c import I2C


class Channel():
    def __init__(self, channel_index: int, i2c: I2C = None) -> None:
        self.index = channel_index
        self.i2c = i2c

        # define Registers
        self.groups = RegisterGroupArray([RegisterGroup(self.index, [Register(0, [BitField(0, 1, 0x00, "NC", "Not connected"),
                                                                                  BitField(1, 1, 0x00, "Ctest", "Injection capacitance connection switch. 0: open"),
                                                                                  BitField(2, 6, 0x00, "DC_PA[5:0]", "Channel-by-channel imput DC level setting")]),
                                                                     Register(1, [BitField(0, 7, 0x40, "DAC_local[6:0]", "Channel-by-channel 7-bit threshold adjustment"),
                                                                                  BitField(7, 1, 0x00, "Mask", "Mask Trigger 0: not masked")])])])
        # init from hw
        if self.i2c:
            # Init registers values from i2c
            for group in self.groups:
                for register in group:
                    value = self.i2c.read(register.i2c_address, 1)[0]
                    register.load(value)

    def save(self) -> dict:
        return {"channel": self.index,
                "groups": [group.save() for group in self.groups]}

    def load(self, configuration: dict) -> bool:
        if "groups" in configuration:
            self.groups.load(configuration["groups"])
        return True

    def to_json(self) -> dict:
        return {"groups": [group.to_json() for group in self.groups]}

    @property
    def injection_capacitance_connection_switch(self) -> int | None:
        register, field = self.groups.get_field("Ctest")
        if register and field:
            return field.value
        return None

    @injection_capacitance_connection_switch.setter
    def injection_capacitance_connection_switch(self, value) -> None:
        register, field = self.groups.get_field("Ctest")
        if register and field and self.i2c:
            register.update(self.i2c, field, value)

    @property
    def channel_by_channel_input_dc_level(self) -> int | None:
        register, field = self.groups.get_field("DC_PA[5:0]")
        if register and field:
            return field.value
        return None

    @channel_by_channel_input_dc_level.setter
    def channel_by_channel_input_dc_level(self, value) -> None:
        register, field = self.groups.get_field("DC_PA[5:0]")
        if register and field and self.i2c:
            field.update(value)
            register.update(self.i2c, field, value)

    @property
    def channel_by_channel_threshold_adjustment(self) -> int | None:
        register, field = self.groups.get_field("DAC_local[6:0]")
        if register and field:
            return field.value
        return None

    @channel_by_channel_threshold_adjustment.setter
    def channel_by_channel_threshold_adjustment(self, value) -> None:
        register, field = self.groups.get_field("DAC_local[6:0]")
        if register and field and self.i2c:
            register.update(self.i2c, field, value)

    @property
    def mask_trigger(self) -> int | None:
        register, field = self.groups.get_field("Mask")
        if register and field:
            return field.value
        return None

    @mask_trigger.setter
    def mask(self, value) -> None:
        register, field = self.groups.get_field("Mask")
        if register and field and self.i2c:
            register.update(self.i2c, field, value)
