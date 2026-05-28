import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

class Translator_api:
    __instance = None

    def __init__(self):
        if Translator_api.__instance is None:
            load_dotenv()
            self.__my_api_key = os.getenv("GEMINI_API_KEY")
            self.__client = genai.Client(api_key=self.__my_api_key )
            self.__MODELS = [
        "gemini-3.5-flash", 
        "gemini-2.5-flash", 
        "gemini-2.5-pro", 
        "gemini-2-flash", 
        "gemini-2-flash-lite"
    ]
            #init stuff here
            Translator_api.__instance = self
        else:
            raise Exception("Translator_api can't be initiated twice!")

    @staticmethod
    def get_instance():
        if Translator_api.__instance is None:
            Translator_api.__instance = Translator_api()
        return Translator_api.__instance   

    def translate(self, korean_text: str):
        if not isinstance(korean_text, str):
            raise TypeError(f"Expected a string, but got {type(korean_text).__name__}")
        
        # Try each model until one succeeds
        for model_name in self.__MODELS:
            try:
                response = self.__client.models.generate_content(
                    model=model_name,
                    contents=f"Translate this ocr extracted manhwa text to Thai, maintaining format for image for line just say line1: thai(next line) line 2:thai like this \n {korean_text}",
                )
                return response.text
            
            except APIError as e:
                pass
        
        return "All models failed to generate a response."