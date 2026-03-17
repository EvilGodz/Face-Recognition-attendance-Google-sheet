"""use to enroll student"""
import pickle
import face_recognition
import cv2
import spreadsheet

photo_folder = 'C:/Desktop/hopeanddream/known faces photos/'
facial_encodings_folder='C:/Desktop/hopeanddream/known face encodings/'

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

def encoding_of_enrolled_person(name,image):
	enroll_encoding=[]

	enroll_encoding.append(face_recognition.face_encodings(face_recognition.load_image_file(image))[0])
	f=open(facial_encodings_folder+name+'.txt','w+')
	
	with open(facial_encodings_folder+name+'.txt','wb') as fp:
		pickle.dump(enroll_encoding,fp)
	f.close
    
    

def enroll_via_camera(name):
	while True:
		ret,frame=cap.read()
		cv2.imshow('Enrolling new student',frame)
		k=cv2.waitKey(1)
		if k & 0xFF==ord('y'):
			cv2.imwrite(photo_folder+name+'.jpg',frame)
			encoding_of_enrolled_person(name,photo_folder+name+'.jpg')
			cv2.destroyAllWindows()
			break
		if k& 0xFF==ord('q'):
			print('quitting')
			cv2.destroyAllWindows()
			break
	cap.release()
	id=input("Enter Student ID: ")
	spreadsheet.enroll_person_to_sheet(name,id)
	