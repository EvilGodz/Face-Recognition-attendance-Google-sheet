"""run this to check attend"""

import spreadsheet
import recognition
#import enroll

recognition.load_facial_encodings_and_names_from_memory()

spreadsheet.mark_all_absent()

recognition.run_recognition()

#enroll.enroll_via_camera('Nontawat Kongnok')

#spreadsheet.enroll_person_to_sheet('Nontawat Kongnok','64301280011')
