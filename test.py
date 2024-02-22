from tkinter import filedialog
from tkinter import *
import os
import pygame


# Initialize Tkinter
root = Tk()
root.title('Music Player')
root.geometry("570x440")  # Increased the height for the progress bar
root.configure(bg="black")

# Initialize Pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

menubar = Menu(root)
root.config(menu=menubar)
songs = []
current_song_index = 0
paused = False
timer_running = False  # Variable to track whether the timer is running or not
is_looping = False  # Variable to track whether looping is enabled or not

# Create a function to update the song list
def update_song_list():
    global current_song_index
    root.directory = filedialog.askdirectory()

    songs.clear()
    songlist.delete(0, END)

    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == '.mp3':
            songs.append(song)

    for song in songs:
        songlist.insert(END, song)

    current_song_index = 0

# Create a function to play the music
def play_music():
    global current_song_index, paused, timer_running

    if songs:
        try:
            if not paused:
                pygame.mixer.music.load(os.path.join(root.directory, songs[current_song_index]))
                if is_looping:
                    pygame.mixer.music.set_endevent(pygame.USEREVENT)
                else:
                    pygame.mixer.music.set_endevent(0)  # Disable looping event
                pygame.mixer.music.play()
                update_song_duration_label()
                if not timer_running:
                    update_current_time_label()
                    timer_running = True
            else:
                pygame.mixer.music.unpause()
                paused = False
        except pygame.error as e:
            print(f"Error playing {songs[current_song_index]}: {str(e)}")

# Create a function to pause the music
def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True

# Create a function to play the next song
def next_music():
    global current_song_index, paused, timer_running

    if songs:
        current_song_index = (current_song_index + 1) % len(songs)
        songlist.selection_clear(0, END)
        songlist.selection_set(current_song_index)
        play_music()
        if not timer_running:
            update_current_time_label()
            timer_running = True

# Create a function to play the previous song
def prev_music():
    global current_song_index, paused, timer_running

    if songs:
        current_song_index = (current_song_index - 1) % len(songs)
        songlist.selection_clear(0, END)
        songlist.selection_set(current_song_index)
        play_music()
        if not timer_running:
            update_current_time_label()
            timer_running = True

# Create a function to update the song duration label
def update_song_duration_label():
    if songs:
        song_path = os.path.join(root.directory, songs[current_song_index])
        
        
      
       
       
        

# Create a function to update the current time label
def update_current_time_label():
    global timer_running

    if songs and pygame.mixer.music.get_busy() and not paused:
        current_time = pygame.mixer.music.get_pos() // 1000
        song_slider.set(current_time)
        song_path = os.path.join(root.directory, songs[current_song_index])
       
       

        if current_time <= song_duration:
            minutes = current_time // 60
            seconds = current_time % 60
            formatted_time = f"{minutes:02}:{seconds:02}"
            current_time_label.config(text=formatted_time)
            root.after(1000, update_current_time_label)
        else:
            current_time_label.config(text="")
            timer_running = False
    else:
        current_time_label.config(text="")
        timer_running = False

# Create a function to handle slider movement
def on_slider_move(val):
    if songs and not paused:
        pygame.mixer.music.set_pos(int(song_slider.get()) / song_slider.cget("to"))

# Create a function to handle slider release
def on_slider_release(event):
    if songs and not paused:
        new_position = int(song_slider.get())
        pygame.mixer.music.set_pos(new_position / song_slider.cget("to"))


# Create a function to play the next song when the current song ends
def play_next_song(event):
    next_music()

# Bind the event handler to the song end event
root.bind(pygame.USEREVENT, play_next_song)

# Create the "Organize" menu
organise_menu = Menu(menubar, tearoff=False)
organise_menu.add_command(label='Select Folder', command=update_song_list)
menubar.add_cascade(label='Organize', menu=organise_menu)

# Create the song list
songlist = Listbox(root, bg="black", fg="white", width=70, height=15)
songlist.pack(pady=10)

# Create button images
next_btn_img = PhotoImage(file="next.png")
play_btn_img = PhotoImage(file="play.png")
prev_btn_img = PhotoImage(file="previous.png")
pause_btn_img = PhotoImage(file="pause.png")

# Create the control frame
control_frame = Frame(root, bg="black")
control_frame.pack()

# Place the buttons in the control_frame
prev_btn = Button(control_frame, image=prev_btn_img, borderwidth=0, command=prev_music)
play_btn = Button(control_frame, image=play_btn_img, borderwidth=0, command=play_music)
pause_btn = Button(control_frame, image=pause_btn_img, borderwidth=0, command=pause_music)
next_btn = Button(control_frame, image=next_btn_img, borderwidth=0, command=next_music)


prev_btn.grid(row=0, column=0, padx=7)
play_btn.grid(row=0, column=1, padx=7)
pause_btn.grid(row=0, column=2, padx=7)
next_btn.grid(row=0, column=3, padx=7)


# Create the label frame for time and duration
label_frame = Frame(root, bg="black")
label_frame.pack()

# Create labels for displaying current time and song duration
current_time_label = Label(label_frame, text="", bg="black", fg="white", font=("Arial", 14))
song_duration_label = Label(label_frame, text="", bg="black", fg="white", font=("Arial", 14))

# Create a progress bar (slider) for the playback position
song_slider = Scale(label_frame, from_=0, to=100, orient=HORIZONTAL, length=400, showvalue=0, bg="black", fg="white", troughcolor="gray")
song_slider.set(0)  # Initialize the slider position to 0
song_slider.bind("<ButtonRelease-1>", on_slider_release)  # Bind release event to seek function

# Pack the labels and progress bar within the label_frame
current_time_label.pack(side=LEFT, padx=10)
song_slider.pack(side=LEFT, padx=10)
song_duration_label.pack(side=LEFT, padx=10)

root.mainloop()
