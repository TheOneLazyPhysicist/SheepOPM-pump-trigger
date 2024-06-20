# Raspberry Pi Pico 1 (Envelope Generator)

from machine import Pin
import utime

# User-defined parameters
duty_cycle = 0.5  # User-defined duty cycle as a fraction (e.g., 0.1 for 10%)
overall_cycle_time_ms = 500  # User-defined overall cycle time in milliseconds (e.g., 500 ms)

# Global laser allowed/off
envelop = 1  # 0 = envelop generator off

envelopPin = 22
if not envelop:
    envelopPin = 21

if envelop == 1:
    # Calculate active time and inactive time based on user-defined duty cycle and overall cycle time
    active_time_ms = overall_cycle_time_ms * duty_cycle
    inactive_time_ms = overall_cycle_time_ms - active_time_ms

    # Initialize envelop control pin
    envelop_pin = Pin(envelopPin, Pin.OUT)

    while True:
        # Envelop active phase
        envelop_pin.value(1)  # Activate the laser
        utime.sleep_ms(int(active_time_ms))  # Keep the laser active for the specified time

        # Envelop inactive phase
        envelop_pin.value(0)  # Deactivate the envelop
        utime.sleep_ms(int(inactive_time_ms))  # Keep the laser inactive for the specified time
else:
    print(f"The envelop generator is off")
