#To drive a laser diode in pulsed manner after receiving an external trigger.


#Frequency limit : set by nop(). use more nop() for low frequency operation or for less each laser on time.
#If you want to reduce jitter. Just increase the irqTiming frequency.
#increasing smlaser frequency with nop() decreases the number of pulses in each cycle but also decreases jitter
#multiply N+3 for every N nop()
#in irqtiming you can comment out the trigger to run this code in internal trigger

externalTriggerActive = 1


# external laser trigger on pin 8


from machine import Pin, Timer
import time
import select
import sys
from rp2 import asm_pio, StateMachine

systemActive = 1 # init value: laser and heater off when uploading code

# global laser allowed/off
laser = 1 # 0 = laser off, 1 = laser on allowed (can be used for debugging)

laserPin = 20

modulation_frequency = int(input("Enter the modulation frequency in Hz: "))
#print("Press 0 to toggle the laser ON and OFF ")

# 1: external trigger , internal pulse duration
if externalTriggerActive == 1:
    @asm_pio(set_init=rp2.PIO.OUT_LOW)
    def laserPulse():
        wait(1,irq,1) #1 clock cycle consumed
        set(pins, 0) #1 clock cycle
        set(pins,1) #1 clock cycle
        nop() #1 clock cycle , to increase the clock cycle of the laser statemachine ,that makes each pulse narrower.
        nop()
        nop()
        nop()
    smLaser = StateMachine(0, laserPulse, set_base=Pin(laserPin), freq=7*modulation_frequency)
    
    @asm_pio()
    def irqTiming():
        wait(1,gpio,8) #comment this out to remove external trigger and run with internal clock
        irq(1) # laser
    smTiming = StateMachine(1, irqTiming, freq=125000000  ) ##Generates a irq every 10ns(icrease to decrease jitter)

    smLaser.active(1)
    smTiming.active(1)

###############################################
print("system is ON", )


