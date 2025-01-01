BlueReporter is a Python script designed to report the battery levels of connected Bluetooth devices. It integrates seamlessly as a component for status bars like Polybar or Waybar, enabling real-time Bluetooth battery monitoring on your desktop.

# Usage

## Install Dependencies:

```terminal
pip install pydbus PyGObject
```
> This should be ran on the main user environment

Or on Ubuntu/Debian

```terminal
sudo apt install python3-pydbus python3-gi python3-gi-cairo
```

## Run the Script:

```terminal
python bluereporter.py
```

## Integration with Polybar:

Add the following to your Polybar config:

```ini
[module/bluetooth]
type = custom/script
exec = /path/to/bluereporter.py
interval = 120
```

## Integration with Waybar:

Add this to your Waybar config:

```json
+  "custom/bluetooth": {
+      "exec": "path/to/bluereporter.py 2> /dev/null",
+      "return-type": "json",
+      "interval": 120,
+      "format": "{}",
+      "on-click": "blueman-manager",
+      "tooltip": true
+  }
```
