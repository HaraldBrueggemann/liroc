class BitField():
    def __init__(self, start_bit: int, length: int, default_value: int, name: str, description: str) -> None:
        self.start_bit = start_bit
        self.length = length
        self.value = default_value
        self.name = name
        self.description = description

    @property
    def bitmask(self) -> int:
        bitmask = 1 << self.start_bit
        for i in range(self.length - 1):
            bitmask |= self.start_bit + i
            bitmask <<= 1
        return bitmask

    def update(self, value: int) -> None:
        self.value = (value & self.bitmask) >> self.start_bit

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "value": self.value,
            "start_bit": self.start_bit,
            "length": self.length,
            "description": self.description
        }


class BitFieldArray(list):
    def __init__(self, fields: list) -> None:
        super().__init__(fields)

    def getField(self, name: str) -> BitField | None:
        return next((x for x in self if x.name == name), None)
