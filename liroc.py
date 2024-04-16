from .blocks.channel import Channel
from .blocks.common import Common

from .i2c.i2c import I2C


class Liroc:
    def __init__(self, i2c: I2C = None):
        self.version = 1
        self.channels = [Channel(i, i2c) for i in range(64)]
        self.common = Common(i2c)

    def save(self):
        return {
            "version": self.version,
            "channels": [channel.save() for channel in self.channels],
            "common": self.common.save()
        }

    def load(self, configuration: dict):
        if "version" in configuration:
            if configuration["version"] >= self.version:
                if "channels" in configuration:
                    for channel in self.channels:
                        channel.load(configuration["channels"][channel.index])
                if "common" in configuration:
                    self.common.load(configuration["common"])

    def to_json(self):
        return {
            "version": self.version,
            "channels": [channel.to_json() for channel in self.channels],
            "common": self.common.to_json()
        }
