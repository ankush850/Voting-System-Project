const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const capture = document.getElementById('capture');
const imageDataInput = document.getElementById('image_data');
const form = document.getElementById('register-form');

// Start webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        alert("Could not access the camera. Please allow camera access.");
        console.error("Camera error:", err);
    });

// On click, capture image and submit
capture.addEventListener('click', () => {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/jpeg', 0.6);
    imageDataInput.value = dataURL;
    form.submit();
});
