import psutil
import platform
import datetime
import os
import subprocess
import speedtest
import tkinter as tk
from tkinter import messagebox
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

# Toggle GUI and File saving here
gui_mode = True
save_to_file = False

def get_system_info():
    uname = platform.uname()
    return (
        f"System: {uname.system}\n"
        f"Node Name: {uname.node}\n"
        f"Release: {uname.release}\n"
        f"Version: {uname.version}\n"
        f"Machine: {uname.machine}\n"
        f"Processor: {uname.processor}\n"
    )

def get_cpu_info():
    return f"CPU Usage: {psutil.cpu_percent(interval=1)}%"

def get_memory_info():
    mem = psutil.virtual_memory()
    return f"RAM Usage: {mem.percent}% ({mem.used // (1024**2)} MB used)"

def get_disk_info():
    disk = psutil.disk_usage('/')
    return f"Disk Usage: {disk.percent}% ({disk.free // (1024**3)} GB free)"

def get_battery_info():
    battery = psutil.sensors_battery()
    if battery:
        return f"Battery: {battery.percent}% {'(Plugged in)' if battery.power_plugged else ''}"
    return "Battery: Not available"

def get_smart_disk_health():
    smartctl_path = r"C:\Program Files\smartmontools\bin\smartctl.exe"
    try:
        result = subprocess.run([smartctl_path, "-H", "C:"], capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if "SMART overall-health self-assessment test result" in line:
                return f"SMART Status: {line.split(':')[-1].strip()}"
    except Exception:
        return "SMART Status: Unknown or smartctl not found"
    return "SMART Status: Not available"

def get_internet_speed():
    try:
        s = speedtest.Speedtest()
        s.get_best_server()
        download = s.download() / 1_000_000
        upload = s.upload() / 1_000_000
        return f"Internet: ↓ {download:.2f} Mbps / ↑ {upload:.2f} Mbps"
    except Exception:
        return "Internet: Speed check failed"

def show_popup(summary, color="green"):
    root = tk.Tk()
    root.title("🖥️ PC Health Summary")
    root.geometry("420x260")
    root.resizable(False, False)

    text = tk.Text(root, height=15, width=60, wrap=tk.WORD)
    text.insert(tk.END, summary)
    text.config(state=tk.DISABLED, bg=color)
    text.pack(padx=10, pady=10)

    tk.Button(root, text="Close", command=root.destroy).pack(pady=5)
    root.mainloop()

def show_tray_icon(status):
    icon = Image.new("RGB", (64, 64), color="black")
    draw = ImageDraw.Draw(icon)
    draw.text((10, 10), status, fill="white")

    def on_quit(icon, item):
        icon.stop()

    menu = Menu(MenuItem("Quit", on_quit))
    tray_icon = Icon("PC Health", icon, menu=menu)
    tray_icon.run()

def generate_summary():
    summary = "\n".join([
        f"📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        get_cpu_info(),
        get_memory_info(),
        get_disk_info(),
        get_battery_info(),
        get_smart_disk_health(),
        get_internet_speed()
    ])
    return summary

def save_report(summary):
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"pc_health_report_{now}.txt"
    save_path = os.path.join(os.path.expanduser("~"), "Documents", filename)
    with open(save_path, "w") as f:
        f.write(summary)
    print(f"✅ Report saved to {save_path}")

# === MAIN ===
summary = generate_summary()

# Health Check Color Coding
cpu_usage = psutil.cpu_percent(interval=1)
disk_usage = psutil.disk_usage('/').percent

color = "green"  # Default color
if cpu_usage > 80 or disk_usage > 85:
    color = "red"  # Bad health
elif cpu_usage > 50 or disk_usage > 70:
    color = "yellow"  # Warning health

if gui_mode:
    show_popup(summary, color)

if save_to_file:
    save_report(summary)

# Show Tray Icon with Health Status
status = f"CPU: {cpu_usage}% | Disk: {disk_usage}%"
show_tray_icon(status)
