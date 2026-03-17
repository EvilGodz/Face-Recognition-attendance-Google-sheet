"""main thing used for recog"""

import face_recognition,cv2,os,pickle
import numpy as np
import spreadsheet 

known_face_encodings=[]
known_face_names=[]
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

photo_folder = 'C:/Desktop/facerecognition project/known face photos/'
facial_encodings_folder='C:/Desktop/facerecognition project/known face encodings/'

def load_facial_encodings_and_names_from_memory():
	for filename in os.listdir(facial_encodings_folder):
		known_face_names.append(filename[:-4])
		with open (facial_encodings_folder+filename, 'rb') as fp:
			known_face_encodings.append(pickle.load(fp)[0])
            
            
def run_recognition():


     video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)


     face_locations = []
     face_encodings = []
     face_names = []
     process_this_frame = True

     while True:
    # หยิบภาพมาเฟรมนึง
          ret, frame = video_capture.read()

    # ย่อให้ภาพเล็กลงเพื่อประมวลผลได้เร็วขึ้น
          small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # เปลี่ยน BGR เป็น RGB
          rgb_small_frame = small_frame[:, :, ::-1]

    # ประมวลผลรูปเว้นรูปเพื่อประหยัดเวลา
          if process_this_frame:
        # หาหน้าที่ถูกเข้ารหัสในเฟรมนี้ของวิดีโอ
               face_locations = face_recognition.face_locations(rgb_small_frame)
               face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

               face_names = []
               for face_encoding in face_encodings:
            # ดูว่าหน้าตรงกับฐานข้อมูลไหม
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

            # แสดงชื่อจากฐานข้อมูล
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # แสดงชื่อจากฐานข้อมูลที่ตรงกับหน้าที่สุด
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                         name = known_face_names[best_match_index]

                         face_names.append(name)

                    process_this_frame = not process_this_frame


    # แสดงผลลัพธ์
          for (top, right, bottom, left), name in zip(face_locations, face_names):
        # ขยายภาพคืนจากตอนประมวล
             top *= 4
             right *= 4
             bottom *= 4
             left *= 4

        # วาดกล่องตรงหน้า
             cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # วาดป้ายพร้อมชื่อตรงหน้า
             cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
             font = cv2.FONT_HERSHEY_DUPLEX
             cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # แสดงรูปผลลัพธ์
          cv2.imshow('Video', frame)
          flag=-1
          if(len(face_names)!=0):
            count=0
          for person in face_names:
               if(person=='Unknown'):
                    count+=1
          if(count==len(face_names)):
               flag=1
          else:
               flag=0


    # กด q เพื่อออก

    
          if cv2.waitKey(1) & 0xFF==ord('q') or flag==0:
               spreadsheet.write_to_sheet(face_names[0])
               break
        
            

# ปล่อยกล้อง
     video_capture.release()
     cv2.destroyAllWindows()
