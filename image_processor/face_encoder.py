import os
import cv2
import face_recognition
from PIL import Image
from .image_utils import smart_crop_and_resize, compute_image_hash

def process_image(file_path, default_hashes):
    """Process a single image: check against defaults, resize, and encode face."""
    try:
        img_hash = compute_image_hash(file_path)
        
        if any(img_hash - default_hash < 5 for default_hash in default_hashes):
            os.remove(file_path)
            return f"Removed: {os.path.basename(file_path)}"
        
        with Image.open(file_path) as img:
            processed_img = smart_crop_and_resize(img, (216, 216))
            processed_img.save(file_path)
        
        image = cv2.imread(file_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_encoding = face_recognition.face_encodings(image_rgb)
        
        if face_encoding:
            return (os.path.splitext(os.path.basename(file_path))[0], face_encoding[0])
        else:
            return f"No face found in: {os.path.basename(file_path)}"
    except Exception as e:
        return f"Error processing {os.path.basename(file_path)}: {str(e)}"