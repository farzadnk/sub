


 

import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
from subsai import SubsAI

class SubtitleApp:
    def __init__(self, master):
        self.master = master
        self.master.configure(bg='#0A131A')
        self.master.title("ReEdit")
        self.master.geometry("500x500")

        self.lable = tk.Label(
            text="Enter all paths into the App",
            bg="#0a111a",
            fg="#1dda93", 
            font="jura", 
            activebackground="#1dda93"
        )
        self.lable.pack(pady=15)

        # create two buttons for selecting input and output directories
        self.input_button = tk.Button(
            master, text="Videos Path",
            bg="#0a111a", 
            fg="#1dda93", 
            font="jura", 
            activebackground="#1dda93", 
            command=self.get_input_directory
        )
        self.input_button.pack(pady=10)
    

        self.output_button = tk.Button(
            master, text="Subtitle Path",   
            bg="#0a111a", 
            fg="#1dda93", 
            font="jura", 
            activebackground="#1dda93",
            command=self.get_output_directory
        )
        self.output_button.pack(pady=10)

        # create a Combobox for selecting model type
        self.model_options = ["tiny.en", "base.en", "medium.en", "large.en",]
        self.model_type_var = tk.StringVar()
        
        # create a new style for the Combobox
        self.style = ttk.Style()
        self.style.theme_create('custom_style', parent='alt', settings={
            'TCombobox': {
                'configure': {
                    'selectbackground': '#1dda93',
                    'fieldbackground': '#0a111a',
                    'background': '#0a111a',
                    'foreground': '#1dda93',
                    'arrowcolor': '#1dda93',
                    'bordercolor': '#ffffff',
                    'lightcolor': '#1dda93',
                    'darkcolor': '#1dda93',
                    
                }
            }
        })
        self.style.theme_use('custom_style')
        
        self.model_type_combobox = ttk.Combobox(
            master, textvariable=self.model_type_var, 
            values=self.model_options,state='readonly', style='custom_style.TCombobox')
        self.model_type_combobox.pack(pady=10)
        
        # create a button to start the subtitle creation process
        self.process_button = tk.Button(
            master, text="Start", 
            bg="#0a111a", 
            fg="#1dda93", 
            font="jura", 
            activebackground="#1dda93",
            command=self.create_subtitles
        )
        self.process_button.pack(pady=20)
        
        # initialize variables for input/output directories
        self.input_dir = ''
        self.output_dir = ''

    def get_input_directory(self):
        # open a dialog box to select the input directory
        self.input_dir = filedialog.askdirectory()
    
    def get_output_directory(self):
        # open a dialog box to select the output directory
        self.output_dir = filedialog.askdirectory()
    
    def get_output_directory2(self):
        # open a dialog box to select the output directory
        self.output_dir = filedialog.askdirectory()
    
    def create_subtitles(self):
        # if input/output directories are not selected, show an error message
        if not self.input_dir or not self.output_dir:
            messagebox.showerror("Error", "Please select input and output directories.")
            return
        
        # create a SubsAI object and load the model
        subs_ai = SubsAI()
        model_type = self.model_type_var.get()
        model = subs_ai.create_model('openai/whisper', {'model_type': model_type})
        
        # loop through all video files in the input directory
        for filename in os.listdir(self.input_dir):
            if filename.endswith('.mp4') or filename.endswith('.avi'):
                # get the full path of the current video file and determine the corresponding subtitle file path
                video_path = os.path.join(self.input_dir, filename)
                subtitle_path = os.path.join(self.output_dir, filename[:-4] + '.ass')
                
                # transcribe the current video file and save the subtitles to the corresponding subtitle file
                subs = subs_ai.transcribe(video_path, model)
                subs.save(subtitle_path)
        
        # show a success message when the process is complete
        messagebox.showinfo("Success", "Subtitles created successfully.",)
        
root = tk.Tk()
subtitle_app = SubtitleApp(root)
root.mainloop()


