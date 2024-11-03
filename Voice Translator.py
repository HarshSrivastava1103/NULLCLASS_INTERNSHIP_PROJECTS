import tkinter as tk
from tkinter import messagebox, ttk
import speech_recognition as sr
from googletrans import Translator
import datetime
import threading
import time

class VoiceTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Translator (English to Hindi)")
        self.root.geometry("600x400")
        
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
        self.is_listening = False
        
        self.setup_gui()
        
    def setup_gui(self):
        style = ttk.Style()
        style.configure('TButton', padding=6, font=('Helvetica', 10))
        style.configure('TLabel', font=('Helvetica', 12))
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(main_frame, text="English:").grid(row=1, column=0, sticky=tk.W)
        self.english_text = tk.Text(main_frame, height=5, width=50)
        self.english_text.grid(row=2, column=0, columnspan=2, pady=5)
        
        ttk.Label(main_frame, text="हिंदी:").grid(row=3, column=0, sticky=tk.W)
        self.hindi_text = tk.Text(main_frame, height=5, width=50)
        self.hindi_text.grid(row=4, column=0, columnspan=2, pady=5)
        
        self.start_button = ttk.Button(main_frame, text="Start Listening", command=self.toggle_listening)
        self.start_button.grid(row=5, column=0, pady=20, padx=5)
        
        clear_button = ttk.Button(main_frame, text="Clear", command=self.clear_text)
        clear_button.grid(row=5, column=1, pady=20, padx=5)
        
        self.time_var = tk.StringVar()
        time_label = ttk.Label(main_frame, textvariable=self.time_var)
        time_label.grid(row=6, column=0, columnspan=2)
        
        self.update_time()
        
    def update_time(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.time_var.set(f"Current Time: {current_time}")
        
        current = datetime.datetime.now().time()
        start_time = datetime.time(21, 30)
        end_time = datetime.time(22, 0)
        
        if not (start_time <= current <= end_time):
            if self.is_listening:
                self.toggle_listening()
            self.status_var.set("Taking rest, see you tomorrow!")
            self.start_button.state(['disabled'])
        else:
            self.start_button.state(['!disabled'])
        
        self.root.after(1000, self.update_time)
    
    def toggle_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.start_button.configure(text="Stop Listening")
            self.status_var.set("Listening...")
            threading.Thread(target=self.listen_and_translate, daemon=True).start()
        else:
            self.is_listening = False
            self.start_button.configure(text="Start Listening")
            self.status_var.set("Stopped")
    
    def listen_and_translate(self):
        while self.is_listening:
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=5)
                    
                try:
                    text = self.recognizer.recognize_google(audio)
                    self.english_text.insert(tk.END, text + "\n")
                    self.english_text.see(tk.END)
                    
                    hindi_translation = self.translator.translate(text, src='en', dest='hi').text
                    self.hindi_text.insert(tk.END, hindi_translation + "\n")
                    self.hindi_text.see(tk.END)
                    
                except sr.UnknownValueError:
                    self.status_var.set("Could not understand audio. Please repeat.")
                    time.sleep(2)
                    self.status_var.set("Listening...")
                    
                except sr.RequestError:
                    messagebox.showerror("Error", "Check your internet connection.")
                    self.toggle_listening()
                    
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
                self.toggle_listening()
    
    def clear_text(self):
        self.english_text.delete(1.0, tk.END)
        self.hindi_text.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceTranslator(root)
    root.mainloop()
