# code modified, tweaked and tailored from code by bertwert 
# on RPi forum thread topic 91796
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
 
# GPIO ports for the 7seg pins
segments =  (6,4,12,20,21,13,25,16)
# 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline
 
for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)
 
# GPIO ports for the digit 0-3 pins 
digits = (5,22,27,24)
# 7seg_digit_pins (12,9,8,6) digits 0-3 respectively
 
for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)
 
num = {' ':(0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,0,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,1,0,1,1)}


def UntilTheAlarm(hour, min):
    cur_hour = int(time.ctime()[11:13])    # Current hour
    cur_min = int(time.ctime()[14:16])      # Current min

    alarm_hour = hour  # Alarm setting hour
    alarm_min = min  # Alarm min

    ret_hour = alarm_hour
    ret_min = alarm_min

    # Calculation for convenience
    if(alarm_min < cur_min):
        ret_hour -= 1
        ret_min += (60-cur_min)
        if(ret_min > 59):
            temp = ret_min - 60
            ret_hour += 1
            ret_min = temp
    else:
        ret_min = alarm_min - cur_min

    # Calculation for convenience
    if(ret_hour > 12):
        ret_hour -= 12
    if(cur_hour > 12):
        cur_hour -= 12        
    ret_hour -= cur_hour    # Until the hour
    if(ret_hour < 0):
        ret_hour *= -1

    return ret_hour, ret_min



try:
    while True:
        hour, min = UntilTheAlarm(11, 56) 

        if(hour/10 <= 10):
            hour = "0"+str(hour)
        else:
            hour = str(hour)
        
        if(min/10 <= 0):
            min = "0"+str(min)
        else:
            min = str(min)

        n = str(hour)+str(min)
        s = str(n).rjust(4)
        for digit in range(4):
            for loop in range(0,7):
                GPIO.output(segments[loop], num[s[digit]][loop])
                if (int(time.ctime()[18:19])%2 == 0) and (digit == 1):
                    GPIO.output(16, 1)
                else:
                    GPIO.output(16, 0)
            GPIO.output(digits[digit], 0)
            time.sleep(0.001)
            GPIO.output(digits[digit], 1)
finally:
    GPIO.cleanup()