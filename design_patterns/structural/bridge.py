from abc import ABC, abstractmethod


# ---------- IMPLEMENTATION (Device) ----------

class Device(ABC):
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @abstractmethod
    def set_volume(self, value):
        pass


class TV(Device):
    def turn_on(self):
        print("TV on")

    def turn_off(self):
        print("TV off")

    def set_volume(self, v):
        print(f"TV volume = {v}")


class Radio(Device):
    def turn_on(self):
        print("Radio on")

    def turn_off(self):
        print("Radio off")

    def set_volume(self, v):
        print(f"Radio volume = {v}")


# ---------- ABSTRACTION (Remote) ----------

class Remote:
    def __init__(self, device: Device):
        self.device = device

    def on(self):
        self.device.turn_on()

    def off(self):
        self.device.turn_off()


class AdvancedRemote(Remote):
    def mute(self):
        self.device.set_volume(0)


def main():
    tv_remote = AdvancedRemote(TV())
    radio_remote = Remote(Radio())

    tv_remote.on()
    tv_remote.mute()
    radio_remote.on()


if __name__ == "__main__":
    main()
