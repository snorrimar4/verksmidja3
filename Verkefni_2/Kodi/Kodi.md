from gpiozero <br> import LED<br>
from time import sleep<br>

led = LED(17)<br>

while True:<br>
    led.on()<br>
    sleep(1)<br>
    led.off()<br>
    sleep(1)<br>
