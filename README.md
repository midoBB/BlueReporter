BlueReporter is a Python script designed to report the battery levels of connected Bluetooth devices. It integrates seamlessly as a component for status bars like Polybar or Waybar, enabling real-time Bluetooth battery monitoring on your desktop.

# Usage

## Install Dependencies:

```terminal
pip install pydbus PyGObject
```

## Run the Script:

```terminal
python bluereporter.py
```

## Integration with Polybar:

Add the following to your Polybar config:

```ini
[module/bluetooth_battery]
type = custom/script
exec = python /path/to/bluereporter.py
interval = 60
```

## Integration with Waybar:

Add this to your Waybar config:

```json
"custom/bluetooth_battery": {
    "exec": "python /path/to/bluereporter.py",
    "interval": 60
}
```
