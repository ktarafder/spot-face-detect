import os
import cv2
import cvzone
import pickle
import numpy as np
import face_recognition
from EncodeGenerator import *
from datetime import datetime

def Load_Encoded():
    file = open('EncodeFile.p', 'rb')
    encodeListKnown_with_ids = pickle.load(file)
    file.close()

    return encodeListKnown_with_ids

Profile_path = "./Profile_Images"

capture = cv2.VideoCapture(0)

capture.set(3, 640)  
capture.set(4, 480)
 
encodings, img_ids = EncodeFolder(Profile_path)

print("\nLoading Encode File...")

encodeListKnown_with_ids = Load_Encoded()
encodeListKnown, img_id = encodeListKnown_with_ids  
print(img_id) 
length_of_encoded_faces = len(img_id)
print(f"\n{length_of_encoded_faces} faces encoded!")
print("\nEncode File Loaded\n")

if len(encodings) == 0:
    print("No faces were encoded. Please check your images and try again.")
    exit()

Load_Encoded()

while True:
    success, image = capture.read()

    img_small = cv2.resize(image, (0, 0), None, 0.25, 0.25)
    img_small_rgb = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(img_small_rgb)

    face_encodings = face_recognition.face_encodings(img_small_rgb, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        
        matches = face_recognition.compare_faces(encodeListKnown, face_encoding)
        face_distances = face_recognition.face_distance(encodeListKnown, face_encoding)
        
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
        else:
            best_match_index = -1

        top, right, bottom, left = face_location  
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        bbox = (left, top, right - left, bottom - top)

        if best_match_index != -1 and matches[best_match_index]:
            recognized_name = img_id[best_match_index]
            print(f"{recognized_name} Recognized!")  

            image = cvzone.cornerRect(image, bbox, colorC=(0, 255, 0), rt=0)

            text_size, _ = cv2.getTextSize(recognized_name, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            text_width, text_height = text_size
            text_x = left + (right - left - text_width) // 2
            text_y = top - 10  

            text_x = max(0, text_x)
            text_y = max(text_height, text_y)
            
            cv2.putText(image, recognized_name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            """LLM pipeline with matched/found face integration here. recognized_name variable contains firstname_lastname of person. TTS prompt for recognized person etc..."""

        else:
            print("UNKNOWN FACE DETECTED")

            image = cvzone.cornerRect(image, bbox, colorC=(255, 0, 0), rt=0)

            unknown_label = 'unknown_face'
            text_size, _ = cv2.getTextSize(unknown_label, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            text_width, text_height = text_size

            text_x = left + (right - left - text_width) // 2
            text_y = top - 10

            text_x = max(0, text_x)
            text_y = max(text_height, text_y)
            cv2.putText(image, unknown_label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            """UNRECOGNIZED FACE condition LLM integration here. Pipeline for TTS prompt when user isn't recognized etc..."""
            
            face_img = image[top:bottom, left:right]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"unknown_face_{timestamp}.jpg"
            cv2.imwrite(os.path.join(Profile_path, filename), face_img)
            print(f"Unknown face saved as {filename}")

            encodings, img_ids = EncodeFolder(Profile_path)
            
            encodeListKnown_with_ids = Load_Encoded()
            encodeListKnown, img_id = encodeListKnown_with_ids  
            print(img_id) 
            length_of_encoded_faces = len(img_id)
            print(f"\n{length_of_encoded_faces} faces encoded!")
            print("\nEncode File Loaded\n")

    cv2.imshow("Spot's Live Feed",image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.getWindowProperty("Spot's Live Feed", cv2.WND_PROP_VISIBLE) < 1:
        break

capture.release()
cv2.destroyAllWindows()
