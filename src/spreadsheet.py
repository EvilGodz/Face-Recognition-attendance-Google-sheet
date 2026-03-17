"""google sheet thingy"""

import datetime,gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

client = gspread.authorize(creds)

sheet = client.open("Face Recognition").sheet1

max_intime='16:00:00'

def enroll_person_to_sheet(name,id):
    nrows = len(sheet.col_values(1))
    sheet.update_cell(nrows+1,1,name)
    sheet.update_cell(nrows+1,2,id)
    
    
def mark_all_absent():
    now=datetime.datetime.now()
    date=now.strftime('%m/%d/%Y').replace('/0','/')
    if(date[0]=='0'):
        date=date[1:]
    datecell=sheet.find(date)
    nrows = len(sheet.col_values(1))
    for row in range(2,nrows+1):
        sheet.update_cell(row,datecell.col,'ข')      
        
def write_to_sheet(name):
	now=datetime.datetime.now()
	date=now.strftime('%m/%d/%Y').replace('/0','/')
	if(date[0]=='0'):
		date=date[1:]
		
	time=now.strftime('%H:%M:%S')
	namecell=sheet.find(name)
	datecell=sheet.find(date)

	if(sheet.cell(namecell.row,datecell.col).value =='ข' ):
		if(time<max_intime):
			sheet.update_cell(namecell.row,datecell.col,'/') 
			print('มา')
         
		else:
			sheet.update_cell(namecell.row,datecell.col,'ส')
			print('สาย')
	# else:
	# 	print('เช็คไปแล้ว')