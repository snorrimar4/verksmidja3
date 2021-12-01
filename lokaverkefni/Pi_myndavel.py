import json
import paho.mqtt.client as mqtt
from GreenPonik_BH1750.BH1750 import BH1750
import RPi.GPIO as GPIO
import time
import datetime
import picamera
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
sensor = BH1750()
id = '4151cfcf-a611-4419-a330-f6b460face58' #einstakt id fengið t.d hér https://www.uuidgenerator.net/ Server og þessi þurfa sama 'id'
client_name = id + 'nightlight_client'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')
COMMASPACE = ', '
camera = picamera.PiCamera()
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN)
GPIO.setup(24, GPIO.OUT)

def Send_Email(image):
    sender = 'insert email address of sender'
    gmail_password = 'insert password of email address of sender'
    recipients = ['insert email address of recipient']

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'Intruder detected!'
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # List of attachments
    attachments = [image]

    # Add the attachments to the message
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: 1")
            raise

    composed = outer.as_string()
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
            print("Email sent!")
    except:
        print("Unable to send the email. Error: 2")
        raise

def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)
    if payload['intruder']:
        while True:
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            print("Intruder Detected at {}".format(st))
            camera.capture('image_Time_{}.jpg'.format(st))
            image = ('image_Time_{}.jpg'.format(st))
            Send_Email(image)
            time.sleep(2)
            break
    else:
       pass

mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command
mqtt_client.loop_start()

print("MQTT connected!")
while True:
    visible = sensor.read_bh1750()
    telemetry = json.dumps({'light' : visible})
    print("Sending telemetry " , telemetry)
    mqtt_client.publish(client_telemetry_topic, telemetry)
    time.sleep(1)