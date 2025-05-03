import speech_recognition as sr
from typing import Callable, Optional

class VoiceRecognition:
    def __init__(self, callback: Callable[[str], None]):
    
        # Initialize voice recognition system.callback: Function to call with recognized text
        self.recognizer = sr.Recognizer()
        self.callback = callback
        self.is_listening = False

    def listen(self) -> Optional[str]:
      
        # Listen to microphone input and attempt speech recognition.
        # Returns:
        #     str: Recognized text if successful, None otherwise
       
        self.is_listening = True
        try:
            with sr.Microphone() as source:
                self.callback("Listening...")
                
                # Adjust for ambient noise and set timeout
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.pause_threshold = 0.8
                
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                self.callback("Processing...")
                
                try:
                    text = self.recognizer.recognize_google(audio)
                    self.callback(f"Recognized: {text}")
                    return text
                except sr.UnknownValueError:
                    self.callback("Could not understand audio")
                except sr.RequestError as e:
                    self.callback(f"API unavailable: {str(e)}")
                    
        except Exception as e:
            self.callback(f"Error: {str(e)}")
        finally:
            self.is_listening = False
        return None

    def stop_listening(self):
        # Stop any active listening operation
        self.is_listening = False