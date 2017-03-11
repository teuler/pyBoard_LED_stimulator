# ----------------------------------------------------------------------------
# led_stim
#
# ----------------------------------------------------------------------------
import micropython
import pyb

micropython.alloc_emergency_exception_buf(100)

MAX_LEDS       = 4
LED_TIMER      = 2
LED_TIMER_FREQ = 10000

# ----------------------------------------------------------------------------
  
# ----------------------------------------------------------------------------
class LEDs():
   def __init__(self, _blank, _freq=LED_TIMER_FREQ, _timer=LED_TIMER):
      # Setup timer for LEDs
      #
      self.timerFreq_Hz = _freq *2.0
      self.timerIndex   = _timer
      self.iMinInt      = []
      self.iMaxInt      = []
      self.iRangeInt    = []
      self.fMinInt      = []
      self.fMaxInt      = []
      self.fRangeInt    = []
      self.LEDs         = []
      self.names        = [] 
      self.currInt      = []
      self.pinIn_blank  = _blank
      self.isBlank      = False
      self.iLED         = 0
      self.LEDTimer     = pyb.Timer(self.timerIndex, freq=self.timerFreq_Hz, 
                                    mode=pyb.Timer.CENTER)

   
   def addLED(self, _name, _pin, _timerChan, _min=0, _max=255):
      # Add an LED if not maximum reached
      #
      if len(self.LEDs) < MAX_LEDS:
         # Define scaling and range
         #
         self.names.append(_name)
         self.iMinInt.append(_min)
         self.iMaxInt.append(_max)
         self.iRangeInt.append(_max -_min)
         self.fMinInt.append(_min/255.0)
         self.fMaxInt.append(_max/255.0)
         self.fRangeInt.append(_max/255.0 -_min/255.0)         
         self.currInt.append(0)
         
         # Setup timer channel
         #
         self.LEDs.append(self.LEDTimer.channel(_timerChan, pyb.Timer.PWM, 
                          pin=_pin, pulse_width=0))

         print("LED #{0}='{1}', range {2}..{3}"
               .format(len(self.LEDs), _name, _min, _max))
         return 0
      else:
         return -1


   def ready(self):          
      self.intr_Blank   = pyb.ExtInt(self.pinIn_blank, pyb.ExtInt.IRQ_RISING_FALLING, 
                                     pyb.Pin.PULL_UP, self.callbackBlank)
         
         
   def setIntensities(self, _intensities):
      # Set LED intensities
      #
      for iLED, intensity in enumerate(_intensities):
         self.currInt[iLED] = (intensity *self.fRangeInt[iLED] +self.fMinInt[iLED]) *100.0
         if not self.isBlank:
            self.LEDs[iLED].pulse_width_percent(self.currInt[iLED])


   def off(self):
      # Turn LEDs off
      #
      for LED in self.LEDs:
         LED.pulse_width_percent(0)
         
         
   def callbackBlank (self, _line):
      self.isBlank = self.pinIn_blank.value()
      iLED = 0
      while iLED < len(self.LEDs):
         if self.isBlank:
            self.LEDs[iLED].pulse_width_percent(self.currInt[iLED])
         else:
            self.LEDs[iLED].pulse_width_percent(0)
         iLED += 1
                                                   
# ----------------------------------------------------------------------------
