from gpiozero import MotionSensor, LED<br>
from time import sleep<br>

pir = MotionSensor(4)<br>
led = LED(16)<br>

i = 0<br>
<br>
while True:<br>

    if pir.motion_detected:<br>
        print("Motion Detected ", i )<br>
        led.on()<br>
    else:<br>
        print("No Motion ", i)<br>
        led.off()<br>
    <br>
    i += 1<br>
    <br>
    sleep(.2)<br>
