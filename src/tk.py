from tkinter import *
from tkinter import messagebox
from time import *
import I2C_LCD_driver
import iot

hour = -1
minute = -1 
my_bus_title ="null"
my_bus_code = "null"
my_city ="null"
my_bus_name = "null"
bus_stop_data =""
mylcd = I2C_LCD_driver.lcd()

# output
dust_data = ""

def set_lcd():
    mylcd.lcd_display_string(dust_data,1)
    mylcd.lcd_display_string(bus_stop_data,2)

#mylcd.lcd_display_string(,1)

def call_bus():
    iot.get_time(my_bus_code, my_bus_name)
    
def call_finedust():
    iot.page_url_parse(my_city)

def set_file():
    f = open('cache.txt','w')
    st = str(hour)+' '+ str(minute)+'\n'+my_bus_title+' '+str(my_bus_code)+' '+my_bus_name[:4]+'\n'+my_city
    print(st)
    f.writelines(st)
    f.close()



def timer_setting():
    window=Toplevel()
    def bus_setting():
        global hour, minute
        a = data1.get()
        b = data2.get()
        try:
            a = int(a)
            b = int(b)
            if a <= 0 or a >= 24:
                a= 10/0
            elif b< 0 or b>=60:
                b = 10/0
            hour = a
            minute = b
            set_file()
        except:
            messagebox.showinfo("경고!", "잘못된 입력입니다..")
        window.destroy()

    
    # window = Tk()
    
    data1 = Entry(window)
    data1.insert(END, hour)
    data1.pack()
    data2 = Entry(window)
    data2.insert(END, minute)
    data2.pack()
    
    bt = Button(window, text="버스 설정", command=bus_setting)
    bt.pack()
    
def bus_setting():
    window=Toplevel()
    def bus_search():
        def submit():
            global my_bus_code,my_bus_title, my_bus_name, bus_stop_data
            my_bus_name =bus_name.get()
            print(my_bus_name)
            res =""
            # print("test")
            if CheckVar1.get() == 1:
                res = iot.get_time(str(bus_stops[0][2]),bus_name.get())
                my_bus_code = str(bus_stops[0][2])
                my_bus_title = data1.get()
            if CheckVar2.get() == 1:
                res = iot.get_time(str(bus_stops[1][2]), bus_name.get())
                my_bus_code = str(bus_stops[1][2])
                my_bus_title = data1.get()
            print(res)
            print(type(res))
            bus_stop_data = res
            set_lcd()
            set_file()
            window.destroy()
            

        bus_stops = iot.bus_data_code(data1.get())
        CheckVar1 = IntVar()
        CheckVar2 = IntVar()
        print(bus_stops)
        if bus_stops.count !=0:
            Checkbutton(window, text = bus_stops[0][0] + bus_stops[0][1], variable = CheckVar1,
                    onvalue = 1, offvalue = 0, height=2, width = 20).pack()
            Checkbutton(window, text = bus_stops[1][0] + bus_stops[1][1], variable = CheckVar2,
                onvalue = 1, offvalue = 0, height=2,width = 20).pack()
        Label(window, text='버스번호를 입력하세요').pack()
        bus_name=Entry(window)
        bus_name.pack()
        Button(window, text="완료", command=submit).pack()

    Label(window,text='정류장 검색').pack()
    
    data1 = Entry(window)
    data1.insert(END, my_bus_title)
    data1.pack()
    
    Button(window, text="버스 설정", command=bus_search).pack()

def fine_dust():
    city = ['서울','경기','인천','강원','세종','충북','충남','대전','경북','경남','대구','울산','부산','전북','전남','광주','제주']
    window=Toplevel()
    # for i in range(14):
    def submit():
        global my_city,dust_data
        my_city = var.get()
        set_file()
        dust_data = iot.page_url_parse(var.get())
        set_lcd()
        window.destroy()

    var = StringVar()
    for i in range(17):
        R1 = Radiobutton(window, text=city[i], variable=var, value=city[i])
        R1.pack()
    var.set('Not yet defined')

    Button(window, text="타이머 설정", command=submit).pack()

    label = Label(window)
    label.pack()

try:
    f = open('cache.txt','r')
    hour, minute = f.readline().split(' ')
    hour =  int(hour)
    minute = int(minute)
    my_bus_title, my_bus_code, my_bus_name = f.readline().split(' ')
    my_bus_name = my_bus_name[4:]
    my_city = f.readline()
    f.close()
except:
    set_file()

root = Tk()
root.title('IoT')
root.geometry("100x170")
root.resizable(False, False)
 
btn = Button(root, text="타이머 설정", command=timer_setting)
btn.grid(column=0,row=0)
btn = Button(root, text="버스 설정", command=bus_setting)
btn.grid(column=0,row=1)
btn = Button(root, text="날씨 설정", command=fine_dust)
btn.grid(column=0,row=2)

Label(root, text="알람 시간").grid(column=0,row=3)
alram = StringVar()
if hour == -1 or minute == -1:
    alram=Label(root, text="no alarm").grid(column=0,row=4)
else:
    alram=Label(root, text= str(hour)+"시"+str(minute)+"분").grid(column=0,row=4)

if my_bus_title == "null":
    Label(root, text="no bus setting").grid(column=0,row=5)

else:
    Label(root, text=my_bus_title).grid(column=0,row=5)
    
if my_city == "null":
    Label(root, text="no city setting").grid(column=0,row=6)
else:
    Label(root, text=my_city).grid(column=0,row=6)




def main():
    set_lcd()
    root.mainloop()
    

if __name__ == "__main__":
    main()