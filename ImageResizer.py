import os
from PIL import Image
import imagehash

def smart_crop_and_resize(img, target_size=(216, 216)):
    width, height = img.size
    
    if width == height:
        # Image is already square, just resize it
        return img.resize(target_size, Image.Resampling.LANCZOS)
    else:
        # Crop to square, then resize
        crop_size = min(width, height)
        left = (width - crop_size) // 2
        top = (height - crop_size) // 2
        right = left + crop_size
        bottom = top + crop_size
        
        img_cropped = img.crop((left, top, right, bottom))
        return img_cropped.resize(target_size, Image.Resampling.LANCZOS)

def remove_duplicate_images(folder_path, filter_path):
    # Load default images and compute their hashes
    default_hashes = []
    for filename in os.listdir(filter_path):
        file_path = os.path.join(filter_path, filename)
        with Image.open(file_path) as img:
            default_hashes.append(imagehash.average_hash(img))

    removed_count = 0

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            try:
                with Image.open(file_path) as img:
                    img_hash = imagehash.average_hash(img)
                
                # Compare with all default image hashes
                if any(img_hash - default_hash < 5 for default_hash in default_hashes):
                    os.remove(file_path)
                    print(f"Removed: {filename}")
                    removed_count += 1
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    print(f"Total images removed: {removed_count}")


def process_images(folder_path, target_size=(216, 216)):
    processed_count = 0

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            try:
                with Image.open(file_path) as img:
                    processed_img = smart_crop_and_resize(img, target_size)
                    processed_img.save(file_path)
                    print(f"Processed: {filename}")
                    processed_count += 1
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    print(f"Total images processed: {processed_count}")

# Usage
folder_path = './Profile_Images'
filter_path = './Filter_Images'

# Remove duplicate images
remove_duplicate_images(folder_path, filter_path)

# Crop remaining images
process_images(folder_path)


#create an exception to of the image is scalable scale it to 216 x 216 if not crop it to that size 