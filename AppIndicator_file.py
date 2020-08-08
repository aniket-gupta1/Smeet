from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
import webbrowser
import threading
import time
import config
from datetime import datetime

class AppIndicator():
	def __init__(self):
		self.Indicator_ID = "Smeet"
		self.indicator = appindicator.Indicator.new(self.Indicator_ID, '/home/aniket/Deep_RL/Smeet/group.png', appindicator.IndicatorCategory.SYSTEM_SERVICES)
		self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
		#self.main_menu()
		self.update_interface = threading.Thread(target = self.main_menu)
		self.update_interface.daemon = True
		self.update_interface.start()
	
	def main_menu(self):
		while True:
			menu = gtk.Menu()

			if config.internet_available:

				currentDateTime = datetime.now()
				date = currentDateTime.date()
				hour = currentDateTime.hour
				minute = currentDateTime.minute

				for meeting in config.temp_meetings:
					item_ = gtk.ImageMenuItem(f"{meeting[1]} at {meeting[0][0]}")
					image = gtk.Image()
					image.set_from_file("/home/aniket/Deep_RL/Smeet/hangouts-meet.png")
					item_.set_image(image)
					item_.set_always_show_image(True)
					item_.connect('activate', self.Open_Meeting_link, meeting[2])
					menu.append(item_)

					if meeting not in config.discard_list:
						time_24_hr = datetime.strptime(meeting[0][0], "%I:%M %p").strftime("%H:%M")
						if str(date)==meeting[3]:
							if time_24_hr[:2] == str(hour) and int(minute)-1 < int(time_24_hr[3:]) < int(minute)+1: 
								try:
									config.discard_list+=[meeting]
									notify.Notification.new("Meeting Alert", f"{meeting[1]} at {meeting[0][0]}", None).show()
								except Exception as e:
									pass
									#print(e)
				
				if not config.temp_meetings:
					menu.append(gtk.MenuItem("No Active Meetings"))
			else:
				menu.append(gtk.MenuItem("No Internet Connection"))

			menu.append(gtk.SeparatorMenuItem("Options"))

			item_quit_icon = gtk.ImageMenuItem("Quit")
			item_quit_icon_image = gtk.Image()
			item_quit_icon_image.set_from_file("/home/aniket/Deep_RL/Meet_Engine/quit.png")
			item_quit_icon.set_image(item_quit_icon_image)
			item_quit_icon.set_always_show_image(True)

			item_quit_icon.connect('activate',self.quit)
			menu.append(item_quit_icon)
			menu.show_all()

			self.indicator.set_menu(menu)

			if config.quit_variable:
				break

			time.sleep(10)

	def Open_Meeting_link(self, temp, link):
		#print("Uncomment this")
		if link!=None:
			webbrowser.open(str(link))
		else:
			pass
			#print("No active link")

	def main_func(self):
		notify.init(self.Indicator_ID)
		gtk.main()

	def quit(self, asdgaf):

		#print("Raching Here")
		config.quit_variable = True
		notify.uninit()
		gtk.main_quit()

if __name__ == "__main__":
	obj = AppIndicator()
	obj.main_func()
