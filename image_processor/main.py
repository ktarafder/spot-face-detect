import os
import pickle
from concurrent.futures import ThreadPoolExecutor, as_completed
from .image_utils import load_default_hashes
from .face_encoder import process_image

def EncodeFolder(folder_path):
    """Process all images in a folder and save face encodings."""
    filter_path = './Filter_Images'
    default_hashes = load_default_hashes(filter_path)

    # Process images
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    encodings = []
    img_ids = []

    with ThreadPoolExecutor() as executor:
        future_to_file = {executor.submit(process_image, file, default_hashes): file 
                         for file in image_files}
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