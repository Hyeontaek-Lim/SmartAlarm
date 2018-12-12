from tkinter import *
from time import *
import RPi.GPIO as GPIO
import I2C_LCD_driver
import iot, tk,threading,rgb,time


GPIO.setmode(GPIO.BCM)
buzzer = 26
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# DATA var
hour = -1

minute = -1 
my_bus_title ="null"
my_bus_code = "null"
my_city ="null"
my_bus_name = "null"
bus_stop_data =""
mylcd = I2C_LCD_driver.lcd()
dust_data = "test"
bus_stop_data = "test"



def set_file():
    f = open('cache.txt','w')
    st = str(hour)+' '+ str(minute)+'\n'+my_bus_title+' '+str(my_bus_code)+' '+my_bus_name[:4]+'\n'+my_city
    f.writelines(st)
    f.close()
    
def set_lcd():
    mylcd.lcd_display_string(dust_data,1)
    mylcd.lcd_display_string(bus_stop_data,2)

def readText():
    while True:
        global hour, minute, my_bus_title,my_bus_code,my_city,my_bus_name, bus_stop_data,dust_data,bus_stop_data
        try:
            f = open('cache.txt','r')
            hour, minute = f.readline().split(' ')
            hour =  int(hour)
            minute = int(minute)
            my_bus_title, my_bus_code, my_bus_name = f.readline().split(' ')
            my_bus_name=my_bus_name[:4]
            my_city = f.readline()
            f.close()
        except:
            set_file()
        print(str(my_bus_code))
        print(my_bus_name)
        dust_data = iot.page_url_parse(my_city)
        if 'good' in dust_data:
            rgb.set_led(0,0,100)
        elif 'normal' in dust_data:
            rgb.set_led(0,100,0)

        elif 'bad' in dust_data:
            rgb.set_led(100,50,0)
        else:
            rgb.set_led(100,0,0)
        bus_stop_data = iot.get_time(my_bus_code, my_bus_name)
        
        print(str(my_bus_code), my_bus_name)
        set_lcd()
        sleep(60) # 60초마다 캐시파일의 최신정보를 읽어옴

def my_callback(self):
    global flag
    print('callback')
    flag = True
    sleep(200)
    

flag = False
t = threading.Thread(target=readText)
t.start()
GPIO.add_event_detect(13, GPIO.FALLING, callback=my_callback)
while True:
    t = time.ctime()
    
    
    t_hour = int(t[11:13])
    t_min = int(t[14:16])
    
    if t_hour != hour or t_min != minute:
        flag= False
    
    if ((t_hour == hour) and (t_min == minute)) and (flag == False):        
        GPIO.output(buzzer,True)
        sleep(0.1)
        GPIO.output(buzzer,False)
        sleep(0.1)