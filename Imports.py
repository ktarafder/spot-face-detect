import os

Imports = "opencv-python", "pickle-mixin", "face-recognition", "numpy", "cvzone"

for x in Imports:
    os.system(f"pip install {x}") 
    print(f"{x} is done.")