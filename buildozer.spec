[app]
title = Smart Finder Pro
package.name = smartfinder
package.domain = com.ammar.smartfinder
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas
source.exclude_dirs = .git,.github,.buildozer,bin,venv,__pycache__
version = 1.0.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a
android.private_storage = True
android.allow_backup = True
android.sdk = 31
android.build_tools = 31.0.0

p4a.fork = kivy
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
android.accept_sdk_license = True
