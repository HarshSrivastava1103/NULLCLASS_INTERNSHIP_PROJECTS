import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pytesseract
from PIL import Image
from googletrans import Translator
import cv2

class TextExtractorTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Extractor and Translator")
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
        upload_button = ttk.Button(main_frame, text="Upload Image/Video", command=self.upload_file)
        upload_button.grid(row=0, column=0, pady=20)
        
        # Output section
        ttk.Label(main_frame, text="Extracted Text:", style='TLabel').grid(row=1, column=0, sticky=tk.W)
        self.extracted_text = tk.Text(main_frame, height=5, width=50)
        self.extracted_text.grid(row=2, column=0, pady=5)
        
        ttk.Label(main_frame, text="Translated Text:", style='TLabel').grid(row=3, column=0, sticky=tk.W)
        self.translated_text = tk.Text(main_frame, height=5, width=50)
        self.translated_text.grid(row=4, column=0, pady=5)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg"), ("Videos", "*.mp4;*.avi")])
        if file_path:
            self.process_file(file_path)

    def process_file(self, file_path):
        # Check if the file is an image
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            self.extract_text_from_image(file_path)
        # Check if the file is a video
        elif file_path.lower().endswith(('.mp4', '.avi')):
            self.extract_text_from_video(file_path)
        else:
            messagebox.showerror("Error", "Unsupported file format")

    def extract_text_from_image(self, image_path):
        # Load image and use pytesseract to extract text
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        self.display_results(text)

    def extract_text_from_video(self, video_path):
        # Use OpenCV to extract frames from the video
        cap = cv2.VideoCapture(video_path)
        success, frame = cap.read()
        while success:
            text = pytesseract.image_to_string(frame)
            if text:  # Break on first valid extraction
                self.display_results(text)
                break
            success, frame = cap.read()
        cap.release()

    def display_results(self, text):
        self.extracted_text.delete(1.0, tk.END)
        self.extracted_text.insert(tk.END, text)

        # Translate only if the text is in English
        if text.strip():  # Check if text is not empty
            translated_text = self.translator.translate(text, dest='hi').text  # Change 'hi' to desired language
            self.translated_text.delete(1.0, tk.END)
            self.translated_text.insert(tk.END, translated_text)
        else:
            messagebox.showinfo("Info", "No text extracted.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextExtractorTranslator(root)
    root.mainloop()
