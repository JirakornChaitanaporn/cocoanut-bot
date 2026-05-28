import cv2
import numpy as np
import easyocr
import urllib.request # Add this import at the top of your file

class KoreanOcr:
    __instance = None

    def __init__(self):
        if KoreanOcr.__instance is None:
            self.__reader = easyocr.Reader(['ko'])
            #init stuff here
            KoreanOcr.__instance = self
        else:
            raise Exception("KoreanOcr can't be initiated twice!")

    @staticmethod
    def get_instance():
        if KoreanOcr.__instance is None:
            KoreanOcr.__instance = KoreanOcr()
        return KoreanOcr.__instance   

    def make_text(self, image_url):
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            image_bytes = response.read()
            
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # 1. Grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 2. Noise Removal
        denoised = cv2.fastNlMeansDenoising(gray, h=10)

        # 3. Normalization (CLAHE) - Move this BEFORE scaling/skew correction
        # This boosts the text contrast while keeping it grayscale for EasyOCR
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast_boosted = clahe.apply(denoised)

        # 4. Skew Correction
        # We temporarily binarize *just* to find the text angle, without ruining the final image
        _, binary_for_skew = cv2.threshold(contrast_boosted, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        coords = np.column_stack(np.where(binary_for_skew > 0))  # foreground pixels

        if len(coords) > 0:
            # minAreaRect behavior can vary slightly by OpenCV version, 
            # but this is a standard approach to normalize the angle
            rect = cv2.minAreaRect(coords)
            angle = rect[-1]
            if angle < -45:
                angle = 90 + angle
            elif angle > 45:
                angle = angle - 90
                
            # Rotate the high-contrast grayscale image, NOT the binary one
            (h, w) = contrast_boosted.shape
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            deskewed = cv2.warpAffine(contrast_boosted, M, (w, h), flags=cv2.INTER_CUBIC, borderValue=255)
        else:
            deskewed = contrast_boosted

        # 5. Image Scaling (Upscale the clean grayscale result)
        scale = 2.0
        final_processed = cv2.resize(deskewed, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

        # Run OCR on the high-contrast grayscale image
        results = self.__reader.readtext(final_processed)

        # Create a list to store every valid line of text found
        extracted_lines = []

        for r in results:
            box, text, confidence = r
            if confidence < 0.24:
                continue
            # Clean up any trailing/leading whitespaces and add to our list
            extracted_lines.append(text.strip())

        # Join the list items together into one big string separated by newlines
        final_text_string = "\n".join(extracted_lines)
        return final_text_string

