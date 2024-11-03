import speech_recognition as sr
from langdetect import detect
from googletrans import Translator
import pyttsx3
import threading
import queue
import time
from datetime import datetime
import logging

class EnhancedVoiceTranslator:
    def __init__(self):
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename=f'translation_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        )
        
        # Initialize components
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        
        # Set up audio properties
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 4000
        self.recognizer.pause_threshold = 0.8
        
        # Initialize queues for async processing
        self.audio_queue = queue.Queue()
        self.translation_queue = queue.Queue()
        
        # Control flags
        self.is_running = True
        self.is_processing = False
        
        # Cache for recent translations
        self.translation_cache = {}
        
    def setup_microphone(self):
        """Configure microphone with noise reduction"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                logging.info("Microphone calibrated for ambient noise")
        except Exception as e:
            logging.error(f"Microphone setup failed: {str(e)}")
            raise
            
    def recognize_speech(self):
        """Enhanced speech recognition with error handling"""
        try:
            with sr.Microphone() as source:
                print("\nListening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                try:
                    text = self.recognizer.recognize_google(audio)
                    logging.info(f"Successfully recognized speech: {text}")
                    return text
                except sr.UnknownValueError:
                    print("Could not understand the audio")
                    logging.warning("Speech recognition failed: UnknownValueError")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                    logging.error(f"Speech recognition request failed: {str(e)}")
                    
        except Exception as e:
            logging.error(f"Error in speech recognition: {str(e)}")
        return None
        
    def detect_and_translate(self, text):
        """Detect language and translate with caching"""
        try:
            # Check cache first
            cache_key = f"{text}"
            if cache_key in self.translation_cache:
                return self.translation_cache[cache_key]
            
            lang = detect(text)
            if lang not in ['en', 'es']:
                print(f"Unsupported language detected: {lang}")
                return None, None, None
                
            target_lang = 'es' if lang == 'en' else 'en'
            translation = self.translator.translate(text, dest=target_lang)
            
            # Cache the result
            result = (lang, translation.text, target_lang)
            self.translation_cache[cache_key] = result
            
            return result
            
        except Exception as e:
            logging.error(f"Translation error: {str(e)}")
            return None, None, None
            
    def speak_text(self, text, lang):
        """Improved text-to-speech with voice selection"""
        try:
            # Select appropriate voice
            voice_idx = 1 if lang == 'es' else 0
            if voice_idx < len(self.voices):
                self.engine.setProperty('voice', self.voices[voice_idx].id)
            else:
                logging.warning(f"Voice for language {lang} not found, using default")
                
            self.engine.say(text)
            self.engine.runAndWait()
            
        except Exception as e:
            logging.error(f"Text-to-speech error: {str(e)}")
            
    def process_translation(self):
        """Process translations in a separate thread"""
        while self.is_running:
            try:
                if not self.translation_queue.empty():
                    text = self.translation_queue.get()
                    source_lang, translated_text, target_lang = self.detect_and_translate(text)
                    
                    if all((source_lang, translated_text, target_lang)):
                        print(f"\n{source_lang.upper()} detected: {text}")
                        print(f"Translated to {target_lang.upper()}: {translated_text}")
                        self.speak_text(translated_text, target_lang)
                        
            except Exception as e:
                logging.error(f"Translation processing error: {str(e)}")
            time.sleep(0.1)
                
    def run(self):
        """Main execution loop with improved control flow"""
        try:
            print("Setting up microphone and calibrating...")
            self.setup_microphone()
            
            # Start translation processing thread
            translation_thread = threading.Thread(target=self.process_translation)
            translation_thread.start()
            
            print("\nReady for conversation! (Press Ctrl+C to exit)")
            self.is_processing = True
            
            while self.is_running:
                speech_input = self.recognize_speech()
                if speech_input:
                    self.translation_queue.put(speech_input)
                    
        except KeyboardInterrupt:
            print("\nStopping translation service...")
        except Exception as e:
            logging.error(f"Runtime error: {str(e)}")
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Clean shutdown of resources"""
        self.is_running = False
        self.is_processing = False
        self.engine.stop()
        logging.info("Translation service stopped")

def main():
    translator = EnhancedVoiceTranslator()
    translator.run()

if __name__ == "__main__":
    main()