import urllib.request
import bz2
import os

url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
zip_path = "shape_predictor_68_face_landmarks.dat.bz2"
dat_path = "shape_predictor_68_face_landmarks.dat"

if not os.path.exists(dat_path):
    print(f"Downloading {zip_path} from {url}... (This may take a minute)")
    urllib.request.urlretrieve(url, zip_path)
    
    print(f"Extracting to {dat_path}...")
    with bz2.BZ2File(zip_path) as fr, open(dat_path, "wb") as fw:
        fw.write(fr.read())
        
    print("Cleaning up...")
    os.remove(zip_path)
    print("Download and extraction complete. You are ready to go!")
else:
    print(f"Model file '{dat_path}' already exists!")
