from gpiozero import Button<br>
from picamera import PiCamera<br>
from datetime import datetime<br>
from signal import pause<br>

button = Button(2)<br>
camera = PiCamera()<br>

def capture():<br>
    timestamp = datetime.now().isoformat()<br>
    camera.capture('/home/pi/%s.jpg' % timestamp)<br>

button.when_pressed = capture<br>

pause()
