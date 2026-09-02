[app]

# (string) Title of your application
title = Smart Finder Pro

# (string) Package name
package.name = smartfinder

# (string) Package domain (needed for android packaging)
package.domain = com.ammar.smartfinder

# (string) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,jpeg,kv,atlas

# (list) List of exclusions using pattern matching
source.exclude_dirs = .git,.github,.buildozer,bin,venv,__pycache__

# (string) Application version
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy

# (string) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (boolean) High-screen expectancy
fullscreen = 0

# =============================================================================
# Android specific configuration
# =============================================================================

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (string) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use
android.ndk_api = 21

# (list) The Android architectures to build for
android.archs = arm64-v8a

# (bool) Use private storage for data
android.private_storage = True

# (bool) Allow backup of application data
android.allow_backup = True

# (bool) Accept SDK license without manual input
android.accept_sdk_license = True

# (string) Android build tools version (Optional)
android.build_tools_version = 34.0.0

# =============================================================================
# Python for android (p4a) specific configuration
# =============================================================================

# (string) python-for-android fork to use
p4a.fork = kivy

# (string) python-for-android branch to use
p4a.branch = master


# =============================================================================
# Buildozer specific configuration
# =============================================================================

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
