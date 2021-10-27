import RPi.GPIO as GPIO<br>
import time<br>
import datetime<br>
import picamera<br>
import os<br>
import smtplib<br>
from email import encoders<br>
from email.mime.base import MIMEBase<br>
from email.mime.multipart import MIMEMultipart<br>


camera = picamera.PiCamera()<br>
GPIO.setmode(GPIO.BCM)<br>

GPIO.setup(4, GPIO.IN) #PIR<br>
GPIO.setup(24, GPIO.OUT) #BUzzer<br>

'''
ts = time.time()<br>
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')<br>
'''



COMMASPACE = ', '<br>

def Send_Email(image):<br>
    sender = 'snorrimar444@gmail.com'<br>
    gmail_password = 'hér var lykilorðið mitt ;)'<br>
    recipients = ['snorrimar4@icloud.com']<br>

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'Attachment Test'
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
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise

    composed = outer.as_string()

    # Send the email
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
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise



try:<br>
    time.sleep(2) # to stabilize sensor<br>
    
            
    while True:
        ##Timeloop
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        if GPIO.input(4):
            ##If loop
            GPIO.output(24, True)
            time.sleep(0.5) #Buzzer turns on for 0.5 sec
            print("Motion Detected at {}".format(st))
            ##Adds timestamp to image
            camera.capture('image_Time_{}.jpg'.format(st))
            image = ('image_Time_{}.jpg'.format(st))
            Send_Email(image)
            time.sleep(2)
            GPIO.output(24, False)
            time.sleep(5) #to avoid multiple detection

        time.sleep(0.1) #loop delay, should be less than detection delay

except:<br>
    GPIO.cleanup()
<br>
