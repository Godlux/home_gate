import json


class ApiBase( object ):
    """ The base class for api """

    def get_devices(self):
        return list()

    def get_commands_for_device(self, device_id):
        return str()

    def turn_on_device(self, device_id):
        pass

    def turn_off_device(self, device_id):
        pass

    def send_command_to_device(self, device_id):
        pass