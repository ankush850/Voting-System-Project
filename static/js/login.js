const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const scan = document.getElementById('scan');
const imageDataInput = document.getElementById('image_data');
const form = document.getElementById('login-form');

// Start webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Webcam access denied:", err);
        alert("Please allow webcam access.");
    });

// On click, capture image and submit
scan.addEventListener('click', () => {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/jpeg', 0.6);
    imageDataInput.value = dataURL;
    form.submit();
});
