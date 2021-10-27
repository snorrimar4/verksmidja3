from time import sleep  <br>
from picamera import PiCamera <br>

camera = PiCamera()<br>
camera.resolution = (1024, 768)<br>
camera.start_preview()<br>
# Camera warm-up time<br>
sleep(2)<br>
camera.capture('foo.jpg')<br>
