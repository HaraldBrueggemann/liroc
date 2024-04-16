from ..components.register import Register, RegisterGroup, RegisterGroupArray
from ..components.bitfield import BitField

from ..i2c.i2c import I2C


class Common():
    def __init__(self, i2c: I2C = None) -> None:
        self.i2c = i2c

        self.groups = RegisterGroupArray([
            RegisterGroup(64, [Register(0, [BitField(0, 2, 0x00, "NC", "Not connected"),
                                            BitField(2, 4, 0x0A, "PA_gain[3:0]", "Pre-Amp DC gain adjustment"),
                                            BitField(6, 1, 0x00, "PP_pa", "Power pulsing of Pre-Amp. 0: not pulsing"),
                                            BitField(7, 1, 0x01, "EN_pa", "Eanble of Pre-Amp. 1: enabled")]),
                               Register(1, [BitField(0, 6, 0x00, "NC", "Not connected"),
                                            BitField(6, 1, 0x00, "PP_7b", "Power pulsing of 7-bit channel-by-channel threshold. 0: not pulsing"),
                                            BitField(7, 1, 0x01, "EN_7b", "Enable of 7-bit channel-by-channel threshold. 1:enabled")]),
                               Register(2, [BitField(0, 4, 0x00, "NC", "Not connected"),
                                            BitField(4, 1, 0x00, "Cmd_hysteresis", "Discriminator hysteresis"),
                                            BitField(5, 1, 0x01, "Polarity", "Discriminator polarity selection 1: negative trigger out polarity for negative input charge"),
                                            BitField(6, 1, 0x00, "PP_disc", " Power pulsing discriminator. 0: not pulsed"),
                                            BitField(7, 1, 0x01, "EN_disc", "Enable of discriminator. 1: enabled")]),]),
            RegisterGroup(65, [Register(0, [BitField(0, 6, 0x00, "NC", "Not connected"),
                                            BitField(6, 1, 0x00, "PP_bg", "Power Pulsing of bandgap. 0: not pulsed"),
                                            BitField(7, 1, 0x01, "EN_bg", "Enable of bandgap. 1: enabled")]),
                               Register(1, [BitField(0, 2, 0x01, "dac_threshold[9:8]", "MSB DAC values"),
                                            BitField(2, 4, 0x00, "NC", "Not connected"),
                                            BitField(6, 1, 0x00, "PP_10bDAC", "Power Pulsing of 10b threshold DAC. 0: not pulsing"),
                                            BitField(7, 1, 0x01, "EN_10bDAC", "Enable of 10bit threshold DAC. 1 : enabled")]),
                               Register(2, [BitField(0, 8, 0xD8, "dac_threshold[7:0]", "LSB DAC values")]),]),
            RegisterGroup(66, [Register(0, [BitField(0, 4, 0x00, "EN-pE[0:3]", "CLPS pre-emphasis trimming"),
                                            BitField(4, 4, 0x04, "EN-CLPS[0:3]]", "CLPS buffer size trimming")]),
                               Register(1, [BitField(0, 6, 0x00, "NC", "Not connected"),
                                            BitField(6, 2, 0x00, "pE-delay[0:1]", "CLPS pre-emphasis delay trimming")]),]),
            RegisterGroup(67, [Register(0, [BitField(0, 3, 0x04, "MillerComp[2:0]", "Probe amplifier compensation capacitance trimming. Range: 0-700fF, step:100fF, default:400fF"),
                                            BitField(3, 3, 0x00, "NC", "Not connected"),
                                            BitField(6, 1, 0x00, "PP_probe", "Power pulsing of analogue probe. 0: not pulsing"),
                                            BitField(7, 1, 0x01, "EN_probe", "Enable of analogue probe. 1: enabled")]),
                               Register(1, [BitField(0, 6, 0x20, "lbo_probe[5:0]", "Output bias of probe amplifier, Range: 0-38µA, step:0.6µA default:20µA"),
                                            BitField(6, 2, 0x02, "lbi_probe[1:0]", "Input bias of probe amplifier. 00: 20µA, 01: 30µA, 10: 40µA, 11: 80µA")])])])

        # init from hw
        if self.i2c:
            # Init registers values from i2c
            for group in self.groups:
                for register in group:
                    value = self.i2c.read(register.i2c_address, 1)[0]
                    register.load(value)

    def save(self) -> dict:
        return {"groups": [group.save() for group in self.groups]}

    def load(self, configuration: dict) -> bool:
        if "groups" in configuration:
            self.groups.load(configuration["groups"])

        return True

    def to_json(self) -> dict:
        return {"groups": [group.to_json() for group in self.groups]}

    @property
    def preamp_gain_adjustment(self) -> int | None:
        register, field = self.groups.get_field("PA_gain[3:0]")
        if register and field:
            return field.value
        return None

    @preamp_gain_adjustment.setter
    def preamp_gain_adjustment(self, value) -> None:
        register, field = self.groups.get_field("PA_gain[3:0]")
        if register and field and self.i2c:
            register.update(self.i2c, field, value)

    @property
    def preamp_power_pulsing(self) -> int | None:
        register, field = self.groups.get_field("PP_pa")
        if register and field:
            return field.value
        return None

    @preamp_power_pulsing.setter
    def preamp_power_pulsing(self, value) -> None:
        register, field = self.groups.get_field("PP_pa")
        if register and field and self.i2c:
            register.update(self.i2c, field, value)

    @property
    def preamp_enable(self) -> int | None:
        register, field = self.groups.get_field("EN_pa")
        if register and field:
            return field.value
        return None

    @preamp_enable.setter
    def preamp_enable(self, value) -> None:
        register, field = self.groups.get_field("EN_Pa")
        if register and field and self.i2c:
            register.update(self.i2c, field, value)

    @property
    def channel_by_channel_threshold_power_pulsing(self) -> int | None:
        register, field = self.groups.get_field("PP_7b")
        if register and field:
            return field.value
        return None

    @channel_by_channel_threshold_power_pulsing.setter
    def powerpulsing_of_7bit_channel_by_channel_threshold_adjustment(self, value) -> None:
        register, field = self.groups.get_field("PP_7b")
        if register and field and self.i2c:
            register.update(self.i2c, field, value)

    @property
    def channel_by_channel_threshold_power_pulsing_enable(self) -> int | None:
        register, field = self.groups.get_field("EN_7b")
        if register and field:
            return field.value
        return None

    @channel_by_channel_threshold_power_pulsing_enable.setter
    def channel_by_channel_threshold_power_pulsing_enable(self, value) -> None:
        register, field = self.groups.get_field("EN_7b")
        if register and field and self.i2c:
            register.update(self.i2c, field, value)

    @property
    def discriminator_hysteresis(self) -> int | None:
        register, field = self.groups.get_field("Cmd_hysteresis")
        if register and field:
            return field.value
        return None

    @discriminator_hysteresis.setter
    def discriminator_hysteresis(self, value) -> None:
        register, field = self.groups.get_field("Cmd_hysteresis")
        if register and field and self.i2c:
            register.update(self.i2c, field, value)

    @property
    def discriminator_polarity_selection(self) -> int | None:
        register, field = self.groups.get_field("Polarity")
        if register and field:
            return field.value
        return None

    @discriminator_polarity_selection.setter
    def discriminator_polarity_selection(self, value) -> None:
        register, field = self.groups.get_field("Polarity")
        if register and field and self.i2c:
            register.update(self.i2c, field, value)

    @property
    def discriminator_power_pulsing(self) -> int | None:
        register, field = self.groups.get_field("PP_disc")
        if register and field:
            return field.value
        return None

    @discriminator_power_pulsing.setter
    def discriminator_power_pulsing(self, value) -> None:
        register, field = self.groups.get_field("PP_disc")
        if register and field and self.i2c:
            register.update(self.i2c, field, value)

    @property
    def discriminator_enable(self) -> int | None:
        register, field = self.groups.get_field("EN_disc")
        if register and field:
            return field.value
        return None

    @discriminator_enable.setter
    def discriminator_enable(self, value) -> None:
        register, field = self.groups.get_field("EN_disc")
        if register and field and self.i2c:
            register.update(self.i2c, field, value)

    @property
    def bandgap_power_pulsing(self) -> int | None:
        register, field = self.groups.get_field("PP_bg")
        if register and field:
            return field.value
        return None

    @bandgap_power_pulsing.setter
    def bandgap_power_pulsing(self, value) -> None:
        register, field = self.groups.get_field("PP_bg")
        if register and field and self.i2c:
            register.update(self.i2c, field, value)

    @property
    def bandgap_enable(self) -> int | None:
        register, field = self.groups.get_field("EN_bg")
        if register and field:
            return field.value
        return None

    @bandgap_enable.setter
    def bandgap_enable(self, value) -> None:
        register, field = self.groups.get_field("EN_bg")
        if register and field and self.i2c:
            register.update(self.i2c, field, value)

    @property
    def threshold_adjustment(self) -> int | None:
        register_lsb, field_lsb = self.groups.get_field("dac_threshold[7:0]")
        register_msb, field_msb = self.groups.get_field("dac_threshold[9:8]")
        if field_lsb and field_msb:
            return field_msb.value << 8 | field_lsb.value
        return None

    @threshold_adjustment.setter
    def threshold_adjustment(self, value) -> None:
        register_lsb, field_lsb = self.groups.get_field("dac_threshold[7:0]")
        register_msb, field_msb = self.groups.get_field("dac_threshold[9:8]")
        if register_msb and register_lsb and field_lsb and field_msb and self.i2c:
            register_lsb.update(self.i2c, field_lsb, value)
            register_msb.update(self.i2c, field_msb, value)
