import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(
        description =
'''     \t\t \033[36m \033[1m \033[4m $$$ CAPE ZERO PLUS $$$ \033[0m
        \033[93mPINMAP ON P9 HEADERS
        LDR 35
        LED 14
        NTC 33
        POT 38
        SSD { a:15 , b:16 , c:21 , d:23 , e:27 , f:13 , g:11 }
        Push Button 41 \033[0m

        \t\t\033[36m \033[1m\033[4m %%% Functions Desciption %%% \033[0m
        \033[93m1. CP.disp(VAL,L,d)
                to display on ssd
                VAL = index
                L = list
                d = delay time in sec

        2. CP.hi()
                displays HI on ssd

        3. CP.bye()
                displays BYE on ssd

        4. CP.adc(PIN)
                returns adc read for PIN
                PIN = CP.POT for POT
                    = CP.LDR for LDR
                    = CP.NTC for Thermistor

        5. CP.pwm(DC)
                set pwm duty cycle = DC on LED

        6. CP.sw()
                return switch read

        7. CP.led_toggle(delay)
                toggle LED with delay time = delay

        8. CP.led_state(ST)
                Switch ON LED when ST = 'ON' or 1
                Switch OFF LED when ST = 'OFF' or 0

        9. CP.led_sw()
                Toggles LED on switch press

        10. CP.cleanup()
                Cleanup GPIO pins
                Stops PWM       \033[0m''' ,
formatter_class=RawTextHelpFormatter)
args = parser.parse_args()


import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC
from time import sleep
import sys, signal

ADC.setup()

LED = "P9_14"
POT = "P9_38"
SW = "P9_41"
SSD = ['P9_15','P9_16','P9_21','P9_23','P9_27','P9_13','P9_11']
LDR = "P9_35"
NTC = "P9_33"

NUM = ['1111110','0110000','1101101','1111001','0110011','1011011','1011111'\
        ,'1110000','1111111','1111011','0000000']
HI = ['0110111','0110000']
BYE = ['1111111','0111011','1001111']

PWM.start(LED,0)
GPIO.setup(SW,GPIO.IN)
for i in range(7) :
        GPIO.setup(SSD[i],GPIO.OUT)

def disp(VAL=10,L = NUM, d = 0) :
        j = 0
        for i in L[VAL] :
                if i == '1' :
                        GPIO.output(SSD[j],GPIO.HIGH)
                else :
                        GPIO.output(SSD[j],GPIO.LOW)
                j += 1
        sleep(d)

def hi() :
        disp(0,HI)
        sleep(0.5)
        disp(1,HI)
        sleep(0.5)

def bye() :
        for i in range(3) :
                disp(i,BYE)
                sleep(0.5)

def adc(PIN) :
        return ADC.read(PIN)

def pwm(DC) :
        PWM.set_duty_cycle(LED,DC)

def sw():
        a = 1
        while not GPIO.input(SW) :
                a = 0
        return a

def led_toggle(delay):
        PWM.set_duty_cycle(LED,100)
        sleep(delay)
        PWM.set_duty_cycle(LED,0)
        sleep(delay)

def led_state(ST):
        if ST == 1 or ST == 'ON' :
                PWM.set_duty_cycle(LED,100)
        elif ST == 0 or ST == 'OFF':
                PWM.set_duty_cycle(LED,0)
        else :
                print "FU wrong state"

flag = False
def led_sw():
        global flag
        if sw() == 0:
                flag = not flag
                if flag :
                        PWM.set_duty_cycle(LED,100)

def cleanup() :
        GPIO.cleanup()
        PWM.stop(LED)
        print "Cleanup Done"


def handler(signal, frame):
        bye()
        GPIO.cleanup()
        PWM.stop(LED)
        PWM.cleanup()
        print "Cleanup"
        sys.exit(0)

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTSTP, handler)
signal.signal(signal.SIGTERM, handler)
