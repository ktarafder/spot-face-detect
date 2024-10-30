import os
import cv2
import pickle
import imagehash
from PIL import Image
import face_recognition
from concurrent.futures import ThreadPoolExecutor, as_completed

def smart_crop_and_resize(img, size):
    width, height = img.size
    crop_size = min(width, height)
    left = (width - crop_size) // 2
    top = (height - crop_size) // 2
    right = left + crop_size
    bottom = top + crop_size
    
    return img.crop((left, top, right, bottom)).resize(size, Image.LANCZOS)

def compute_image_hash(file_path):
    with Image.open(file_path) as img:
        return imagehash.average_hash(img)

def process_image(file_path, default_hashes):
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

def EncodeFolder(folder_path):
    filter_path = './Filter_Images'
    # Load default image hashes
    default_hashes = [compute_image_hash(os.path.join(filter_path, f)) 
                        for f in os.listdir(filter_path) 
                        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # Process images
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    encodings = []
    img_ids = []

    with ThreadPoolExecutor() as executor:
        future_to_file = {executor.submit(process_image, file, default_hashes): file for file in image_files}
        for future in as_completed(future_to_file):
            result = future.result()
            if isinstance(result, tuple):
                img_ids.append(result[0])
                encodings.append(result[1])
            else:
                print(result)

    # Save encodings
    with open("EncodeFile.p", 'wb') as file:
        pickle.dump([encodings, img_ids], file)

    print(f"Processed {len(encodings)} images. Encodings saved to EncodeFile.p")
    return encodings, img_ids
