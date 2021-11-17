from gpiozero import Button, LED
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero.tools import all_values
from signal import pause

factory3 = PiGPIOFactory(host='10.11.46.15')
factory4 = PiGPIOFactory(host='10.11.46.4')

led = LED(17)
button_1 = Button(2, pin_factory=factory3)
button_2 = Button(2, pin_factory=factory4)

led.source = all_values(button_1, button_2)

pause()
