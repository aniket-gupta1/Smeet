from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta
import datetime
import calendar
import pickle
import datefinder
import webbrowser
import config

class Interface():
	def __init__(self):
		self.credentials_available = False
		self.service = None
		try:
			self.credentials=pickle.load(open("token.pkl", 'rb'))
			self.credentials_available = True

			if config.internet_available:
				self.service=build("calendar", "v3", credentials=self.credentials)

		except:
			pass

	def open_credentials_website(self):
		scopes = ['https://www.googleapis.com/auth/calendar']
		self.flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
		self.flow.redirect_uri = self.flow._OOB_REDIRECT_URI
		auth_url, _ = self.flow.authorization_url()
		webbrowser.open(auth_url)

	def enter_credentials(self, token):
		#print("The token is: ",token)
		self.flow.fetch_token(code=token)

		self.credentials = self.flow.credentials
		pickle.dump(self.credentials, open("token.pkl", 'wb'))

		self.credentials_available = True
		self.service=build("calendar", "v3", credentials=self.credentials)

	def show_events(self):
		page_token = None

		if self.service==None and config.internet_available:
			self.service=build("calendar", "v3", credentials=self.credentials)

		result = self.service.calendarList().list().execute()
		calendar_id = result['items'][0]['id']
		event_items = []
		while(True):
			all_events = self.service.events().list(calendarId='primary', pageToken=page_token).execute()
		
			for event in all_events['items'][0:]:
				todays_date = datetime.datetime.now()
				day = todays_date.day
				month = todays_date.month

				try:
					start_time=event['start'][list(event['start'].keys())[0]].split('+')[0].split('T')
				except:
					pass

				if((int(start_time[0][-2:]) in range(day,day+2)) and int(start_time[0][-5:-3])==month):
					try:
						event_name = event['summary']
						date = start_time[0]
						event_date, event_month, event_year = date[8:], calendar.month_name[int(date[5:7])], date[:4]
						event_day = calendar.day_name[datetime.datetime.strptime(date,"%Y-%m-%d").weekday()]
						event_start_time = start_time[1][:5]
						event_link = None
						try:
							event_link = event['hangoutLink']
						except:
							pass

						event_start_time = datetime.datetime.strptime(event_start_time, "%H:%M").strftime("%I:%M %p")
						event_items.append([[event_start_time, event_date, event_month, event_year, event_day], event_name, event_link, date])
					except:
						pass
			
			page_token = all_events.get('nextPageToken')
			if not page_token:
				break
		
		return event_items

	def create_event(self, summary, datetime, attendees='', meet_link=False, location=None, duration=1, description=None):
		
		if self.service==None and config.internet_available:
			self.service=build("calendar", "v3", credentials=self.credentials)

		temp = list(datefinder.find_dates(datetime))
		start_time = temp[0]
		
		# if len(attendees):
		# 	attendees = attendees.split(" ")
		#print(datetime, start_time)
		#print(start_time.strftime("%Y-%m-%dT%H:%M:%S"))
		end_time = start_time + timedelta(hours=duration)
		
		event = {
			'summary': summary,
			'location': location,
			'description': description,
			'start': {
				'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
				'timeZone': 'Asia/Kolkata',
			},
			'end': {
				'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
				'timeZone': 'Asia/Kolkata',
			},
			
			'reminders': {
				'useDefault': False,
				'overrides': [
					{'method': 'email', 'minutes': 24 * 60},
					{'method': 'popup', 'minutes': 10},
				],
			},
			'conferenceData': {
				'createRequest': {'requestId': '7qxaadfaelsvy0e',
								  'conferenceSolutionKey': {'type': 'hangoutsMeet'},
								  'status': {'statusCode': 'success'}
								 }
			}
		}
		self.service.events().insert(calendarId='primary', body=event, conferenceDataVersion=meet_link).execute()

	def main(self):
		s = """Press 1. Create Event 
					 2. Show ALl events
					 3. Exit"""
		#print(s)
		option=int(input())
		if(option==1):
			self.create_event("Meetingfakljjjjjjjjjjjj", "5 August 2 PM 2020")
		elif(option==2):
			self.show_events()
		else:
			exit()

if __name__=="__main__":
	obj = Interface()
	obj.main()
