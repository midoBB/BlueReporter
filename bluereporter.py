import sys

from gi.repository import GLib
from pydbus import SystemBus


def get_connected_bluetooth_devices():
    bus = SystemBus()
    bluez = bus.get("org.bluez", "/")

    manager = bluez["org.freedesktop.DBus.ObjectManager"]
    objects = manager.GetManagedObjects()

    devices = {}
    for obj_path, interfaces in objects.items():
        if "org.bluez.Device1" in interfaces:
            device_props = interfaces["org.bluez.Device1"]
            if device_props.get("Connected", False):
                devices[obj_path] = device_props.get("Alias", "Unknown")
    return devices


def get_battery_level(device_path):
    try:
        bus = SystemBus()
        device = bus.get("org.bluez", device_path)
        properties = device["org.freedesktop.DBus.Properties"]
        return properties.Get("org.bluez.Battery1", "Percentage")
    except Exception:
        return None


def main():
    devices = get_connected_bluetooth_devices()
    if not devices:
        print("No connected Bluetooth devices found.")
        return

    for device_path, device_name in devices.items():
        battery_level = get_battery_level(device_path)
        if battery_level is not None:
            print(f"Device: {device_name} | Battery Level: {battery_level}%")
        else:
            print(f"Device: {device_name} | Battery Level: Not available")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
