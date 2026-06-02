# Some-Useful-scripts
This repo is for my collection of some scripts that may be of help

### pc_health_report.py

Windows PC health monitoring tool with a simple GUI and system tray integration.

#### Features
- CPU, RAM, and disk usage monitoring
- Battery status reporting
- SMART disk health checks (Smartmontools)
- Internet speed testing
- Color-coded health status indicators
- Optional report export to Documents
- System tray icon support

#### Requirements
- Python 3.8+
- psutil
- speedtest-cli
- pystray
- Pillow

#### Run

```bash
python pc_health_report.py
```

---

### setup_django.ps1

PowerShell script that automates the creation of a Django project structure.

#### Features
- Prompts for project folder, environment name, and installation path
- Creates and activates a Python virtual environment
- Installs Django automatically
- Creates a Django project named `backend`
- Creates a Django app named `base`
- Adds `base.apps.BaseConfig` to `INSTALLED_APPS`
- Starts the Django development server

#### Requirements
- Windows PowerShell 5.1+ or PowerShell 7+
- Python installed and available in PATH

#### Run

```powershell
.\setup_django.ps1
```
