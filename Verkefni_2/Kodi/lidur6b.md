from picamera import PiCamera<br>
from datetime import datetime<br>
from signal import pause<br>
from time import sleep<br>

button = Button(12)<br>
camera = PiCamera()<br>

def capture():<br>
    timestamp = datetime.now().isoformat()<br>
    sleep(3)<br>
    camera.capture('/home/pi/time1.jpg')<br>

button.when_pressed = capture<br>

pause()<br>
