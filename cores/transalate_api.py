import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

class Translator_api:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Translator_api, cls).__new__(cls)
            load_dotenv()
            cls._instance.__my_api_key = os.getenv("GEMINI_API_KEY")
            cls._instance.__client = genai.Client(api_key=cls._instance.__my_api_key)
            cls._instance.__MODELS = [
                "gemini-3.5-flash", 
                "gemini-3.1-flash-lite",
                "gemini-3-flash",
                "gemini-2.5-flash", 
                "gemini-2.5-pro", 
                "gemini-2-flash", 
                "gemini-2-flash-lite"
            ]
        return cls._instance

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