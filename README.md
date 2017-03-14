## pyBoard_LED_stimulator

Full-field LED stimulator running on the pyBoard using MicroPython.

![Test](https://github.com/teuler/pyBoard_LED_stimulator/blob/master/pictures/2017-03-11 09.04.15.jpg)

First test version, with 4 LEDs connected to pins X1 to X4, a synchronization signal ("trigger") provided at pin Y11, and a fast, external "blanking" signal (high == LEDs off) received at pin Y10.

### Release Notes

* 2017-03-10 - First test version
  Tested with a 500 Hz (0.4 ms off-time) blanking signal provided by an Arduino: With the current code, the blanking is not reliable;
  the LEDs are blanked for longer periods at irregular intervals. Possibly due to the garbage collector running in the background.
  Turning off garbage collection caused memory problems; these can probably be addressed by removing all dynamic memory allocations, but 
  this also removes advantages of using Python (vs. for example C on an Arduino).
  
  ![](https://github.com/teuler/pyBoard_LED_stimulator/blob/master/pictures/2017-03-11 09.02.55.jpg)
