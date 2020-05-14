from api.mFi.mFiApi import MfiApi
api = MfiApi()


def get_devices():
    devices = list()
    devices.append(api.get_devices())
    return devices


def handle(device = None, action = None):
    print(f"device: {device}, action: {action}")
    return True