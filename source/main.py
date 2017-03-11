# --------------------------------------------
# Timing test 1
#
# --------------------------------------------
import math 
import micropython
import pyb
import gc
import led_stim

# Some definitions
#
TWO_PI         = math.pi *2.0

TRIG_LEN_MS    = const(50)
TRIG_LED_INDEX = const(1)
TRIG_OUT_PIN   = pyb.Pin.board.Y11

LED_COUNT      = const(4)
LED_PINS       = [pyb.Pin.board.X1, pyb.Pin.board.X2, pyb.Pin.board.X3, pyb.Pin.board.X4]
LED_CHANNELS   = [1, 2, 3, 4]
LED_TIMER      = const(2)
LED_TIMER_FREQ = const(10000)

RED            = const(0)
GREEN          = const(1)
BLUE           = const(2)
YELLOW         = const(3)

# --------------------------------------------
# Main 
# --------------------------------------------
# User input
#
sinFreq_Hz   = 1.0
trigFreq_Hz  = sinFreq_Hz

# Initializing hardware
# 
LED_trig     = pyb.LED(TRIG_LED_INDEX)
pinOut_trig  = pyb.Pin(TRIG_OUT_PIN, mode=pyb.Pin.OUT_PP)

LEDs         = led_stim.LEDs(_blank=pyb.Pin.board.Y10)
LEDs.addLED("red",    LED_PINS[RED],    LED_CHANNELS[RED])
LEDs.addLED("green",  LED_PINS[GREEN],  LED_CHANNELS[GREEN])
LEDs.addLED("blue",   LED_PINS[BLUE],   LED_CHANNELS[BLUE])
LEDs.addLED("yellow", LED_PINS[YELLOW], LED_CHANNELS[YELLOW])
LEDs.ready()

# Initializing variables
#
trigOn       = False
currInt      = [0.0]*LED_COUNT
trigPer_ms   = 1000 /trigFreq_Hz

# Main loop
#
try:
   t0_ms    = pyb.millis()
   tTrig_ms = t0_ms
   t_ms     = 0.0
   periode  = 0.0
       
   while True:
      t_ms = pyb.millis()

      if (t_ms % trigPer_ms) == 0:
         pinOut_trig.high()
         trigOn   = True
         tTrig_ms = t_ms
         LED_trig.on()
      if trigOn and (t_ms > (tTrig_ms +TRIG_LEN_MS)):
         pinOut_trig.low()
         trigOn   = False
         LED_trig.off()

      periode         = TWO_PI *t_ms/1000.0 *sinFreq_Hz
      currInt[RED]    = (math.sin(periode) +1.0) /2.0
      currInt[GREEN]  = (math.cos(periode) +1.0) /2.0      
      currInt[BLUE]   = currInt[RED]      
      currInt[YELLOW] = currInt[GREEN]      
      LEDs.setIntensities(currInt)
            
finally:
   LEDs.off()
   LED_trig.off()
    
# --------------------------------------------