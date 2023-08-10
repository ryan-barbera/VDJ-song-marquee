import tkinter as tk
import time
import os
import random
from helpers import filehelper
from configparser import ConfigParser
from tinytag import TinyTag

#Variables used everywhere lol
root = tk.Tk()
svar = tk.StringVar()

# Load Config and config based variables
config = ConfigParser()
config.read('config.ini', encoding='utf-8')
config_main = config['main_section']
track_history_path = filehelper.get_latest_m3u(config_main.get('dj_history_path'))
delay = int(config_main.get('text_delay'))  
labl = tk.Label(root, textvariable=svar, height=10, bg=config_main.get('text_bg_color'), fg=config_main.get('text_fg_color'), font=(config_main.get('text_font'), int(config_main.get('text_size'))) )
root.geometry(config_main.get('window_size'))
persist_msg = config_main.get('persist_message')


#Function occurs every delay, moves text and changes text when needed
def shif():
    #In here have code to change msg when needed, IE check the current 
    global text
    global last_update_time
    global shift_time
    global count
    #global track_history_path
    
    #change msg when new song
    #if last_update_time != os.path.getmtime(track_history_path):
    #    shif.msg = set_text()
    #    last_update_time = os.path.getmtime(track_history_path)
    if count > shift_time:
        shif.msg = set_text()
        last_update_time = os.path.getmtime(track_history_path)
        count = 0
    #Change msg when 60 sec passes

    else:
        shif.msg = shif.msg[1:] + shif.msg[0]
        #print(count)
        count += 1
    
    
    
    svar.set(shif.msg)
    root.after(delay, shif)
    
def pick_random_line(filename):
    """Choose a line at random from the text file""" 
    with open(filename, 'r', encoding='utf-8') as file: 
        lines = file.readlines() 
        random_line = random.choice(lines) 
    return random_line.strip()
   
    
#Uses tags to assemble the text to be displayed
def get_track_text(tag,front_text):
    text = front_text
    
    if(tag.artist):
        text += ' ' + tag.artist + ' - '
    
    if(tag.title):
        text += ' ' + tag.title
    #Make sure the word remix only appears once
    #if(tag.remix):
        #text += ' (' + tag.title + 'Remix) '
    return text

#Chances text to display the current song, previous song, and a custom message
def set_text():
    #Get metadata of last two tracks
    current_track = TinyTag.get(filehelper.read_last_line(track_history_path).strip())
    previous_track = TinyTag.get(filehelper.read_second_to_last_line(track_history_path).strip())
    ctext = get_track_text(current_track,"Current Track: ") 
    #Make this a config flag?
    qtext = pick_random_line("quotes.txt")
    ptext = get_track_text(previous_track,"Previous Track: ")
    ttltext = pick_random_line("titles.txt")
    #text = ' // ' + persist_msg + ' // ' + ctext + ' // ' +  qtext + ' // '+  ptext
    #text = ' // ' +  ttltext +  ' // ' + persist_msg + ' // ' + ctext + ' // ' +  qtext 
    #text = ' // ' + ttltext + ' // ' + ctext + ' // ' +  qtext + ' // '+  ptext
    text = ' // ' + persist_msg + ' // ' + ttltext + ' // ' +  qtext 
    #rphrase = 'VAMOS // VAMOS'
    #text = rphrase + ' // ' + rphrase + ' // ' + rphrase + ' // ' + rphrase + ' // ' 
    return text
    

def main():    
    #Set Globals
    global last_update_time
    global quote_array
    global shift_time
    global count
    shift_time = 800
    count = 0
    last_update_time = os.path.getmtime(track_history_path)
    shif.msg = set_text()
    shif()
    labl.pack()
    
    root.mainloop()


if __name__ == "__main__":
    main()