# Prompt for inputs
$projectFolder = Read-Host "Enter the name of your main project folder (e.g., ecommerce)"
$envPrefix = Read-Host "Enter the environment name prefix (e.g., myproject)"
$basePath = Read-Host "Enter the full path where the project should be created"

# Construct full paths
$envName = "${envPrefix}_env"
$fullProjectPath = Join-Path $basePath $projectFolder
$backendProjectName = "backend"
$appName = "base"

# Create project folder and navigate to it
New-Item -ItemType Directory -Path $fullProjectPath -Force | Out-Null
Set-Location -Path $fullProjectPath

# Create virtual environment
python -m venv $envName

# Activate the virtual environment
& ".\$envName\Scripts\Activate.ps1"

# Install Django
pip install django

# Create Django project
django-admin startproject $backendProjectName

# Navigate into backend project
Set-Location -Path $backendProjectName

# Create base app
django-admin startapp $appName

# Add app to settings.py
$settingsPath = ".\$backendProjectName\settings.py"
$settingsContent = Get-Content $settingsPath

# Add 'base.apps.BaseConfig' right after the opening of INSTALLED_APPS list
$modifiedContent = $settingsContent -replace "(?<=INSTALLED_APPS = \[)", "`n    '$appName.apps.BaseConfig',"

# Write changes to settings.py
$modifiedContent | Set-Content $settingsPath

# Run the server
python manage.py runserver
