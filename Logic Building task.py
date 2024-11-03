import tkinter as tk
from tkinter import messagebox, ttk
from googletrans import Translator
import datetime

class LogicBuildingTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("English to Hindi Translator")
        self.root.geometry("600x400")
        
        self.translator = Translator()
        
        self.setup_gui()
        
    def setup_gui(self):
        # Style configuration
        style = ttk.Style()
        style.configure('TButton', padding=6, font=('Helvetica', 10))
        style.configure('TLabel', font=('Helvetica', 12))
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input section
        ttk.Label(main_frame, text="Enter English Word:", style='TLabel').grid(row=0, column=0, sticky=tk.W)
        self.input_text = tk.Entry(main_frame, width=50)
        self.input_text.grid(row=1, column=0, pady=10)
        
        translate_button = ttk.Button(main_frame, text="Translate", command=self.translate_text)
        translate_button.grid(row=1, column=1, padx=10)
        
        # Output section
        ttk.Label(main_frame, text="Translated Hindi:", style='TLabel').grid(row=2, column=0, sticky=tk.W)
        self.hindi_output = tk.Text(main_frame, height=3, width=50)
        self.hindi_output.grid(row=3, column=0, pady=5)

    def translate_text(self):
        text = self.input_text.get().strip().lower()
        
        # Check if the input starts with a vowel
        if text and text[0] in 'aeiou':
            current_time = datetime.datetime.now().time()
            start_time = datetime.time(21, 0)
            end_time = datetime.time(22, 0)
            
            if start_time <= current_time <= end_time:
                # Translate to Hindi
                hindi_translation = self.translator.translate(text, dest='hi').text
                self.hindi_output.delete(1.0, tk.END)
                self.hindi_output.insert(tk.END, hindi_translation)
            else:
                messagebox.showinfo("Time Error", "This word starts with a vowel. Please provide another word.")
        else:
            # Translate if it does not start with a vowel
            hindi_translation = self.translator.translate(text, dest='hi').text
            self.hindi_output.delete(1.0, tk.END)
            self.hindi_output.insert(tk.END, hindi_translation)

if __name__ == "__main__":
    root = tk.Tk()
    app = LogicBuildingTranslator(root)
    root.mainloop()
