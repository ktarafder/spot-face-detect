# encode.py
from image_processor import EncodeFolder
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python encode.py <folder_path>")
        return
    
    folder_path = sys.argv[1]
    print(f"Processing images from: {folder_path}")
    
    # Run encoding
    encodings, img_ids = EncodeFolder(folder_path)
    print(f"Completed! Processed {len(img_ids)} images")

if __name__ == "__main__":
    main()