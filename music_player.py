from tkinter import *
import customtkinter as ctk
from tkinter import messagebox,filedialog
from datetime import datetime
from PIL import Image,ImageTk
from pygame import *
import pygame
import time,os
from mutagen.mp3 import MP3

ctk.set_appearance_mode('system')
ctk.set_default_color_theme('dark-blue')

win=ctk.CTk()
#daclared colors
col1="#dce600"
col2="#000088"
col3="#fffff0"
col4="#000000"

win.config(fg_color=col2)
win.title("ESS Music Player")
scr_h=win.winfo_screenheight()
scr_w=win.winfo_screenwidth()

winwidth=900
winheight=550

x_cord=(scr_w/2)-(winwidth/2)
y_cord=(scr_h/2)-(winheight/2)

win.geometry("%dx%d+%d+%d"%(winwidth,winheight,x_cord,y_cord))
myicon=PhotoImage(file="icons/ESSMUSICPLAYER.png")
win.iconphoto(False,myicon)

#declare icons
iw=20 #width/height of the icons
essmusiclogo=Image.open("icons/ESSMUSICPLAYER1.png")
essmusiclogo=essmusiclogo.resize((150,150))
essmusiclogo=ImageTk.PhotoImage(essmusiclogo)
musicicon=Image.open("icons/music.png")
musicicon=musicicon.resize((20,20))
musicicon=ImageTk.PhotoImage(musicicon)
iconprev=Image.open("icons/previous.png")
iconprev=iconprev.resize((iw,iw))
iconprev=ImageTk.PhotoImage(iconprev)
iconnext=Image.open("icons/next.png")
iconnext=iconnext.resize((iw,iw))
iconnext=ImageTk.PhotoImage(iconnext)
iconplay=Image.open("icons/play.png")
iconplay=iconplay.resize((iw,iw))
iconplay=ImageTk.PhotoImage(iconplay)
iconstop=Image.open("icons/stop.png")
iconstop=iconstop.resize((iw,iw))
iconstop=ImageTk.PhotoImage(iconstop)
iconpause=Image.open("icons/pause.png")
iconpause=iconpause.resize((iw,iw))
iconpause=ImageTk.PhotoImage(iconpause)
iconaddv=Image.open("icons/add.png")
iconaddv=iconaddv.resize((iw,iw))
iconaddv=ImageTk.PhotoImage(iconaddv)
iconminusv=Image.open("icons/minus.png")
iconminusv=iconminusv.resize((iw,iw))
iconminusv=ImageTk.PhotoImage(iconminusv)
iconspeaker=Image.open("icons/speaker.png")
iconspeaker=iconspeaker.resize((iw,iw))
iconspeaker=ImageTk.PhotoImage(iconspeaker)
iconmute=Image.open("icons/mute.png")
iconmute=iconmute.resize((iw,iw))
iconmute=ImageTk.PhotoImage(iconmute)
iconresume=Image.open("icons/resume.png")
iconresume=iconresume.resize((iw,iw))
iconresume=ImageTk.PhotoImage(iconresume)

#----functions--------------------
cur_index=1
song_stop_status=1
#function to play music
def play_music():
    global cur_index,song_length,song_pos,song_stop_status
    song_stop_status=1
    current_song=musiclist.get(ACTIVE)
    lblcurrentmusic.configure(text=current_song)
    try:
        mixer.music.load(current_song)
        #song_pos=mixer.music.get_pos()
        mixer.music.play()
        song_mut=MP3(current_song)
        song_length=song_mut.info.length
        c_song_length=time.strftime('%H:%M:%S',time.gmtime(song_length))
        lblsong_length.configure(text=str(c_song_length))
        #display music length
        musicprogress.configure(to=song_length)
        
        song_position()
    except:
        next_music()
#get song position

def song_position():
    global song_length,song_pos,song_stop_status
    if song_stop_status==1:
        try:
            song_pos=mixer.music.get_pos()/1000
            c_song_pos=time.strftime('%H:%M:%S',time.gmtime(song_pos))
            lblprogress.configure(text=c_song_pos)
            musicprogress.set(song_pos)
            if int(song_pos)==int(song_length):
                next_music()
            lblprogress.after(200,song_position)
        except:
            pass
    else:
        musicprogress.set(0)
#play next music
def next_music():
    global cur_index
    musicprogress.set(0)#set music progress to zero
    prev_index=musiclist.curselection()
    for item in musiclist.curselection():
        cur_index=item+1
    musiclist.selection_clear(prev_index)
    musiclist.activate(cur_index)
    musiclist.selection_set(cur_index)
    play_music()

#play previous music
def previous_music():
    global cur_index
    musicprogress.set(0)
    prev_index=musiclist.curselection()
    for item in musiclist.curselection():
        cur_index=item-1
    musiclist.selection_clear(prev_index)
    musiclist.activate(cur_index)
    musiclist.selection_set(cur_index)
    play_music()

#pause mixer
def pause_music():
    mixer.music.pause()

#stop mixer to play music
def stop_playing():
    global song_stop_status
    if song_stop_status==1:
        song_stop_status=0
        mixer.music.set_pos(0)
        mixer.music.stop()
        song_pos=0
        c_song_pos=time.strftime("%H:%M:%S",time.gmtime(song_pos))
        lblprogress.configure(text=c_song_pos)
    else:
        messagebox.showinfo("Song message","song is stopped click play")
        song_stop_status=1
#resume from pause
def resume_music():
    try:
        mixer.music.unpause()
    except:
        play_music()

#set music volume position
current_volume=1 #volume is 1 that is 100%
speaker_status=1 #speaker set to unmute

# add volume
def add_volume():
    global current_volume
    if current_volume>1:
        pass
    else:
        btnspeaker.configure(image=iconspeaker)
        current_volume=current_volume+0.05
        mixer.music.set_volume(current_volume)

# reducing volume
def minus_volume():
    global current_volume
    if current_volume<=0:
        btnspeaker.configure(image=iconmute)
        pass
    else:
        btnspeaker.configure(image=iconspeaker)
        current_volume=current_volume-0.05
        mixer.music.set_volume(current_volume)

# muting speaker
def mute_speaker():
    global speaker_status,current_volume
    if speaker_status==1: #check if speaker is unmute if unmute mute change to speaker status to zero
        speaker_status=0
        btnspeaker.configure(image=iconmute)
        mixer.music.set_volume(0)
    elif speaker_status==0: # check is speaker is muted if muted to unmute
        speaker_status=1
        btnspeaker.configure(image=iconspeaker)
        mixer.music.set_volume(current_volume)

#loading music folder
def load_music():
    global songs
    clear_music()
    music_folder=filedialog.askdirectory(initialdir=user+"\\Music",title="Select Folder")
    os.chdir(music_folder)
    songs=os.listdir()
    def show1():
        for i in songs:
            if i.endswith(".mp3"):
                musiclist.insert(END,i)
            elif i.endswith(".ogg"):
                musiclist.insert(END,i)
    show1()

#clear music list
def clear_music():
    musiclist.delete(0,END)
    mixer.music.stop()

#search music in music list
def search_song():
    sstr=str(searchtext.get())
    if sstr=="":
        for i in songs:
            if i.endswith(".mp3"):
                musiclist.insert(END,i)
            elif i.endswith(".ogg"):
                musiclist.insert(END,i)
    else:
        musiclist.delete(0,END)
        filter_data=list()
        for item in songs:
            if item.find(sstr)>=0:
                filter_data.append(item)
        for i in filter_data:
            if i.endswith(".mp3"):
                musiclist.insert(END,i)
            elif i.endswith(".ogg"):
                musiclist.insert(END,i)
            #musiclist.insert(END,i)
        
        

#placing objects
frame1=ctk.CTkFrame(win,fg_color=col2)
frame1.pack(side=TOP,fill=BOTH,expand=1)
frame1_logohol=ctk.CTkFrame(frame1,fg_color=col4,corner_radius=0)
frame1_logohol.pack(side=LEFT,fill=BOTH,expand=1)
lblimage=ctk.CTkLabel(frame1_logohol,text="",image=essmusiclogo)
lblimage.pack(fill=BOTH,expand=1)
frame1_musichol=ctk.CTkFrame(frame1,width=400,corner_radius=0,fg_color=col2)
frame1_musichol.pack(side=LEFT,fill=BOTH,expand=1)
framesearch=ctk.CTkFrame(frame1_musichol,height=40,fg_color=col4,corner_radius=0)
framesearch.pack(side=TOP,fill=X)
lb=ctk.CTkLabel(framesearch,text="Search",text_color=col1,text_font=("times",12))
lb.grid(column=0,row=0,padx=(5,5),pady=(4,4))
searchtext=ctk.CTkEntry(framesearch,text_color=col4,fg_color=col3,width=200,height=30)
searchtext.grid(column=1,row=0,padx=(5,5),pady=(4,4))
btnsearch=ctk.CTkButton(framesearch,text="Search",fg_color=col2,text_color=col1,hover_color=col2,cursor="hand2",width=50,command=search_song)
btnsearch.grid(column=2,row=0,padx=(5,5),pady=(4,4))
framemusicholder=ctk.CTkFrame(frame1_musichol)
framemusicholder.pack(side=TOP,fill=BOTH,expand=1)
musiclist=Listbox(framemusicholder,fg=col3,bg=col2,selectbackground=col4,relief=SUNKEN,border=1)
musiclist.pack(fill=BOTH,side=LEFT,expand=True)
scrolly=ctk.CTkScrollbar(framemusicholder,width=15,command=musiclist.yview,fg_color=col4)
scrolly.pack(side=LEFT,fill=Y)
musiclist.configure(yscrollcommand=scrolly.set)
musiclist.focus()
framemscops=ctk.CTkFrame(frame1_musichol,height=40,fg_color=col4,corner_radius=0)
framemscops.pack(side=BOTTOM,fill=X)
btnloadmusic=ctk.CTkButton(framemscops,text="Load",image=musicicon,width=60,fg_color=col2,text_color=col1,hover_color=col2,cursor="hand2",command=load_music)
btnloadmusic.grid(column=0,row=0,padx=(20,10),pady=(5,5))
btnclearmusic=ctk.CTkButton(framemscops,text="clear",image=musicicon,width=60,fg_color=col2,text_color=col1,hover_color=col2,cursor="hand2",command=clear_music)
btnclearmusic.grid(column=1,row=0,padx=(10,10),pady=(5,5))


frame2=ctk.CTkFrame(win,fg_color=col2,height=120)
frame2.pack(side=TOP,fill=X)
lblcurrentmusic=ctk.CTkLabel(frame2,text="current music",text_color=col1)
lblcurrentmusic.pack(side=TOP,fill=X)
framemusicprogress=ctk.CTkFrame(frame2,fg_color=col2,corner_radius=0)
framemusicprogress.pack(side=TOP,fill=X)
lblprogress=ctk.CTkLabel(framemusicprogress,text_color=col1,text="0.0")
lblprogress.pack(side=LEFT,padx=(5,10))
musicprogress=ctk.CTkSlider(framemusicprogress,fg_color=col4,button_color=col1,from_=0,to=100)
musicprogress.pack(pady=(5,5),side=LEFT,fill=X,padx=(15,15),expand=1)
musicprogress.set(0)
lblsong_length=ctk.CTkLabel(framemusicprogress,text_color=col1,text="0.0")
lblsong_length.pack(side=RIGHT,padx=(5,10))
framemusicoperation=ctk.CTkFrame(frame2,fg_color=col2,corner_radius=0)
framemusicoperation.pack(side=TOP,fill=X,pady=(30,30))
frameforops=ctk.CTkFrame(framemusicoperation,fg_color=col2,corner_radius=0)
frameforops.pack(side=LEFT,padx=(30,30))
btnprev=ctk.CTkButton(frameforops,text="",image=iconprev,corner_radius=0,width=20,height=20,fg_color=col2,hover_color=col2,cursor="hand2",command=previous_music)
btnprev.grid(column=0,row=0,padx=(5,5),pady=(4,4))
btnplay=ctk.CTkButton(frameforops,text="",image=iconplay,corner_radius=0,width=20,height=20,fg_color=col2,hover_color=col2,cursor="hand2",command=play_music)
btnplay.grid(column=1,row=0,padx=(5,5),pady=(4,4))
btnnext=ctk.CTkButton(frameforops,text="",image=iconnext,corner_radius=0,width=20,height=20,fg_color=col2,hover_color=col2,cursor="hand2",command=next_music)
btnnext.grid(column=2,row=0,padx=(5,5),pady=(4,4))
btnpause=ctk.CTkButton(frameforops,text="",image=iconpause,corner_radius=0,width=20,height=20,fg_color=col2,hover_color=col2,cursor="hand2",command=pause_music)
btnpause.grid(column=3,row=0,padx=(5,5),pady=(4,4))
btnresume=ctk.CTkButton(frameforops,text="",image=iconresume,corner_radius=0,width=20,height=20,fg_color=col2,hover_color=col2,cursor="hand2",command=resume_music)
btnresume.grid(column=4,row=0,padx=(5,5),pady=(4,4))
btnstop=ctk.CTkButton(frameforops,text="",image=iconstop,corner_radius=0,width=20,height=20,fg_color=col2,hover_color=col2,cursor="hand2",command=stop_playing)
btnstop.grid(column=5,row=0,padx=(5,5),pady=(4,4))
frameforvol=ctk.CTkFrame(framemusicoperation,fg_color=col2,corner_radius=0)
frameforvol.pack(side=RIGHT,padx=(30,30))
btnminus=ctk.CTkButton(frameforvol,text="",image=iconminusv,corner_radius=0,width=20,height=20,fg_color=col2,hover_color=col2,cursor="hand2",command=minus_volume)
btnminus.grid(column=0,row=0,padx=(5,5),pady=(4,4))
btnspeaker=ctk.CTkButton(frameforvol,text="",image=iconspeaker,corner_radius=0,width=20,height=20,fg_color=col2,hover_color=col2,cursor="hand2",command=mute_speaker)
btnspeaker.grid(column=1,row=0,padx=(5,5),pady=(4,4))
btnadd=ctk.CTkButton(frameforvol,text="",image=iconaddv,corner_radius=0,width=20,height=20,fg_color=col2,hover_color=col2,cursor="hand2",command=add_volume)
btnadd.grid(column=2,row=0,padx=(5,5),pady=(4,4))
lblcompany=ctk.CTkLabel(frame2,text="Developed By: Eric software solutions",text_color=col1)
lblcompany.pack(side=BOTTOM)

#-----get system user---------
user=os.path.expanduser('~')
os.chdir(user+"\Music")
songs=os.listdir()
def showmusic():
    if songs:
        for i in songs:
            if i.endswith(".mp3"):
                musiclist.insert(END,i)
            elif i.endswith(".ogg"):
                musiclist.insert(END,i)
    else:
        messagebox.showwarning("No music in music folder")

#exit confirmation messsage
def exiting():
    extmsg=messagebox.askyesno("Exit message","Do you want to exit?")
    if extmsg==1:
        exit(0)
#show music in musiclist
showmusic()
#initialize pygame and mixer
pygame.init()
mixer.init()
music_state=StringVar()
music_state.set("choose1")
musiclist.activate(0)
musiclist.selection_set(0)

play_music()
win.protocol('WM_DELETE_WINDOW',exiting)
win.mainloop()
pygame.quit()