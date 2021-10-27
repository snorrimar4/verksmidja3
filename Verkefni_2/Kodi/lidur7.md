from gpiozero import MotionSensor, LED<br>
from time import sleep<br>

pir = MotionSensor(4)<br>
led = LED(16)<br>

i = 0<br>
<br>
while True:<br>

    if pir.motion_detected
        print("Motion Detected ", i )
        led.on()
    else:
        print("No Motion ", i)
        led.off()
    
    i += 1
    
    sleep(.2)
