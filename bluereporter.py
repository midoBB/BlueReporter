#!/usr/bin/python3

import json
import sys

from gi.repository import GLib
from pydbus import SystemBus

# Device class icons
MAJOR_DEVICE_CLASSES = {
    0x01: "💻",  # Computer
    0x02: "📱",  # Phone
    0x03: "🌐",  # LAN/Network Access Point
    0x04: "🎧",  # Audio/Video
    0x05: "⌨️",  # Peripheral
    0x06: "📷",  # Imaging
    0x07: "⌚",  # Wearable
    0x08: "🧸",  # Toy
    0x09: "❤️",  # Health
}


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
                devices[obj_path] = {
                    "name": device_props.get("Alias", "Unknown"),
                    "class": device_props.get("Class", None),
                }
    return devices


def decode_major_device_class(device_class):
    if device_class is None:
        return "❓"
    major_device_class = (device_class >> 8) & 0x1F
    return MAJOR_DEVICE_CLASSES.get(major_device_class, "❓")


def get_battery_level(device_path):
    try:
        bus = SystemBus()
        device = bus.get("org.bluez", device_path)
        properties = device["org.freedesktop.DBus.Properties"]
        return properties.Get("org.bluez.Battery1", "Percentage")
    except Exception:
        return None


def format_device_info(name, class_icon, battery_level):
    battery_status = f"{
        battery_level}%" if battery_level is not None else "N/A"
    return f"{class_icon}  {name}\t\t{battery_status}"


def main():
    devices = get_connected_bluetooth_devices()
    device_count = len(devices)

    # Format tooltip text with device information
    device_info_list = []
    for device_path, device_info in devices.items():
        name = device_info["name"]
        class_icon = decode_major_device_class(device_info["class"])
        battery_level = get_battery_level(device_path)
        device_info_list.append(format_device_info(
            name, class_icon, battery_level))

    tooltip_text = "\n".join(
        ["\t\tConnected Devices\t\t", "─" * 40, *device_info_list])

    # Prepare output data
    status_class = "active" if device_count > 0 else "inactive"
    out_data = {
        "text": f" {device_count}",  # Bluetooth icon + device count
        "tooltip": tooltip_text,
        "class": status_class,
    }

    print(json.dumps(out_data))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
