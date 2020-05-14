from api.abstract_api import ApiBase
from .devices import Device
from .mfi_device_listener import MfiListener


class MfiApi( ApiBase ):
    """ The base class for api """

    def __init__(self):
        self.mfi_device_listener = MfiListener()
        self.mfi_device_listener.start()

    def get_devices(self):
        devices = list()
        devices_dict = self.mfi_device_listener.devices

        import json
        with open ('devices.json', 'r') as registred_devices:
            json.load(registred_devices)

            print(len(devices_dict))  # fixme debug
            for device_ip in devices_dict:
                data = devices_dict[device_ip]
                print(f"D{device_ip}, DA{data}")
                for registred_device in registred_devices:
                    if device_ip == registred_device["ip"]:
                        device = Device(name=registred_device["name"], ip=device_ip, mfi_data=data)
                        devices.append(device)

        return devices

    def get_commands_for_device(self, device_id):
        return str()

    def turn_on_device(self, device_id):
        pass

    def turn_off_device(self, device_id):
        pass

    def send_command_to_device(self, device_id):
        pass