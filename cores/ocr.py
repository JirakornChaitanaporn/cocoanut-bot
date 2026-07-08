import gc
import cv2
import numpy as np
import easyocr
import urllib.request

_MAX_DIMENSION = 1600


class KoreanOcr:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KoreanOcr, cls).__new__(cls)
            # quantize=True halves model memory (float32 -> int8)
            cls._instance.__reader = easyocr.Reader(['ko'], gpu=False, quantize=True)
        return cls._instance

    def make_text(self, image_url):
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            image_bytes = response.read()

        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        del nparr, image_bytes

        # Cap resolution to avoid holding multiple giant arrays at once
        h, w = image.shape
        if max(h, w) > _MAX_DIMENSION:
            factor = _MAX_DIMENSION / max(h, w)
            image = cv2.resize(image, None, fx=factor, fy=factor, interpolation=cv2.INTER_AREA)

        denoised = cv2.fastNlMeansDenoising(image, h=10)
        del image

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast_boosted = clahe.apply(denoised)
        del denoised

        _, binary_for_skew = cv2.threshold(contrast_boosted, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        coords = np.column_stack(np.where(binary_for_skew > 0))
        del binary_for_skew

        if len(coords) > 0:
            rect = cv2.minAreaRect(coords)
            angle = rect[-1]
            if angle < -45:
                angle = 90 + angle
            elif angle > 45:
                angle = angle - 90

            h, w = contrast_boosted.shape
            M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
            deskewed = cv2.warpAffine(contrast_boosted, M, (w, h), flags=cv2.INTER_CUBIC, borderValue=255)
            del contrast_boosted
        else:
            deskewed = contrast_boosted

        del coords

        # Only upscale small images; large ones already have enough resolution
        if deskewed.shape[1] < 800:
            final = cv2.resize(deskewed, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
            del deskewed
        else:
            final = deskewed

        results = self.__reader.readtext(final)
        del final
        gc.collect()

        extracted_lines = [
            text.strip()
            for _, text, confidence in results
            if confidence >= 0.24
        ]
        return "\n".join(extracted_lines)
