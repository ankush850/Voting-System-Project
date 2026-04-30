from flask import Flask, render_template, request, redirect, url_for, session, flash
import cv2
import face_recognition
import numpy as np
import os
import base64
from io import BytesIO
from PIL import Image
import dlib
from db_config import get_connection

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Load dlib's face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Liveness detection: eye blink based (EAR)
def get_eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def detect_liveness(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        left_eye = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(36, 42)])
        right_eye = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(42, 48)])
        ear = (get_eye_aspect_ratio(left_eye) + get_eye_aspect_ratio(right_eye)) / 2
        if ear < 0.2:  # blink threshold
            return True
    return False

@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        image_data = request.form.get('image_data')

        if not name or not username or not password or not image_data:
            flash("All fields are required.")
            return redirect(url_for('register'))

        try:
            image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            img = Image.open(BytesIO(image_bytes)).convert('RGB')
            frame = np.array(img)
        except:
            flash("Invalid image.")
            return redirect(url_for('register'))

        faces = face_recognition.face_locations(frame)
        if len(faces) != 1:
            flash("Please ensure only your face is visible.")
            return redirect(url_for('register'))

        if not detect_liveness(frame):
            flash("Liveness detection failed. Please blink.")
            return redirect(url_for('register'))

        encoding = face_recognition.face_encodings(frame, known_face_locations=faces)[0]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT face_encoding FROM users")
        for (face_data,) in cursor.fetchall():
            db_enc = np.frombuffer(face_data, dtype=np.float64)
            if face_recognition.compare_faces([db_enc], encoding)[0]:
                flash("Face already registered.")
                return redirect(url_for('register'))

        try:
            cursor.execute("INSERT INTO users (name, username, password, face_encoding) VALUES (%s, %s, %s, %s)",
                           (name, username, password, encoding.tobytes()))
            conn.commit()
            flash("Registered successfully!")
            return redirect(url_for('login'))
        except:
            conn.rollback()
            flash("Registration error.")
            return redirect(url_for('register'))
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        image_data = request.form['image_data']
        if not image_data:
            flash("No image received.")
            return redirect(url_for('login'))

        try:
            image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            img = Image.open(BytesIO(image_bytes)).convert('RGB')
            frame = np.array(img)
        except:
            flash("Invalid image.")
            return redirect(url_for('login'))

        faces = face_recognition.face_locations(frame)
        if len(faces) != 1:
            flash("Only one face should be visible.")
            return redirect(url_for('login'))

        if not detect_liveness(frame):
            flash("Liveness detection failed. Please blink.")
            return redirect(url_for('login'))

        encoding = face_recognition.face_encodings(frame, known_face_locations=faces)[0]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, face_encoding FROM users")
        for user_id, face_data in cursor.fetchall():
            db_encoding = np.frombuffer(face_data, dtype=np.float64)
            if face_recognition.compare_faces([db_encoding], encoding)[0]:
                session['user_id'] = user_id
                return redirect(url_for('vote'))

        flash("Face not recognized.")
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT has_voted FROM users WHERE id = %s", (user_id,))
    if cursor.fetchone()[0]:
        return redirect(url_for('vote_confirmation'))

    if request.method == 'POST':
        candidate_id = request.form['candidate']
        cursor.execute("SELECT name FROM candidates WHERE id = %s", (candidate_id,))
        candidate_name = cursor.fetchone()[0]

        cursor.execute("INSERT INTO votes (user_id, candidate_id) VALUES (%s, %s)", (user_id, candidate_id))
        cursor.execute("UPDATE users SET has_voted = TRUE WHERE id = %s", (user_id,))
        conn.commit()
        session['voted_candidate'] = candidate_name
        return redirect(url_for('vote_confirmation'))

    cursor.execute("SELECT id, name FROM candidates")
    candidates = cursor.fetchall()
    return render_template('vote.html', candidates=candidates)

@app.route('/vote_confirmation')
def vote_confirmation():
    return render_template('vote_confirmation.html')

@app.route('/results')
def results():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT c.name, COUNT(v.id) as vote_count FROM candidates c LEFT JOIN votes v ON c.id = v.candidate_id GROUP BY c.id")
    results = cursor.fetchall()
    return render_template("results.html", results=results)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
