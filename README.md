# Momentum Android

<p align="center">
  <strong>A focused, dark-mode productivity companion built with Python, Kivy, and KivyMD.</strong>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white">
  <img alt="Kivy" src="https://img.shields.io/badge/UI-Kivy-2F9FD7">
  <img alt="KivyMD" src="https://img.shields.io/badge/Material_UI-KivyMD-6C8CFF">
  <img alt="Platform" src="https://img.shields.io/badge/Platform-Android-3DDC84?logo=android&logoColor=white">
  <img alt="Build" src="https://img.shields.io/badge/APK-GitHub_Actions-2088FF?logo=githubactions&logoColor=white">
</p>

Momentum brings daily planning and focused work into one app. The project is being prepared for Android packaging; the APK workflow is intended to build a debug APK on GitHub-hosted Linux runners so local Ubuntu is not required.

## Features

- **Dashboard** — daily overview, habits, and routine progress
- **Habits & routines** — track recurring actions and daily checklists
- **Pomodoro** — focus/break timer and preset support
- **Study tracker** — record study sessions and review activity
- **Calendar** — organize and review daily study/work records
- **Statistics** — inspect progress and productivity metrics
- **Goals & projects** — track longer-term objectives
- **Settings & backup** — manage app settings and data backup

> Feature availability depends on the current source revision. This repository is being prepared for its first reproducible Android build.

## Tech stack

- Python
- Kivy
- KivyMD 1.2.0
- SQLite
- Buildozer / python-for-android
- GitHub Actions for cloud APK builds

## Build an Android debug APK

1. Open the **Actions** tab.
2. Choose **Build Momentum Android APK**.
3. Select **Run workflow**.
4. When the run succeeds, download the `Momentum-Android-debug-APK` artifact.
5. Extract the artifact ZIP and install the APK on your Android device.

The first Android build may take several minutes while Android SDK/NDK and Python dependencies are downloaded. The workflow needs the actual app source and a valid `buildozer.spec` at the expected project path before it can succeed.

## Run on Windows for development

Create and activate a virtual environment in the app folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Install the dependencies listed by the project, then run:

```powershell
python main.py
```

Kivy Android packaging is different from running the Python app on Windows. Use the GitHub Actions workflow for APK packaging.

## Repository layout

```text
.github/
  workflows/
    android-apk.yml
momentum_android/
  main.py
  buildozer.spec
  config/
  controllers/
  database/
  models/
  screens/
  services/
  themes/
  utils/
```

## Data and privacy

- Do not commit your personal SQLite database, backups, passwords, API keys, signing keys, or local virtual environments.
- Keep personal data out of screenshots and issue reports.
- Back up your database before testing a new build.

## Contributing / reporting issues

Use the **Issues** tab to report reproducible bugs or suggest improvements. Include your device/Android version, steps to reproduce, expected behavior, actual behavior, and relevant logs. Do not attach private databases or credentials.

## Project status

The project is in active development. Debug APKs are for testing, not a production release. Android-device testing, backup/restore validation, and release signing should be completed before distribution.

## License

No license has been declared yet. Unless a license is added, all rights remain with the copyright holder and reuse is not automatically permitted.
