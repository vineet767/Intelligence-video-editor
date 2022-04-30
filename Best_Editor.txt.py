import vlc
import ctypes
from ctypes.util import find_library
import sys
import cv2
import math
from tkinter import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
if sys.version_info[0] < 3:
    import Tkinter as Tk
    from Tkinter import ttk
    from Tkinter.filedialog import askopenfilename
else:
    import tkinter as Tk
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename
import os
import pathlib
from threading import Thread, Event
import time
import platform
start_time = 0
end_time = 0
filename_store= ''
saved_dir = ''
filename = ''
v1 = ''
v2 = ''


def maximum(a,b):
    if(a>=b):
        return a
    else:
        return b
    
def mspf(mp):
    return mp.get_fps()


def set_val(val):
	v1=val

class ttkTimer(Thread):
    def __init__(self, callback, tick):
        Thread.__init__(self)
        self.callback = callback
        self.stopFlag = Event()
        self.tick = tick
        self.iters = 0
    def run(self):
        while not self.stopFlag.wait(self.tick):
            self.iters += self.tick
            self.callback()
    def stop(self):
        self.stopFlag.set()
    def get(self):
        return self.iters


    
global index
index=0
class Player(Tk.Frame):
    def __init__(self, parent, title=None):
        global index,v2,v1
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        if title == None:
            title = "Intelligent Video Editor"
        self.parent.title(title)
        menubar = Tk.Menu(self.parent)
        self.parent.config(menu=menubar)
        fileMenu = Tk.Menu(menubar)
        fileMenu.add_command(label="Open", underline=0, command=self.OnOpen)
        fileMenu.add_command(label="Exit", underline=1, command=_quit)
        menubar.add_cascade(label="File", menu=fileMenu)
        self.player = None
        self.videopanel = ttk.Frame(self.parent)
        self.canvas = Tk.Canvas(self.videopanel).pack(fill=Tk.BOTH,expand=1)
        self.videopanel.pack(fill=Tk.BOTH,expand=1)
        ctrlpanel = ttk.Frame(self.parent)
        
        ctrlpanel1 = ttk.Frame(self.parent)
        ctrlpanel3 = ttk.Frame(self.parent)
        ctrlpanel2=ttk.Frame(self.parent)
        



       
        self.scale_var = Tk.DoubleVar()
        self.timeslider_last_val = ""
        self.timeslider = Tk.Scale(ctrlpanel, variable=self.scale_var, width=1.5,command=self.scale_sel,from_=0, to=1000, orient=Tk.HORIZONTAL, length=880)
        self.timeslider.pack(side=Tk.TOP, fill=Tk.X,expand=1)
        self.timeslider_last_update = time.time()


        

        #ttk.Style().configure('TButton',foreground="green",background="black");
        pause  = Tk.Button(ctrlpanel,background="red",width=10, text="Pause",relief=RAISED, command=self.OnPause)
        saveVideo  = Tk.Button(ctrlpanel,bg="cyan",fg="green",width=10, text="Screenshot",relief=SUNKEN, command=self.saveVideo)
        plus5  = Tk.Button(ctrlpanel, bg="blue",fg="black",width=10,text="plus5",relief=SUNKEN, command=self.plus5)
        minus5  = Tk.Button(ctrlpanel,bg="violet",fg="black",width=10, text="minus5",relief=SUNKEN, command=self.minus5)
        play   = Tk.Button(ctrlpanel,bg="green",fg="yellow",width=10, text="Play",relief=RAISED, command=self.OnPlay)
        stop   = Tk.Button(ctrlpanel,bg="violet",fg="black", width=10,text="Stop",relief=SUNKEN, command=self.OnStop)
        Clip_Start = Tk.Button(ctrlpanel,bg="turquoise",fg="black", width=10,text="Start Clip",relief=SUNKEN, command=self.OnClipStart)
        Clip_Stop = Tk.Button(ctrlpanel,bg="IndianRed1",fg="black",width=10, text="End Clip", relief=RAISED,command=self.OnClipStop)
        Clip_Save = Tk.Button(ctrlpanel,bg="DarkOliveGreen1",fg="black",width=10, text="Save Clip",relief=RAISED, command=self.OnClipSave)
        extraButton = Tk.Button(ctrlpanel,bg="black",fg="red", text="|||",relief=RAISED)


        v1 = StringVar()
        v2 = StringVar()

        S_Time = Entry(ctrlpanel3, textvariable=v1, width=9)
        S_Time.pack(side=LEFT,anchor=W)
        

        E_Time = Entry(ctrlpanel3, textvariable=v2, width=9)
        E_Time.pack(side=LEFT)
        
       
        max_lbl = Label(ctrlpanel3, text="Min").pack(side=LEFT,padx=(80,0))





        self.volume_var = Tk.IntVar()
        self.volslider = Tk.Scale(ctrlpanel3, variable=self.volume_var,width=1.5, command=self.volume_sel,from_=0, to=100, orient=Tk.HORIZONTAL, length=200)
        self.volslider.pack(side=LEFT)


        min_lbl = Label(ctrlpanel3, text="Max").pack(side=LEFT)
        
        












    
        global filename_store,directory_store,fullname
        
        textBox=Text(ctrlpanel3, height=1, width=10)
        textBox.pack(side=LEFT,padx=(130,10))
        
        text_buttonAdd = Button(ctrlpanel3, height=1, width=9,fg="red",bg="green yellow", text="Add button", command=lambda:[ttk.Button(ctrlpanel2, text=textBox.get("1.0","end-1c"), 
                command=lambda dummy=textBox.get("1.0","end-1c"): self.click_event(dummy)).pack(side="left"),os.mkdir(directory_store+'/'+textBox.get("1.0","end-1c"))])
        text_buttonAdd.pack(side="left",padx=(0,40))
        

        Clip_Start.pack(side=Tk.LEFT)
        Clip_Stop.pack(side=Tk.LEFT)
        minus5.pack(side=Tk.LEFT)
        play.pack(side=Tk.LEFT)
        plus5.pack(side=Tk.LEFT)
        pause.pack(side=Tk.LEFT)
        saveVideo.pack(side=Tk.LEFT)
        Clip_Save.pack(side=Tk.LEFT)
        stop.pack(side=Tk.LEFT)
        extraButton.pack(side=Tk.LEFT)
        
        Clip_Save.pack(side=Tk.LEFT)
       
       
        
        ctrlpanel2.pack(side=Tk.BOTTOM)
        ctrlpanel3.pack(side=Tk.BOTTOM)
        ctrlpanel.pack(side=Tk.BOTTOM)
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        self.timer = ttkTimer(self.OnTimer, 1.0)
        self.timer.start()
        self.parent.update()
    
    def click_event(self,text):
        print('click event')
        global filename_store,directory_store
        tyme = self.player.get_time()
        tyme=tyme*0.001
        ffmpeg_extract_subclip(filename_store,tyme,tyme+5, targetname=directory_store+"/"+text+"/"+str(tyme)+".mp4")
        print('video saved')
        
    def set_string(self,text,number):
        global string1,string2,string3,string4,string5
        if(number==1):
            string1=text
        elif(number==2):
            string2=text
        elif(number==3):
            string3=text
        elif(number==4):
            string4=text
        elif(number==5):
            string5=text

    def OnExit(self, evt):
        self.Close()


    def OnClipStart(self):
        global start_time,v1,v2
        length = self.player.get_length()
        dbl = length * 0.001
        self.timeslider.config(to=dbl)
        tyme = self.player.get_time()
        if tyme == -1:
            tyme = 0
        dbl = tyme * 0.001
        start_time = dbl
        v1.set(dbl)
        v2.set(' ')
        
        

    def OnClipSave(self):
         
         print("Start Time is :",start_time)
         print("End Time is : ",end_time)
         print("The Filename is: ",filename)
         print("The File source is : ",filename_store)
         ffmpeg_extract_subclip(filename_store, start_time, end_time, targetname="test.mp4")
         print("file saved")

    def OnClipStop(self):
        global end_time,v2
        length = self.player.get_length()
        dbl = length * 0.001
        self.timeslider.config(to=dbl)
        tyme = self.player.get_time()
        if tyme == -1:
            tyme = 0
        dbl = tyme * 0.001
        end_time = dbl
        v2.set(dbl)
        
        

    def OnOpen(self):
        global filename_store,directory_store,fullname,filename
        self.OnStop()
        p = pathlib.Path(os.path.expanduser("~"))
        fullname =  askopenfilename(initialdir = p, title = "choose your file",filetypes = (("all files","*.*"),("mp4 files","*.mp4")))
        print(fullname)
        if os.path.isfile(fullname):
            dirname  = os.path.dirname(fullname)
            filename = os.path.basename(fullname)
            print(dirname)
            print(filename)
            filename_store=str(dirname)+'/'+str(filename)
            directory_store=str(dirname)
            print(filename)
            self.Media = self.Instance.media_new(str(os.path.join(dirname, filename)))
            self.player.set_media(self.Media)
            if platform.system() == 'Windows':
                self.player.set_hwnd(self.GetHandle())
            else:
                self.player.set_xwindow(self.GetHandle())
            self.OnPlay()
            self.volslider.set(self.player.audio_get_volume())

    def OnPlay(self):
        if not self.player.get_media():
            self.OnOpen()
        else:
            if self.player.play() == -1:
                self.errorDialog("Unable to play.")

    def GetHandle(self):
        return self.videopanel.winfo_id()

    def plus5(self):
        global index
        print('index : ' ,index)
        self.player.pause()
        new_time = 25*5 * mspf(self.player)
        self.player.set_time(math.ceil(self.player.get_time()+new_time))
        print('no of frames : ',mspf(self.player))
        self.player.play()
        
    def minus5(self):
        self.player.pause()
        new_time = 25*6 * mspf(self.player)
        self.player.set_time(maximum(0,math.floor(self.player.get_time()-new_time)))
        print('no of frames : ',mspf(self.player))
        self.player.play()
        '''
    def saveVideo(self):
        global filename_store,directory_store
        tyme = self.player.get_time()
        tyme=tyme*0.001
        ffmpeg_extract_subclip(filename_store,tyme,tyme+5, targetname=directory_store+"/sss.mp4")
        print('video saved')'''
    
    def saveVideo(self):
        global fullname,directory_store
        print(directory_store)
        cap = cv2.VideoCapture(fullname) 
        fps = cap.get(cv2.CAP_PROP_FPS)
        print('fps:',fps)
        tyme = self.player.get_time()
        tyme=tyme*0.001
        frame_no=int(fps*tyme)
        print('frame_no',frame_no)
        cap.set(1,frame_no); # Where frame_no is the frame you want
        ret, frame = cap.read() # Read the frame
        cv2.imwrite(directory_store+'/'+str(tyme)+'.jpeg', frame)

    def OnPause(self):
        global filename_store
        print(filename_store)
        self.player.pause()

    def OnStop(self):
        self.player.stop()
        self.timeslider.set(0+100)

    def OnTimer(self):
        #global filename_store
        global index
    
        if self.player == None:
            return
        length = self.player.get_length()
        dbl = length * 0.001
        self.timeslider.config(to=dbl)
        tyme = self.player.get_time()
        if tyme == -1:
            tyme = 0
        dbl = tyme * 0.001
        print('player length : ',dbl)
        #print(filename_store)
        
        self.timeslider_last_val = ("%.0f" % dbl) + ".0"
        if time.time() > (self.timeslider_last_update + 2.0):
            self.timeslider.set(dbl)

    def scale_sel(self, evt):
        if self.player == None:
            return
        nval = self.scale_var.get()
        sval = str(nval)
        if self.timeslider_last_val != sval:
            self.timeslider_last_update = time.time()
            mval = "%.0f" % (nval * 1000)
            self.player.set_time(int(mval))


    def volume_sel(self, evt):
        if self.player == None:
            return
        volume = self.volume_var.get()
        if volume > 100:
            volume = 100
        if self.player.audio_set_volume(volume) == -1:
            self.errorDialog("Failed to set volume")

    def OnToggleVolume(self, evt):
        is_mute = self.player.audio_get_mute()
        self.player.audio_set_mute(not is_mute)
        self.volume_var.set(self.player.audio_get_volume())

    def OnSetVolume(self):
        if volume > 100:
            volume = 100
        if self.player.audio_set_volume(volume) == -1:
            self.errorDialog("Failed to set volume")

    def errorDialog(self, errormessage):
        Tk.tkMessageBox.showerror(self, 'Error', errormessage)

def Tk_get_root():
    if not hasattr(Tk_get_root, "root"):
        Tk_get_root.root= Tk.Tk()
    return Tk_get_root.root

def _quit():
    print("_quit: bye")
    root = Tk_get_root()
    root.quit()    
    root.destroy()
    os._exit(1)

if __name__ == "__main__":
    root = Tk_get_root()
    root.geometry("890x500")
    root.protocol("WM_DELETE_WINDOW", _quit)
    player = Player(root, title="tkinter vlc")
    root.mainloop()
