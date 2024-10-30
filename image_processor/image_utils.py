import os
from PIL import Image
import imagehash

def smart_crop_and_resize(img, size):
    """Crop and resize image while maintaining aspect ratio."""
    width, height = img.size
    crop_size = min(width, height)
    left = (width - crop_size) // 2
    top = (height - crop_size) // 2
    right = left + crop_size
    bottom = top + crop_size
    
    return img.crop((left, top, right, bottom)).resize(size, Image.LANCZOS)

def compute_image_hash(file_path):
    """Compute average hash of an image."""
    with Image.open(file_path) as img:
        return imagehash.average_hash(img)

def load_default_hashes(filter_path):
    """Load hashes of default/filter images."""
    return [compute_image_hash(os.path.join(filter_path, f)) 
            for f in os.listdir(filter_path) 
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]