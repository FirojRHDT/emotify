import cv2
import numpy as np
from flask import Flask, render_template, Response
import requests

app = Flask(__name__)

# Load pre-trained emotion detection model
# You can load your model here (example: model = load_model('model.h5'))
# For simplicity, let's mock the model's predictions
def get_emotion(frame):
    # Here, you can replace with your model's prediction logic
    # For demonstration, let's return a random emotion
    emotions = ['happy', 'sad', 'angry', 'surprised']
    return np.random.choice(emotions)

# Function to generate frames from the webcam
def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Detect emotion (mocked)
            emotion = get_emotion(frame)
            # Display detected emotion on frame
            cv2.putText(frame, emotion, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Convert frame to JPEG for streaming
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_playlist/<emotion>')
def get_playlist(emotion):
    # Dummy function to return a YouTube playlist URL based on emotion
    playlists = {
        'happy': 'https://youtube.com/playlist?list=PL9khxBZiiQwoKEqdTrb4ip-S_Tov6FkBQ&si=h0fZ2K9n4LICUVnm',
        'sad': 'https://youtube.com/playlist?list=PLDL1LmzYahkcwTMCkYg9wizbtcB_30yax&si=TU4B1jc5JhEs7lMA',
        'angry': 'https://youtube.com/playlist?list=PLxNm0dqHxmlupV3dr7uq4Rl8L5nwlGKQA&si=--2hXqAhH2bIzbAj',
        'surprised': 'https://youtube.com/playlist?list=PLHM4Qas12Eo60v5S4jCBroz47GlBuquIg&si=Z7ipbvRuroXLwB5o'
    }
    return {'playlist': playlists.get(emotion, 'No playlist available')}

if __name__ == '__main__':
    app.run(debug=True)
