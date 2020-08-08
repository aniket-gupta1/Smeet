import sys
import time
import pprint
import pickle
import config
from datetime import datetime
import webbrowser
from functools import partial
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from AppIndicator_file import AppIndicator
from Calendar_interface import Interface
from socket import create_connection
from gi.repository import Notify as notify

Theme_dict = dict()

Theme_dict['Reference'] = ["Background", "Button_colour", "Button_press", "Groupbox_bg", "Text", "", "", "", ""]
Theme_dict['Deep_Purple'] = ["#1A1A1D", "#3500D3", "#240090", "#4E4E50", "#EDF5E1"]
Theme_dict['Contemporary'] = ["#1A1A1D", "#C30740", "#6F2232", "#4E4E50", "#EDF5E1"]

default_theme = 'Contemporary'
Colour_pallete = Theme_dict[default_theme]

class Smeet(QWidget):
	"""docstring for Smeet"""
	def __init__(self, parent=None):
		super(Smeet, self).__init__(parent)
		smeet_.aboutToQuit.connect(self.change_quit_var)
		self.Main_window()

	def Main_window(self):

		self.setWindowTitle('Smeet')

		self.main_layout = QVBoxLayout()

		self.main_layout.addWidget(self.Top_groupbox())
		self.top_label = QLabel("<H3>Upcoming Meetings</H3>")
		self.top_label.setStyleSheet(f"color : {Colour_pallete[4]}")
		self.main_layout.addWidget(self.top_label)

		self.notification_groupbox = QWidget()
		self.notification_groupbox.setContentsMargins(0,0,0,0)
		self.notification_groupbox_layout = QVBoxLayout()
		self.notification_groupbox.setLayout(self.notification_groupbox_layout)

		self.scroll = QScrollArea()
		self.scroll.setWidget(self.notification_groupbox)
		self.scroll.setWidgetResizable(True)
		self.scroll.setStyleSheet(f"QScrollBar:vertical {{background-color: {Colour_pallete[0]}; width: 15px;\
		 		margin: 15px 3px 15px 3px; border: 1px transparent {Colour_pallete[0]};border-radius: 4px;}}\
		 		QScrollBar::handle:vertical {{background-color: {Colour_pallete[1]}; min-height: 5px; border-radius: 4px;}}\
		 		QScrollBar::sub-line:vertical {{margin: 3px 0px 3px 0px; border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\
     			height: 10px; width: 10px; subcontrol-position: top; subcontrol-origin: margin; }}\
     			QScrollBar::add-line:vertical {{ margin: 3px 0px 3px 0px; border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\
     			height: 10px; width: 10px; subcontrol-position: bottom; subcontrol-origin: margin; }}\
     			QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {{ border-image: url(:/qss_icons/rc/up_arrow.png);\
     			height: 10px; width: 10px; subcontrol-position: top; subcontrol-origin: margin;}}\
     			QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {{ border-image: url(:/qss_icons/rc/down_arrow.png);\
     			height: 10px; width: 10px; subcontrol-position: bottom; subcontrol-origin: margin; }}\
     			QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{background: none;}}\
     			QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: none; }}")
		self.scroll.AdjustToContents

		self.scroll.setMinimumHeight(120)
		self.scroll.setMaximumHeight(300)
		self.main_layout.addWidget(self.scroll)

		self.update_timer = QTimer()
		self.update_timer.setInterval(1000)
		self.update_timer.timeout.connect(self.Notification_Groupbox_update)
		self.update_timer.start()
		self.notes_label = QLabel("<H3>Personal Notes</H3>")
		self.notes_label.setStyleSheet(f"color : {Colour_pallete[4]}")
		self.main_layout.addWidget(self.notes_label)

		self.notepad = QTextEdit()

		try:
			temp_string = pickle.load(open("note_file.pkl", "rb"))
			self.notepad.setText(temp_string)
		except:
			pass

		self.notepad.setStyleSheet(f" color: {Colour_pallete[4]}; background-color: {Colour_pallete[3]}; border-radius: 5px")
		self.main_layout.addWidget(self.notepad)

		self.main_layout.addWidget(self.Bottom_groupbox())

		self.setLayout(self.main_layout)
		self.setMinimumSize(500,400)
		self.setWindowIcon(QIcon("/home/aniket/Deep_RL/Smeet/human2.png"))

	def change_quit_var(self):
		#print("yaysdfghjksdfghjkasdfghjklasdfghjk")
		#global quit_variable
		config.quit_variable = True
		notify.uninit()

	def Notification_Groupbox_update(self):

		if config.quit_variable:
			smeet_.closeAllWindows()

		if config.internet_available:
			try:
				create_connection(("1.1.1.1", 53), timeout = 2)
			except:
				config.internet_available=False

		#global temp_meetings
		self.Join_meeting_buttons = []
		self.Delete_meeting_buttons = []

		for i in reversed(range(self.notification_groupbox_layout.count())): 
			widgetToRemove = self.notification_groupbox_layout.itemAt(i).widget()
			# remove it from the layout list
			self.notification_groupbox_layout.removeWidget(widgetToRemove)
			# remove it from the gui
			widgetToRemove.setParent(None)

		for i,meeting in enumerate(config.temp_meetings):
			sub_group = QGroupBox()
			layout = QHBoxLayout()
			layout.setContentsMargins(5,5,5,5)

			#Sublayout to print date nicely
			sub_sub_groupbox = QGroupBox()
			sub_sub_groupbox.setStyleSheet(f"QGroupBox {{ border:0px ;padding: 0px 0px 0px 0px; background-color : {Colour_pallete[3]}}} ")
			sub_layout = QVBoxLayout()
			sub_layout.setContentsMargins(0,0,0,0)
			Time_label = QLabel(meeting[0][0])
			Time_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color : {Colour_pallete[4]} ; background-color : {Colour_pallete[3]} ; padding: 0px 0px 0px 0px; margin = 0px 0px 0px 0px")
			Day_label = QLabel(meeting[0][4])
			Day_label.setStyleSheet(f"font-size: 11px; color : {Colour_pallete[4]} ; background-color : {Colour_pallete[3]} ; padding: 0px 0px 0px 0px; margin = 0px 0px 0px 0px")

			sub_layout.addWidget(Time_label)
			sub_layout.addWidget(Day_label)
			sub_sub_groupbox.setLayout(sub_layout)
			sub_sub_groupbox.setFixedSize(100, 50)
			layout.addWidget(sub_sub_groupbox)

			self.Event_name_label = QLabel(str(meeting[1]))
			self.Event_name_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color : {Colour_pallete[4]} ; background-color : {Colour_pallete[3]}")
			# self.Event_name_label.setMaximumSize(300,30)
			layout.addWidget(self.Event_name_label, alignment = Qt.AlignLeft)

			if meeting[2] is not None:
				self.Join_meeting_buttons.append(QPushButton("Join Meeting"))
			else:
				self.Join_meeting_buttons.append(QPushButton("No active link"))
			self.Join_meeting_buttons[i].clicked.connect(self.temp_(meeting[2]))
			self.Join_meeting_buttons[i].setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px; max-width: 6em;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}")


			self.Delete_meeting_buttons.append(QPushButton())
			self.Delete_meeting_buttons[i].setIcon(QIcon("/home/aniket/Deep_RL/Smeet/bin.png"))
			self.Delete_meeting_buttons[i].setMaximumSize(30,30)
			#self.Delete_meeting_buttons[i].clicked.connect(self.Delete_event(meeting[2]))
			self.Delete_meeting_buttons[i].setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}")

			layout.addWidget(self.Join_meeting_buttons[i])
			#layout.addWidget(self.Delete_meeting_buttons[i])
			
			sub_group.setLayout(layout)
			sub_group.setStyleSheet(f"QGroupBox::title {{ border: 0px ; border-radius: 0px; padding: 0px 0px 0px 0px; margin = 0px 0px 0px 0px }} \
				QGroupBox {{ border:0px ; border-radius: 5px; padding: 0px 0px 0px 0px; background-color :{Colour_pallete[3]} }} ")

			self.notification_groupbox_layout.addWidget(sub_group)

		if not config.temp_meetings and config.internet_available:
			# print("True")
			empty_label = QLabel("No Upcoming events")
			empty_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color : {Colour_pallete[4]};")
			self.notification_groupbox_layout.addWidget(empty_label, alignment = Qt.AlignCenter)
		elif not config.internet_available:
			empty_label = QLabel("No Internet Available. Please connect to internet")
			empty_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color : {Colour_pallete[4]};")
			self.notification_groupbox_layout.addWidget(empty_label, alignment = Qt.AlignCenter)

		#print("Groupbox: ",config.internet_available)

		self.notification_groupbox.setLayout(self.notification_groupbox_layout)

	def Delete_event(self, meeting):
		pass

	def temp_(self, link):
		#print("asdffffffffffff")
		def open_link():
			if link!=None:
				try:
					webbrowser.open(link)
				except:
					#print("No link provided")
					pass
			else:
				pass
				#print("No link provided")
		return open_link

	def Top_groupbox(self):
		top_groupbox_ = QGroupBox()
		top_groupbox_.setStyleSheet(f"QGroupBox::title {{ border: 0px ; border-radius: 0px; padding: 0px 0px 0px 0px; margin = 0px 0px 0px 0px }} \
					QGroupBox {{ border:0px ;padding: 0px 0px 0px 0px; background-color : {Colour_pallete[0]} }} ")

		layout = QHBoxLayout()
		layout.setContentsMargins(0,0,0,0)

		self.goto_login_window = QPushButton()
		self.goto_login_window.setMaximumSize(QSize(30,30))
		self.goto_login_window.setIcon(QIcon("/home/aniket/Deep_RL/Smeet/login_.png"))
		self.goto_login_window.setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}")
		layout.addWidget(self.goto_login_window)

		layout.addWidget(QLabel())

		self.Launch_appindicator_button = QPushButton()
		self.Launch_appindicator_button.setMaximumSize(QSize(30,30))
		self.Launch_appindicator_button.move(50,50)
		self.Launch_appindicator_button.setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}")
		self.Launch_appindicator_button.setIcon(QIcon("/home/aniket/Deep_RL/Smeet/smeet_icon.png"))
		layout.addWidget(self.Launch_appindicator_button)
		
		self.new_event_button = QPushButton()
		self.new_event_button.setMaximumSize(QSize(30,30))
		self.new_event_button.setIcon(QIcon("/home/aniket/Deep_RL/Smeet/add_event.png"))
		self.new_event_button.setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}")
		layout.addWidget(self.new_event_button)
		
		self.calendar_button = QPushButton()
		self.calendar_button.setMaximumSize(QSize(30,30))
		self.calendar_button.setIcon(QIcon("/home/aniket/Deep_RL/Smeet/calendar.png"))
		self.calendar_button.setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}")
		layout.addWidget(self.calendar_button)

		top_groupbox_.setLayout(layout)

		return top_groupbox_

	def Bottom_groupbox(self):
		bottom_groupbox_ = QGroupBox()

		bottom_groupbox_.setStyleSheet(f"QGroupBox::title {{ border: 0px ; border-radius: 0px; padding: 0px 0px 0px 0px; margin = 0px 0px 0px 0px }} \
					QGroupBox {{ border:0px ;padding: 0px 0px 0px 0px; background-color : {Colour_pallete[0]} }} ")

		layout = QHBoxLayout()
		layout.setContentsMargins(0,0,0,0)

		self.about_button = QPushButton()
		self.about_button.setMaximumSize(QSize(30,30))
		self.about_button.setIcon(QIcon("/home/aniket/Deep_RL/Smeet/icons8-about-100.png"))
		self.about_button.setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}")
		layout.addWidget(self.about_button)

		self.save_notes_button = QPushButton("Save Note")
		self.save_notes_button.setMaximumSize(QSize(90,30))
		self.save_notes_button.setContentsMargins(0,0,0,0)
		self.save_notes_button.setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}")
		self.save_notes_button.clicked.connect(self.save_notes_func)
		layout.addWidget(self.save_notes_button)
		
		self.quit_button = QPushButton()
		self.quit_button.setMaximumSize(QSize(30,30))
		self.quit_button.setIcon(QIcon("/home/aniket/Deep_RL/Smeet/quit.png"))
		self.quit_button.setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}")
		layout.addWidget(self.quit_button)

		layout.addWidget(QLabel())

		bottom_groupbox_.setLayout(layout)

		return bottom_groupbox_

	def save_notes_func(self):
		pickle.dump(self.notepad.toPlainText(), open("note_file.pkl", 'wb'))

	def check_func(self):
		global Colour_pallete
		selected_theme = self.settings_button.currentText()
		Colour_pallete = Theme_dict[str(selected_theme)]

class Settings_Page(QWidget):
	def __init__(self, parent = None):
		super(Settings_Page, self).__init__(parent)
		self.setWindowTitle("Settings")
		layout = QVBoxLayout()

		self.return_to_main_window = QPushButton()
		self.return_to_main_window.setIcon(QIcon("/home/aniket/Deep_RL/Smeet/back-arrow.png"))
		self.return_to_main_window.setMaximumSize(QSize(30,30))
		self.return_to_main_window.setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}")

		layout.addWidget(self.return_to_main_window)

class About_Page(QWidget):
	def __init__(self, parent = None):
		super(About_Page, self).__init__(parent)
		self.setWindowTitle("About")
		layout = QVBoxLayout()

		self.return_to_main_window = QPushButton()
		self.return_to_main_window.setIcon(QIcon("/home/aniket/Deep_RL/Smeet/back-arrow.png"))
		self.return_to_main_window.setMaximumSize(QSize(30,30))
		self.return_to_main_window.setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}")

		layout.addWidget(self.return_to_main_window)

		print_string = """Smeet was dveloped as an utility app to easily keep a tab of open items in your calendar. 
		It provides an interactive way to create and see all the events set on your Google calendar and notifies the user of upcoming events."""

		label = QLabel(print_string)
		label.setWordWrap(True)
		label.setStyleSheet(f"font-size: 14px; font-weight: bold; color : {Colour_pallete[4]} ;")
		layout.addWidget(label)

		self.setLayout(layout)

class Login_Page(QWidget):
	def __init__(self, parent=None):
		super(Login_Page, self).__init__(parent)
		self.setWindowTitle("Smeet")

		self.interface_obj = Interface()

		self.threadpool = QThreadPool()
		temp_obj = Event_show(self.interface_obj)
		self.threadpool.start(temp_obj)
				
		layout = QVBoxLayout()
		self.return_to_main_window = QPushButton()
		self.return_to_main_window.setMaximumSize(QSize(30,30))
		self.return_to_main_window.setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}")
		self.return_to_main_window.setIcon(QIcon("/home/aniket/Deep_RL/Smeet/back-arrow.png"))
		layout.addWidget(self.return_to_main_window)
		
		hello_label = QLabel("Hello.")
		hello_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color : {Colour_pallete[4]} ;")
		layout.addWidget(hello_label, alignment = Qt.AlignCenter)

		signin_label = QLabel("Welcome to Smeet!")
		signin_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color : {Colour_pallete[4]} ;")
		layout.addWidget(signin_label, alignment = Qt.AlignCenter)

		layout.addWidget(QLabel())
		layout.addWidget(QLabel())

		d= """		Sign Up Instructions"""
		Instructions_label = QLabel(d)
		Instructions_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color : {Colour_pallete[4]} ;")
		Instructions_label.setAlignment(Qt.AlignLeft)
		Instructions_label.setContentsMargins(0,0,0,0)
		layout.addWidget(Instructions_label)
		
		s = """		1. Press Sign Up
		2. Wait for the browser to open 
		3. Select your account 
		4. Copy the generated token here
		"""
		
		label = QLabel(s)
		label.setStyleSheet(f"font-size: 14px; font-weight: bold; color : {Colour_pallete[4]} ;")
		label.setAlignment(Qt.AlignLeft)
		label.setContentsMargins(0,0,0,0)
		layout.addWidget(label)

		self.Sign_in_button = QPushButton("Sign Up")
		self.Sign_in_button.setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}")
		self.Sign_in_button.setMaximumSize(QSize(80,30))
		self.Sign_in_button.clicked.connect(self.interface_obj.open_credentials_website)
		layout.addWidget(self.Sign_in_button, alignment = Qt.AlignCenter)
		
		self.Token_input = QLineEdit()
		self.Token_input.setPlaceholderText("Enter Token")
		self.Token_input.setMinimumSize(300,30)
		self.Token_input.setStyleSheet(f"border-color: black; background-color: {Colour_pallete[3]}")
		layout.addWidget(self.Token_input, alignment = Qt.AlignCenter)

		self.Proceed_button = QPushButton("Proceed")
		self.Proceed_button.setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}")
		self.Proceed_button.setMaximumSize(QSize(80,30))
		self.Proceed_button.clicked.connect(self.temp)
		layout.addWidget(self.Proceed_button, alignment = Qt.AlignCenter)

		layout.addStretch(1)

		self.setLayout(layout)

	def temp(self):
		self.interface_obj.enter_credentials(self.Token_input.text())

class Calendar_window(QWidget):
	def __init__(self, parent=None):
		super(Calendar_window, self).__init__(parent)
		self.setWindowTitle("Smeet Calendar")

		layout = QVBoxLayout()
		self.calendar = QCalendarWidget()
		self.calendar.move(20,20)
		self.calendar.setGridVisible(False)
		self.calendar.setNavigationBarVisible(1)
		#self.calendar.setFont(QFont('Times', 8))
		#self.calendar.setStyleSheet("background-color : #C3073F")

		self.calendar.setStyleSheet(f"QWidget {{background-color: {Colour_pallete[1]}}}\
		QMenu {{font-size:12px; width: 80px; left: 20px; background-color: {Colour_pallete[3]};}} \
		QToolButton {{icon-size: 14px, 14px; background-color: {Colour_pallete[1]};}}\
		QAbstractItemView {{border-radius: 10px; background-color: {Colour_pallete[4]}; selection-background-color: {Colour_pallete[3]};}}\
		QToolButton::menu-arrow {{}}\
		QToolButton::menu-button {{}}\
		QToolButton::menu-indicator{{width: 50px;}}\
		QToolButton::menu-indicator:pressed ,\
		QToolButton::menu-indicator:open{{top:10px; left: 10px;}}\
		QListView {{background-color:{Colour_pallete[4]};}}\
		QSpinBox::up-button {{ subcontrol-origin: border;\
		subcontrol-position: top right; width:50px; border-image: url(icons:arrow_up_n.png);}}\
		QSpinBox::down-button {{subcontrol-origin: border; subcontrol-position: bottom right;\
		border-width: 1px; width:50px;}}\
		QSpinBox::down-arrow {{ width:26px; height:17px;\
		image: url(icons:arrow_down_n.png); }}")

		self.calendar.clicked.connect(self.printDateInfo)

		self.return_to_main_window = QPushButton()
		self.return_to_main_window.setIcon(QIcon("/home/aniket/Deep_RL/Smeet/back-arrow.png"))
		self.return_to_main_window.setMaximumSize(QSize(30,30))
		self.return_to_main_window.setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}")
		layout.addWidget(self.return_to_main_window)
		layout.addWidget(self.calendar)
		self.setLayout(layout)

	def printDateInfo(self, qDate):
		pass
		# print('{0}/{1}/{2}'.format(qDate.month(), qDate.day(), qDate.year()))
		# print(f'Day Number of the year: {qDate.dayOfYear()}')
		# print(f'Day Number of the week: {qDate.dayOfWeek()}')

class Event_show(QRunnable):
	def __init__(self, interface_obj):
		super(Event_show, self).__init__()

		self.interface_obj = interface_obj

	@pyqtSlot()
	def run(self):
		#print("here?")
		while (True):
			try:
				if config.quit_variable:
					break

				try:
					create_connection(("1.1.1.1", 53), timeout = 2)
					config.internet_available = True
					meetings = self.interface_obj.show_events()			

					currentDateTime = datetime.now()
					date = currentDateTime.date()
					hour = currentDateTime.hour
					minute = currentDateTime.minute

					for m in meetings:
						if m not in config.discard_list:
							time_24_hr = datetime.strptime(m[0][0], "%I:%M %p").strftime("%H:%M")
							if str(date)==m[3]:
								if time_24_hr[:2] == str(hour) and int(minute)-10 <= int(time_24_hr[3:]) <= int(minute)+10: 

									try:
										config.discard_list+=[m]
										notify.Notification.new("Meeting Alert", f"{m[1]} at {m[0][0]}", None).show()
									except Exception as e:
										pass
										#print(e)

						if m in config.temp_meetings:
							continue
						else:
							config.temp_meetings+=[m]
					#print("event: ",config.internet_available)
				except Exception as e:
					#print("Exception line 554:",e)
					config.internet_available = False
			except Exception as e:
				pass
				#print(e)

			time.sleep(0.01)

class Create_Event(QWidget):
	def __init__(self):
		super(Create_Event, self).__init__()
		self.interface_obj = Interface()

		self.layout = QVBoxLayout()
		self.return_to_main_window = QPushButton()
		self.return_to_main_window.setMaximumSize(QSize(30,30))
		self.return_to_main_window.setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}")
		self.return_to_main_window.setIcon(QIcon("/home/aniket/Deep_RL/Smeet/back-arrow.png"))
		self.layout.addWidget(self.return_to_main_window)

		self.form_group = QGroupBox()

		self.form_layout = QFormLayout()

		self.Event_label = QLabel("Event")
		self.Event_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color : {Colour_pallete[4]};")
		self.Event_input = QLineEdit()
		self.Event_input.setStyleSheet(f"color: {Colour_pallete[4]}; border-color: black; background-color: {Colour_pallete[3]}")
		self.Event_input.setPlaceholderText("Enter event name")

		self.Date_label = QLabel("Date")
		self.Date_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color : {Colour_pallete[4]};")
		self.Date_input = QDateTimeEdit()
		self.Date_input.setDateTime(QDateTime.currentDateTime())
		self.Date_input.setStyleSheet(f"color: {Colour_pallete[4]}; border-color: black; background-color: {Colour_pallete[3]}")

		self.Attendees_label = QLabel("Add Guests")
		self.Attendees_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color : {Colour_pallete[4]};")

		layout2 = QHBoxLayout()
		self.Add_attendees_file = QPushButton()
		self.Add_attendees_file.setIcon(QIcon("/home/aniket/Deep_RL/Smeet/icons8-add-file-50.png"))
		self.Add_attendees_file.setMaximumSize(30,30)
		self.Add_attendees_file.setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}") 
		self.Add_attendees_file.clicked.connect(self.get_guest_emails)
		self.Attendees_input = QLineEdit()
		self.Attendees_input.setStyleSheet(f"color: {Colour_pallete[4]}; border-color: black; background-color: {Colour_pallete[3]}")
		self.Attendees_input.setPlaceholderText("Enter guest mails")

		layout2.addWidget(self.Attendees_input)
		layout2.addWidget(self.Add_attendees_file)

		self.Meet_label = QLabel("Video Conference")
		self.Meet_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color : {Colour_pallete[4]};")
		self.Meet_input = QPushButton("Add Google Meet Link")
		self.Meet_input.setMaximumSize(200,30)
		self.Meet_input.setCheckable(True)
		self.Meet_input.clicked.connect(self.Change_color)
		self.Meet_input.setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}")

		self.Location_label = QLabel("Location")
		self.Location_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color : {Colour_pallete[4]};")
		self.Location_input = QLineEdit()
		self.Location_input.setStyleSheet(f"color: {Colour_pallete[4]}; border-color: black; background-color: {Colour_pallete[3]}")
		self.Location_input.setPlaceholderText("Enter location ")

		self.Description_label = QLabel("Event_description")
		self.Description_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color : {Colour_pallete[4]};")
		self.Description_input = QTextEdit()
		self.Description_input.setStyleSheet(f"color: {Colour_pallete[4]}; border-color: black; background-color: {Colour_pallete[3]}")
		self.Description_input.setPlaceholderText("Enter event description")

		self.form_layout.addRow(self.Event_label, self.Event_input)
		self.form_layout.addRow(self.Date_label, self.Date_input)
		#self.form_layout.addRow(self.Attendees_label, self.Attendees_input)
		self.form_layout.addRow(self.Attendees_label, layout2)
		self.form_layout.addRow(self.Meet_label, self.Meet_input)
		self.form_layout.addRow(self.Location_label, self.Location_input)
		self.form_layout.addRow(self.Description_label, self.Description_input)

		self.form_group.setLayout(self.form_layout)

		submit_button = QPushButton("Set Event")
		submit_button.setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}")
		submit_button.clicked.connect(self.create_event_func)

		self.layout.addWidget(self.form_group)
		self.layout.addWidget(submit_button, alignment=Qt.AlignCenter)
		
		self.setLayout(self.layout)

		self.guest_list = []

	def get_guest_emails(self):
		dlg = QFileDialog()
		name = dlg.getOpenFileName(self, 'Open File')
		file = open(name[0], 'r')

		with file:
			text = str(file.read())
		
		self.guest_list = text.strip().split("\n")
		#print(self.guest_list)

	def Change_color(self):
		if self.Meet_input.isChecked():
			self.Meet_input.setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[2]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[1]};}}")
		else:
			self.Meet_input.setStyleSheet(f"QPushButton {{background-color: {Colour_pallete[1]}; border-style: outset; \
				border-width: 1px; border-radius: 5px; border-color: black; font: 14px;\
				padding: 6px;}} QPushButton:pressed {{background-color: {Colour_pallete[2]};}}")

	def create_event_func(self):

		guest_list1 = self.Attendees_input.text()
		if len(guest_list1):
			guest_list1 = guest_list1.split(" ")

			if len(self.guest_list):
				guest_list1 += self.guest_list
		else:
			guest_list1 = self.guest_list


		self.interface_obj.create_event(self.Event_input.text(), self.Date_input.dateTime().toString(), 
								guest_list1, self.Meet_input.isChecked(), self.Location_input.text(), 
								description = self.Description_input.toPlainText())

def Launch_AppIndicator():
	obj = AppIndicator()
	obj.main_func()

def Quit_app():
	#global quit_variable
	config.quit_variable = True
	QApplication.instance().quit()

if __name__=="__main__":
	smeet_ = QApplication(sys.argv)
	smeet_.setStyle('Oxygen')
	palette = QPalette()
	palette.setColor(QPalette.Window, QColor(f"{Colour_pallete[0]}"))
	smeet_.setPalette(palette)
	notify.init("Smeet")

	main_window = Smeet()
	login_window = Login_Page()
	calendar_window = Calendar_window()
	about_window = About_Page()
	settings_window = Settings_Page()
	create_event_window = Create_Event()

	main_window.Launch_appindicator_button.clicked.connect(Launch_AppIndicator)

	w = QStackedWidget()

	w.addWidget(main_window)
	w.addWidget(login_window)
	w.addWidget(calendar_window)
	w.addWidget(settings_window)
	w.addWidget(about_window)
	w.addWidget(create_event_window)

	if login_window.interface_obj.credentials_available:
		w.setCurrentIndex(0)
	else:
		w.setCurrentIndex(1)

	main_window.goto_login_window.clicked.connect(lambda: w.setCurrentIndex(1))
	login_window.return_to_main_window.clicked.connect(lambda: w.setCurrentIndex(0))
	main_window.calendar_button.clicked.connect(lambda: w.setCurrentIndex(2))
	calendar_window.return_to_main_window.clicked.connect(lambda: w.setCurrentIndex(0))
	main_window.about_button.clicked.connect(lambda: w.setCurrentIndex(4))
	about_window.return_to_main_window.clicked.connect(lambda: w.setCurrentIndex(0))
	main_window.new_event_button.clicked.connect(lambda: w.setCurrentIndex(5))
	create_event_window.return_to_main_window.clicked.connect(lambda: w.setCurrentIndex(0))

	main_window.quit_button.clicked.connect(Quit_app)

	w.show()

	sys.exit(smeet_.exec_())
