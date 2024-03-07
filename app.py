from flask import Flask, render_template, request, redirect, url_for, Response, flash, session
from flask_mail import Mail, Message
import cv2
import time

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your SMTP server
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TSL'] = False
app.config['MAIL_USERNAME'] = 'pigvitals@gmail.com'  # Your username
app.config['MAIL_PASSWORD'] = 'cxho vzxs qgyv ijji'  # Your email account password
app.config['MAIL_DEFAULT_SENDER'] = 'pigvitals@gmail.com'  # Your email
app.secret_key = 'kuba12345'

mail = Mail(app)

def generate_video_stream(video_path):
    cap = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not cap.isOpened():
        print("Error opening video stream or file")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)  # Get the original video's frame rate
    frame_delay = 1 / fps  # Calculate the delay between frames for real-time playback
    i = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Write some Text
            font = cv2.FONT_HERSHEY_SIMPLEX
            #cv2.putText(frame, 'Ticks: ' + str(i) , (10, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            i +=1
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield a frame as a byte stream
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            time.sleep(frame_delay)  # Introduce delay for real-time playback speed
        else:
            break

    cap.release()


@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_video_stream('static/pig_demo_deepsort_info_demo.mp4'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/thesis_info')
def thesis_info():
    return render_template('thesis_info.html')

@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Create the message
    msg = Message("Návrh na zlepšení!",
                  recipients=["jakub.rd@seznam.cz"],  # Email address where you want to receive emails
                  body=f"Jméno odesílatele: {name}\n"
                       f"Email odesílatele: {email}\n"
                       f"\n"
                       f"\n"
                       f"{message}")

    # Send the email
    mail.send(msg)
    flash('Vaše zpráva byla úspěšně odeslána. Děkujeme!', 'success')

    # Redirect to a new page or back to the contact form with a success message
    return redirect(url_for('contact'))
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
