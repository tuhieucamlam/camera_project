from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# for ip camera
#camera = cv2.VideoCapture('rtsp://admin:VIRYFYCODE@192.168.8.101:554/h264/ch1/main/av_stream') #螢石
# mp4
#camera = cv2.VideoCapture('test.mp4')
# web-cam: 0=first cam
#camera = cv2.VideoCapture(0)

camera = cv2.VideoCapture('rtsp://192.168.1.53/media/video2')

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # use yield to return this time image
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_start')
def video_start():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #app.run()