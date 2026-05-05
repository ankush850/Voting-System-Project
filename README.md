# 🗳️ Secure Voting System with Facial Recognition

A robust, web-based voting platform built with Flask, utilizing advanced facial recognition and liveness detection to ensure secure, verifiable, and transparent elections.

## ✨ Key Features
- **Facial Recognition Authentication**: Users register and log in securely using their face.
- **Liveness Detection (Anti-Spoofing)**: Enforces an eye-blink check using Eye Aspect Ratio (EAR) via 68-point facial landmarks to prevent spoofing via printed photos or screens.
- **Secure Voting Integrity**: Implements database-level `UNIQUE` constraints and server-side transaction handling to completely prevent double-voting and race-condition exploits.
- **Live Results Dashboard**: Real-time aggregation of votes for each candidate.

## 🛠️ Technology Stack
- **Backend Framework:** Python / Flask
- **Database:** MySQL
- **Computer Vision:** OpenCV (`cv2`), `dlib`, `face_recognition`, `numpy`
- **Frontend:** HTML/CSS (Jinja2 Templates)

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.8+
- MySQL Server running locally
- C++ Build Tools & CMake (Required on Windows for building `dlib` during installation)

### 2. Clone the Repository
```bash
git clone https://github.com/ankush850/Voting-System-Project.git
cd Voting-System-Project
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Note: If `dlib` fails to install on Windows, ensure you have CMake and Visual Studio C++ Build Tools installed, or use a pre-compiled wheel).*

### 4. Download Required ML Models
The application requires the dlib 68-point face landmark predictor model. Run the included script to download and extract it automatically (~100MB):
```bash
python download_model.py
```

### 5. Database Setup
1. Ensure your local MySQL server is running.
2. The setup scripts assume your MySQL root password is `votingsystem`. If yours is different, update the `password` field in both `db_config.py` and `setup_db.py`.
3. Run the setup script to initialize the database, tables, and insert default candidates:
```bash
python setup_db.py
```

### 6. Run the Application
```bash
python app.py
```
The application will start and be available in your browser at `http://127.0.0.1:5000`.

## 🛡️ Security Architecture
This system addresses critical vulnerabilities found in conventional digital voting systems:
- **Enforced Single Voting**: A database-level constraint makes it physically impossible for the system to record more than one vote per user, neutralizing automated scripts and race conditions.
- **Biometric Presence Validation**: Requires real-time physical interaction (blinking) to validate that the user is physically present in front of the camera, neutralizing static photo bypasses.
