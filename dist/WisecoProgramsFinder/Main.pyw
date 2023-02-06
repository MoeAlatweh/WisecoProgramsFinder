#+++++-------App Notes-------+++++#
## APP NAME:
# WisecoProgramsFinder
## VERSION:
# WisecoProgramsFinderVersion0.0.3
## Language:
# Python 3.7
## Framwork:
# Kivy and Kivymd to build the App and design the Layout
## Libraries and Built in Functions:
# glob(): Used to search files inside folder
# find(): Used to search specific text inside file
##__init__, _keyboard_closed and _on_keyboard_down:
# Used to activate the keyboard and read the keys input

## Created by:
# Moemen Alatweh
## Email:
# malatweh@rwbteam.com
# moemenatweh@hotmail.com
#+++++-----------------------------+++++#

#+++++-------Code Beginning-------+++++#
# FROM kivy.config IMPORT Config TO CONTROL APP CONFIGURATION SETTINGS.
from kivy.config import Config
# MAKE THE APP HAVE FIXED CONFIGURATION(BY PUT False) THAT'S MAKE THE USER CAN'T CHANGE ANY THING AS MEXIMIZE THE SCREEN FOR FULL SCREEN OR CHANGE THE SIZE, TO KEEP THE APP ORGANIZED.
Config.set('graphics', 'resizable', False)
# IMPORT (MDApp) TO CREATE THE APP
from kivymd.app import MDApp
# FROM kivy.core IMPORT Window TO BE ABLE TO CONTROL THE WINDOW SIZE.
from kivy.core.window import Window
# FROM kivymd.uix IMPORT ALL WIDGETS(LABELS, BUTTONS,BoxLayout,...) THAT USED IN THE APP.
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
# FROM kivymd.uix.screen IMPORT Screen TO USE IT TO DISPLAY THE APP.
from kivymd.uix.screen import Screen
# FROM kivy.uix.image IMPORT (AsyncImage) IF NEED TO USE IMAGE FROM WEBSITE , USE (Image) IF PHOTO ON LOCAL COMPUTER
from kivy.uix.image import AsyncImage, Image
# USE MDDialog TO SHOW DIALOG WINDOW OF RESULT OF JOB SEARCH
from kivymd.uix.dialog import MDDialog
# FROM kivy.lang IMPORT Builder THAT'S A METHOD TO CREATE THE TEXT INPUT
from kivy.lang import Builder
# USE glob() (BUILT IN FUNCTION IN PYTHON) TO SEARCH FILES INSIDE FOLDER USING JOB NAME.
import glob
# IMPORT err TO SHOW ERROR MESSAGE IF SOMETHING GET WRONG
from Tools.scripts.fixcid import err
# FROM kivy.uix.widget IMPORT Widget TO USE IT IN KEYBOARD FUNCTION
from kivy.uix.widget import Widget

#+++++-----------------------------+++++#
## CREATE TEXT INPUT FIELDS SEPARATELY FOR Directory Path AND Job Number TO USE THEM IN THE CLASS LATER
# TEXT INPUT FOR DIRECTORY PATH USING builder METHOD
# USED (text: "H:\CNCProgs") AS A DEFAULT TEXT INPUT CAUSE THIS IS THE PATH INCLUDE FOLDERS THAT HAVE ALL PROGRAMS, WE CAN CHANGE IT FROM THE APP DIRECT IF NEEDED
Directory_Path_builder = """       
MDTextField:
    hint_text: "Directory Path"
    text: "H:\CNCProgs"
    line_color_focus: 1, 1, 1, 1
    pos_hint: {'center_x': 0.5, 'center_y': 0.75}
    size_hint_x:None
    width:300
    height:50
"""
# TEXT INPUT FOR JOB NUMBER USING builder METHOD
# USED (helper_text_mode: "on_focus") TO SHOW MESSAGE OF (helper_text: "Enter job number without (P) nor any extension.") WHEN CLICK ON THE TEXT FIELD.
Job_Number_builder = """       
MDTextField:
    hint_text: "Enter Job Number"
    helper_text: "Enter job number without (P) nor any extension."
    helper_text_mode: "on_focus"
    line_color_focus: 1, 1, 1, 1
    pos_hint: {'center_x': 0.5, 'center_y': 0.70}
    size_hint_x:None
    width:300
    height:10
"""

#+++++-----------------------------+++++#
# CREATE CLASS WITH APP NAME ((MDApp) TO BUILD THE APP, (Widget) TO USE IT IN KEYBOARD FUNCTION)
class WisecoProgramsFinder(MDApp,Widget):
    # USED (build) METHOD AS FUNCTION TO BUILD THE APP.
    # USED (self) TO CONNECT THE ELEMENTS WITH EACH OTHER
    # (self PARAMETER IS A REFERENCE TO THE CURRENT INSTANCE OF CLASS, AND IT USED TO ACCESS VARIABLES THAT BELONGS TO THE CLASS.)
    def build(self):
        # TO CONTROL SIZE OF THE SCREEN (Window.size = (WIDTH, HEIGHT))
        Window.size = (900, 660)
        # TO CHOOSE BACKGROUND MODE OF APP WHETHER DARK OR LIGHT
        self.theme_cls.theme_style = "Dark"
        # TO SET DEFAULT COLOR OF APP ELEMENTS(LABELS,BUTTONS...ETC)
        self.theme_cls.primary_palette = "Red"
        # TO SET DEFAULT COLOR CONCENTRATION(DARKNESS AND BRIGHTNESS) OF APP ELEMENTS(LABELS,BUTTONS...ETC)
        self.theme_cls.primary_hue = "800"
        # TO DEFINE (Screen() THAT USED TO DISPLAY THE APP) AS (AppScreen) TO USE LATER
        AppScreen = Screen()

        ## BoxLayout FOR ENTIRE APP INCLUDE ALL WIDGETS AND ELEMENTS, SHOULD ADD ALL APP COMPONENTS FOR THIS BOX LAYOUT.
        # (orientation='vertical') TO ORGANIZE APP ELEMENTS VERTICALLY,
        # (spacing=20) TO MAKE SPACE BETWEEN APP ELEMENTS, (padding=15) TO MAKE SPACE BETWEEN WALL BORDERS AND APP ELEMENTS,
        # (md_bg_color= [32/255.0, 32/255.0, 32/255.0, 1]) TO CHANGE THE COLOR BY ADJUSTING RGB VALUE(CHECK: https://www.w3schools.com/colors/colors_picker.asp?colorhex=edfeff)
        AppBoxLayout = MDBoxLayout(orientation='vertical', spacing=20, padding=15 , md_bg_color= [32/255.0, 32/255.0, 32/255.0, 1])

        # TO ADD PICTURE FOR THE APP FROM WEBSITE
        AppImage = Image(source=r'H:\CNC_Programming\WisecoApplications\WisecoApplicationsLogo/Wiseco.gif',
                         size_hint_y=None, height=70, allow_stretch=True, pos_hint={'center_x': 0.5, 'center_y': 0.90},
                         color=[150/255.0, 0/255.0, 0/255.0, 1])
        # TO ADD AppImage TO AppBoxLayout TO DISPLAY IT IN THE APP SCREEN
        AppBoxLayout.add_widget(AppImage)

        # LOAD Directory_Path TEXT INPUT THAT CREATED ABOVE.
        self.Directory_Path = Builder.load_string(Directory_Path_builder)
        # TO ADD Directory_Path TO AppBoxLayout TO DISPLAY IT IN THE APP SCREEN.
        AppBoxLayout.add_widget(self.Directory_Path)

        # LOAD Job_Number TEXT INPUT THAT CREATED ABOVE.
        self.Job_Number = Builder.load_string(Job_Number_builder)
        # TO ADD Job_Number TO AppBoxLayout TO DISPLAY IT IN THE APP SCREEN.
        AppBoxLayout.add_widget(self.Job_Number)

        # CREATE BOX LAYOUT CONTAIN APP BUTTONS
        ButtonsBoxLayout = MDBoxLayout(spacing=10, pos_hint={'center_x': 0.396}, size_hint=(None, None), height=30)
        ## CREATE BUTTON TO SEARCH JOBS
        # (on_press=self.ResetMachinesLabels): WHEN PRESS THE BUTTON IT CALLED (ResetMachinesLabels) FUNCTION TO RESET MACHINE LABELS COLOR TO BE WHITE TO PREPARED TO NEXT SEARCH.
        # (on_release=self.SearchFile): WHEN RELEASE THE BUTTON IT CALLED (SearchFile) FUNCTION TO SEARCH JOB PROGRAMS AND ADJUST MACHINE LABELS COLOR DEPEND ON PROGRAMS AVAILABILITY.
        # USED (on_press AND on_release) TO GIVE CORRECT SEARCH RESULT IF USE SEARCH BUTTON WITHOUT RESET ANYTHING.
        Search_Button = MDRectangleFlatButton(text='Search', pos_hint={'center_x': 0.45, 'center_y': 0.5},
                                              on_press=self.ResetMachinesLabels, on_release=self.SearchFile)
        # TO ADD Search_Button TO ButtonsBoxLayout THAT CONTAIN APP BUTTONS.
        ButtonsBoxLayout.add_widget(Search_Button)
        # CREATE BUTTON TO RESET EVERYTHING TO START OVER
        # (on_press=self.ClearEverything): WHEN PRESS THE BUTTON IT CALLED (ClearEverything) FUNCTION TO RESET MACHINE LABELS COLOR TO BE WHITE AND MAKE JOB NUMBER FIELD EMPTY TO START OVER THE NEXT SEARCH.
        Reset_Button = MDRectangleFlatButton(text='Reset', pos_hint={'center_x': 0.55, 'center_y': 0.5},
                                              on_press=self.ClearEverything)
        # TO ADD Reset_Button TO ButtonsBoxLayout THAT CONTAIN APP BUTTONS.
        ButtonsBoxLayout.add_widget(Reset_Button)
        # CREATE BUTTON TO SHOW SEARCH RESULT
        # (on_press=self.ShowResult): WHEN PRESS THE BUTTON IT CALLED (ShowResult) FUNCTION TO CALL DIALOG WINDOW TO DISPLAY THE SEARCH RESULT.
        Show_Button = MDRectangleFlatButton(text='Show All', pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                        on_press=self.ShowResult)
        # TO ADD Show_Button TO ButtonsBoxLayout THAT CONTAIN APP BUTTONS.
        ButtonsBoxLayout.add_widget(Show_Button)
        # TO ADD ButtonsBoxLayout TO AppBoxLayout TO DISPLAY IT IN THE APP SCREEN
        AppBoxLayout.add_widget(ButtonsBoxLayout)

        # CREATE BOX LAYOUT CONTAIN COLORS GUIDE
        # USED MDGridLayout INSTEAD MDBoxLayout FOR ORGANIZATION PURPOSE.
        ColorBoxLayout = MDGridLayout(cols=3, spacing=5, pos_hint={'center_x': 0.34}, size_hint=(None, None), height=10)
        ## CREATE LABEL FOR Green COLOR THAT INDICATE PROGRAM EXIST IN FILE THAT USE TO RUN THE PROGRAM ON THE MACHINE
        # (text_color=(0, 1, 0, 1)) : IT IS RGB VALUE FOR GREEN COLOR
        # (font_style='Subtitle2') : IT IS CUSTOM FONT COMES WITH MDLabel
        Green_Color = MDLabel(text='Green: Running File', pos_hint={'center_x': 0.86},
                              size_hint=(None, None), width=130, height=10,
                              theme_text_color='Custom', text_color=(0, 1, 0, 1),
                              font_style='Subtitle2')
        # TO ADD Green_Color TO ColorBoxLayout THAT CONTAIN COLORS LABELS.
        ColorBoxLayout.add_widget(Green_Color)
        ## CREATE LABEL FOR Yellow COLOR THAT INDICATE PROGRAM EXIST IN ORIGINAL FILE THAT USE AS BACKUP FOLDER CONTAIN PROGRAMS.
        # (text_color=(1, 1, 0, 1)) : IT IS RGB VALUE FOR YELLOW COLOR
        # (font_style='Subtitle2') : IT IS CUSTOM FONT COMES WITH MDLabel
        Yellow_Color = MDLabel(text='Yellow: Original File', pos_hint={'center_x': 0.86},
                               size_hint=(None, None), width=130, height=10,
                               theme_text_color='Custom', text_color=(1, 1, 0, 1),
                               font_style='Subtitle2')
        # TO ADD YELLOW_Color TO ColorBoxLayout THAT CONTAIN COLORS LABELS.
        ColorBoxLayout.add_widget(Yellow_Color)
        ## CREATE LABEL FOR White COLOR THAT INDICATE PROGRAM NOT EXIST.
        # (text_color=(1, 1, 1, 1)) : IT IS RGB VALUE FOR WHITE COLOR
        # (font_style='Subtitle2') : IT IS CUSTOM FONT COMES WITH MDLabel
        White_Color = MDLabel(text='White: Not Exist', pos_hint={'center_x': 0.86},
                              size_hint=(None, None), width=130, height=10,
                              theme_text_color='Custom', text_color=(1, 1, 1, 1),
                              font_style='Subtitle2')  # , halign='left'
        # TO ADD WHITE_Color TO ColorBoxLayout THAT CONTAIN COLORS LABELS.
        ColorBoxLayout.add_widget(White_Color)
        # TO ADD ColorBoxLayout TO AppBoxLayout TO DISPLAY IT IN THE APP SCREEN
        AppBoxLayout.add_widget(ColorBoxLayout)

        # CREATE GRID LAYOUT CONTAIN DIFFERENT MACHINES OF THE SHOP
        # (cols=1) USED ONE COLUMNS THAT WILL CONTAIN MANY ROWS CONTAIN MACHINES SEPARATELY
        # (spacing=30) SPACING BETWEEN EACH ROW
        MachinesPrograms = MDGridLayout(cols=1, pos_hint={'center_x': 0.382}, spacing=30,
                                        size_hint=(None, None), width=500, height=280)
        # CREATE GRID LAYOUT WITH 1 COLUMN CONTAIN Programs List AS TITLE OF TABLE OF MACHINES
        MachinesProgramsTitleLabel = MDGridLayout(cols=1, pos_hint={'center_x': 0.4}, size_hint=(None, None), height=10)
        # CREATE ProgramsList BUTTON(USED BUTTON FOR FUTURE USE)
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.ProgramsList = MDRectangleFlatButton(text='Programs List', text_color=[1, 1, 1, 1],increment_width=617)
        # TO ADD ProgramsList LABEL(ACTUALLY BUTTON) TO MachinesProgramsTitleLabel THAT CONTAIN TITLE OF MACHINES TABLE.
        MachinesProgramsTitleLabel.add_widget(self.ProgramsList)
        # TO ADD MachinesProgramsTitleLabel TO MachinesPrograms THAT CONTAIN MACHINES OF THE SHOP.
        MachinesPrograms.add_widget(MachinesProgramsTitleLabel)
        #+++------+++#
        # CREATE GRID LAYOUT CONTAIN PIN BORE MACHINES
        # (cols=4) USED FOUR COLUMNS AND ONE ROW(DEFAULT) THAT CONTAIN PIN BORE MACHINES.
        PinBorePrograms = MDGridLayout(cols=4, pos_hint={'center_x': 0.4}, size_hint=(None, None), height=10)
        # CREATE Horebore BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE RUNNING FILE FOR HORIZONTAL MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.Horebore = MDRectangleFlatButton(text='HOREBORE', text_color=[1, 1, 1, 1],increment_width=87)
        # TO ADD Horebore LABEL(ACTUALLY BUTTON) TO PinBorePrograms THAT CONTAIN PIN BORE MACHINES.
        PinBorePrograms.add_widget(self.Horebore)
        # CREATE Horebore_Original BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE ORIGINAL FILE FOR HORIZONTAL MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.Horebore_Original = MDRectangleFlatButton(text='HOREBORE ORIGINAL', text_color=[1, 1, 1, 1],increment_width=38)
        # TO ADD Horebore_Original LABEL(ACTUALLY BUTTON) TO PinBorePrograms THAT CONTAIN PIN BORE MACHINES.
        PinBorePrograms.add_widget(self.Horebore_Original)
        # CREATE Horebore_127 BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE RUNNING FILE FOR HORIZONTAL 127 MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.Horebore_127 = MDRectangleFlatButton(text='HORIZONTAL 127', text_color=[1, 1, 1, 1], increment_width=62)
        # TO ADD Horebore_127 LABEL(ACTUALLY BUTTON) TO PinBorePrograms THAT CONTAIN PIN BORE MACHINES.
        PinBorePrograms.add_widget(self.Horebore_127)
        # CREATE Horebore_127_Original BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE ORIGINAL FILE FOR HORIZONTAL 127 MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.Horebore_127_Original = MDRectangleFlatButton(text='HORIZONTAL 127 ORIGINAL', text_color=[1, 1, 1, 1],increment_width=11)
        # TO ADD Horebore_127_Original LABEL(ACTUALLY BUTTON) TO PinBorePrograms THAT CONTAIN PIN BORE MACHINES.
        PinBorePrograms.add_widget(self.Horebore_127_Original)
        # TO ADD PinBorePrograms THAT CONTAIN PIN BORE MACHINES TO MachinesPrograms THAT CONTAIN MACHINES OF THE SHOP.
        MachinesPrograms.add_widget(PinBorePrograms)
        #+++------+++#
        # CREATE GRID LAYOUT CONTAIN PRIMARY LATHE MACHINES
        # (cols=4) USED FOUR COLUMNS AND ONE ROW(DEFAULT) THAT CONTAIN PRIMARY LATHE MACHINES.
        LathePrograms = MDGridLayout(cols=4, pos_hint={'center_x': 0.4}, size_hint=(None, None),height=10)
        # CREATE Okuma_Lathe BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE RUNNING FILE FOR OKUMA LATHE MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.Okuma_Lathe = MDRectangleFlatButton(text='Okuma LT Lathes', text_color=[1, 1, 1, 1], increment_width=51)
        # TO ADD Okuma_Lathe LABEL(ACTUALLY BUTTON) TO LathePrograms THAT CONTAIN PRIMARY LATHE MACHINES.
        LathePrograms.add_widget(self.Okuma_Lathe)
        # CREATE Okuma_Lathe_Original BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE ORIGINAL FILE FOR OKUMA LATHE MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.Okuma_Lathe_Original = MDRectangleFlatButton(text='Okuma LT Lathes Originals', text_color=[1, 1, 1, 1],increment_width=10)
        # TO ADD Okuma_Lathe_Original LABEL(ACTUALLY BUTTON) TO LathePrograms THAT CONTAIN PRIMARY LATHE MACHINES.
        LathePrograms.add_widget(self.Okuma_Lathe_Original)
        # CREATE Mazak BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE RUNNING FILE FOR MAZAK LATHE MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.Mazak = MDRectangleFlatButton(text='MazakLathe34', text_color=[1, 1, 1, 1], increment_width=81)
        # TO ADD Mazak LABEL(ACTUALLY BUTTON) TO LathePrograms THAT CONTAIN PRIMARY LATHE MACHINES.
        LathePrograms.add_widget(self.Mazak)
        # CREATE Mazak BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE ORIGINAL FILE FOR MAZAK LATHE MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.Mazak_Original = MDRectangleFlatButton(text='MazakLathe34 Originals', text_color=[1, 1, 1, 1],increment_width=38)
        # TO ADD Mazak_Original LABEL(ACTUALLY BUTTON) TO LathePrograms THAT CONTAIN PRIMARY LATHE MACHINES.
        LathePrograms.add_widget(self.Mazak_Original)
        # TO ADD LathePrograms THAT CONTAIN PRIMARY LATHE MACHINES TO MachinesPrograms THAT CONTAIN MACHINES OF THE SHOP.
        MachinesPrograms.add_widget(LathePrograms)
        #+++------+++#
        # CREATE GRID LAYOUT CONTAIN SECONDARY LATHE MACHINES
        # (cols=6) USED SIX COLUMNS AND ONE ROW(DEFAULT) THAT CONTAIN SECONDARY LATHE MACHINES.
        LathePrograms2 = MDGridLayout(cols=6, pos_hint={'center_x': 0.4}, size_hint=(None, None),height=10)
        # CREATE Multus Lathe BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE RUNNING FILE FOR Multus Lathe MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.Multus = MDRectangleFlatButton(text='Multus Lathe', text_color=[1, 1, 1, 1], increment_width=79)
        # TO ADD Multus LABEL(ACTUALLY BUTTON) TO LathePrograms2 THAT CONTAIN SECONDARY LATHE MACHINES.
        LathePrograms2.add_widget(self.Multus)
        # CREATE Multus_Original Lathe BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE ORIGINAL FILE FOR Multus Lathe MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.Multus_Original = MDRectangleFlatButton(text='Multus Lathe Original', text_color=[1, 1, 1, 1],increment_width=45)
        # TO ADD Multus_Original LABEL(ACTUALLY BUTTON) TO LathePrograms2 THAT CONTAIN SECONDARY LATHE MACHINES.
        LathePrograms2.add_widget(self.Multus_Original)
        # CREATE Lathe7 BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE RUNNING FILE FOR Lathe7 MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.Lathe7 = MDRectangleFlatButton(text='Lathe7', text_color=[1, 1, 1, 1],increment_width=0)
        # TO ADD Lathe7 LABEL(ACTUALLY BUTTON) TO LathePrograms2 THAT CONTAIN SECONDARY LATHE MACHINES.
        LathePrograms2.add_widget(self.Lathe7)
        # CREATE Lathe14 BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE RUNNING FILE FOR Lathe14 MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.Lathe14 = MDRectangleFlatButton(text='Lathe14', text_color=[1, 1, 1, 1],increment_width=0)
        # TO ADD Lathe14 LABEL(ACTUALLY BUTTON) TO LathePrograms2 THAT CONTAIN SECONDARY LATHE MACHINES.
        LathePrograms2.add_widget(self.Lathe14)
        # CREATE Lathe10 BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE RUNNING FILE FOR Lathe10 MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.Lathe10AS = MDRectangleFlatButton(text='Lathe10AS', text_color=[1, 1, 1, 1], increment_width=24)
        # TO ADD Lathe10 LABEL(ACTUALLY BUTTON) TO LathePrograms2 THAT CONTAIN SECONDARY LATHE MACHINES.
        LathePrograms2.add_widget(self.Lathe10AS)
        # CREATE Lathe11 BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE RUNNING FILE FOR Lathe11 MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.Lathe11AS = MDRectangleFlatButton(text='Lathe11AS', text_color=[1, 1, 1, 1], increment_width=28)
        # TO ADD Lathe11 LABEL(ACTUALLY BUTTON) TO LathePrograms2 THAT CONTAIN SECONDARY LATHE MACHINES.
        LathePrograms2.add_widget(self.Lathe11AS)
        # TO ADD LathePrograms2 THAT CONTAIN SECONDARY LATHE MACHINES TO MachinesPrograms THAT CONTAIN MACHINES OF THE SHOP.
        MachinesPrograms.add_widget(LathePrograms2)
        #+++------+++#
        # CREATE GRID LAYOUT CONTAIN MILLING MACHINES
        # (cols=5) USED FIVE COLUMNS AND ONE ROW(DEFAULT) THAT CONTAIN MILLING MACHINES.
        MillingPrograms = MDGridLayout(cols=5, pos_hint={'center_x': 0.4}, size_hint=(None, None),width=500, height=10)
        # CREATE Okuma_Dome BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE RUNNING FILE FOR OKUMA DOME MILLING MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.Okuma_Dome = MDRectangleFlatButton(text='Okuma Dome Mills', text_color=[1, 1, 1, 1], increment_width=47)
        # TO ADD Okuma_Dome LABEL(ACTUALLY BUTTON) TO MillingPrograms THAT CONTAIN MILLING MACHINES.
        MillingPrograms.add_widget(self.Okuma_Dome)
        # CREATE Okuma_Dome_Original BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE ORIGINAL FILE FOR OKUMA DOME MILLING MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.Okuma_Dome_Original = MDRectangleFlatButton(text='Okuma Dome Originals', text_color=[1, 1, 1, 1],increment_width=35)
        # TO ADD Okuma_Dome_Original LABEL(ACTUALLY BUTTON) TO MillingPrograms THAT CONTAIN MILLING MACHINES.
        MillingPrograms.add_widget(self.Okuma_Dome_Original)
        # CREATE Okuma_Skirt BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE RUNNING FILE FOR OKUMA SKIRT MILLING MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.Okuma_Skirt = MDRectangleFlatButton(text='Okuma Skirt Mills', text_color=[1, 1, 1, 1], increment_width=70)
        # TO ADD Okuma_Skirt LABEL(ACTUALLY BUTTON) TO MillingPrograms THAT CONTAIN MILLING MACHINES.
        MillingPrograms.add_widget(self.Okuma_Skirt)
        # CREATE Okuma_Skirt_Original BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE ORIGINAL FILE FOR OKUMA SKIRT MILLING MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.Okuma_Skirt_Original = MDRectangleFlatButton(text='Okuma Skirt Originals', text_color=[1, 1, 1, 1],increment_width=55)
        # TO ADD Okuma_Skirt_Original LABEL(ACTUALLY BUTTON) TO MillingPrograms THAT CONTAIN MILLING MACHINES.
        MillingPrograms.add_widget(self.Okuma_Skirt_Original)
        # TO ADD MillingPrograms THAT CONTAIN MILLING MACHINES TO MachinesPrograms THAT CONTAIN MACHINES OF THE SHOP.
        MachinesPrograms.add_widget(MillingPrograms)
        #+++------+++#
        # CREATE GRID LAYOUT CONTAIN OTHER PROGRAMS AND MACHINES
        # (cols=4) USED FOUR COLUMNS AND ONE ROW(DEFAULT) THAT CONTAIN OTHER PROGRAMS AND MACHINES.
        OtherPrograms = MDGridLayout(cols=4, pos_hint={'center_x': 0.4}, size_hint=(None, None), width=500,height=10)
        # CREATE OilHole2_3 BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE RUNNING FILE FOR OilHole2_3 FILE MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.OilHole2_3 = MDRectangleFlatButton(text='Oilhole2_3', text_color=[1, 1, 1, 1],increment_width=98)
        # TO ADD OilHole2_3 LABEL(ACTUALLY BUTTON) TO OtherPrograms THAT CONTAIN OTHER PROGRAMS AND MACHINES.
        OtherPrograms.add_widget(self.OilHole2_3)
        # CREATE OilHole2_3_AS BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE RUNNING FILE FOR OilHole2_3_AS (MOST LIKELY CUSTOM JOBS FILE) MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.OilHole2_3_AS = MDRectangleFlatButton(text='Oilhole2_3AS', text_color=[1, 1, 1, 1],increment_width=97)
        # TO ADD OilHole2_3_AS LABEL(ACTUALLY BUTTON) TO OtherPrograms THAT CONTAIN OTHER PROGRAMS AND MACHINES.
        OtherPrograms.add_widget(self.OilHole2_3_AS)
        # CREATE TOOL_18 BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE TOOL_18 EXISTENCE IN RUNNING SKIRT PROGRAM FILE.
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.TOOL_18 = MDRectangleFlatButton(text='TOOL 18', text_color=[1, 1, 1, 1],increment_width=122)
        # TO ADD TOOL_18 LABEL(ACTUALLY BUTTON) TO OtherPrograms THAT CONTAIN OTHER PROGRAMS AND MACHINES.
        OtherPrograms.add_widget(self.TOOL_18)
        # CREATE Takisawa_64 BUTTON(USED BUTTON FOR FUTURE USE) THAT INDICATE RUNNING FILE FOR Takisawa_64 FINISH TURN MACHINE
        # (increment_width): TO CONTROL THE WIDTH AND MAKE IT LINE UP WITH OTHER MACHINES LABELS
        self.Takisawa_64 = MDRectangleFlatButton(text='Takisawa 64', text_color=[1, 1, 1, 1],increment_width=109)
        # TO ADD Takisawa_64 LABEL(ACTUALLY BUTTON) TO OtherPrograms THAT CONTAIN OTHER PROGRAMS AND MACHINES.
        OtherPrograms.add_widget(self.Takisawa_64)
        # TO ADD OtherPrograms THAT CONTAIN OTHER PROGRAMS AND MACHINES TO MachinesPrograms THAT CONTAIN MACHINES OF THE SHOP.
        MachinesPrograms.add_widget(OtherPrograms)
        #+++-----+++#
        ## SAVE IT IN CASE NEEDED LATER
        ## CREATE GRIDLAYOUT CONTAIN OilHoles MACHINES
        # OilHolesPrograms = MDGridLayout(cols=2, pos_hint={'center_x': 0.4}, size_hint=(None, None),width=500, height=10)  # row_force_default=True, row_default_height=2
        ## CREATE GRIDLAYOUT CONTAIN FinishTurn MACHINES     SAVE IT FOR LATER
        # FinishTurnPrograms = MDGridLayout(cols=1, pos_hint={'center_x': 0.4}, size_hint=(None, None),width=500, height=10)  # row_force_default=True, row_default_height=2
        #+++-----+++#
        # ADD BOXLAYOUT OF MachinesPrograms THAT CONTAIN MACHINES OF THE SHOP TO AppBoxLayout TO DISPLAY IT IN THE APP SCREEN.
        AppBoxLayout.add_widget(MachinesPrograms)

        # DEFINE LIST WITH NAME result_of_existing_programs  OUTSIDE THE FUNCTIONS SECTION JUST TO AVOID HAVING ERROR IF WE PRESS Show All BUTTON BEFORE USE THE Search BUTTON
        # USED global TO BE ABLE USE THE LIST OUTSIDE THE FUNCTION
        global result_of_existing_programs
        # LIST TO STORE THE FOUND JOBS WITH WHOLE PATH INCLUDING FILE NAME
        result_of_existing_programs = []

        ## TO ADD DeveloperInfo TO THE APP.
        # ('\n') USED TO PRINT THE NEXT TEXT IN SEPARATE LINE
        # (halign='right') USED TO LOCATE THE LABEL ON THE RIGHT OF THE SCREEN
        # text_color=(175/255.0, 0/255.0, 0/255.0, 1)) : USED RGB VALUE METHOD TO CUSTOM A COLOR
        # (font_style='Subtitle2') : IT IS CUSTOM FONT COMES WITH MDLabel
        DeveloperInfo = MDLabel(text='Version 0.0.3               ''\n''Created by: Moemen Alatweh''\n'' malatweh@rwbteam.com   ', halign='right',
                                theme_text_color='Custom', text_color=(175/255.0, 0/255.0, 0/255.0, 1),
                                font_style='Caption')
        # ADD DeveloperInfo TO AppBoxLayout TO DISPLAY IT IN THE APP SCREEN.
        AppBoxLayout.add_widget(DeveloperInfo)

        # ADD AppBoxLayout THAT CONTAIN ALL ELEMENTS AND WIDGETS OF THE APP TO AppScreen TO DISPLAY IT IN THE APP SCREEN.
        AppScreen.add_widget(AppBoxLayout)

        # TO RETURN AppScreen OF build function TO DISPLAY IT IN THE APP SCREEN.
        return AppScreen

    #+++++-------FUNCTIONS SECTION-------+++++#

    # CREATE FUNCTION TO SEARCH THE JOBS
    # THIS FUNCTION CALLED WHEN USER CLICK THE SEARCH BUTTON OR, PRESS 'enter' KEY FROM KEYBOARD
    # WE USE glob() (BUILT IN FUNCTION IN PYTHON) TO SEARCH JOBS INSIDE THE DIRECTORY
    # ALL FUNCTIONS SHOULD HAVE (self, obj) AS PARAMETERS TO WORK
    def SearchFile(self, obj):
        # USED global TO BE ABLE USE THE LIST OUTSIDE THE FUNCTION
        global result_of_existing_programs
        # LIST TO STORE THE FOUND JOBS WITH WHOLE PATH INCLUDING FILE NAME
        result_of_existing_programs = []
        # USED FOR LOOP TO SEARCH JOBS AND STORE THEM IN result_of_existing_programs LIST TO USE IT TO CHECK PROGRAMS AVAILABILITY
        # WE USE (glob.glob) METHOD TO SEARCH IN SPECIFIC DIRECTORY FOR SPECIFIC FILE NAME
        # WE USE THIS METHOD (*\*) TO SEARCH INSIDE ALL SUBFOLDER OF H:\CNCProgs (ONE MORE DIRECTORY), EX: H:\CNCProgs\HOREBORE
        # WE PUT (*) AFTER FILE NAME TO SEARCH THE FILE EVEN WITH PART OF NAME, EX: WD-123 IT GIVES ALL RESULT OF WD-12345, WD-12315...ETC  >>>METHOD IS (Wildcard or asterisk is used to match zero or more characters)
        # (self.Directory_Path.text) : IT IS THE TEXT OF Directory_Path TEXTINPUT THAT'S CREATED IN TOP OF THE CODE
        # (self.Job_Number.text) : IT IS THE TEXT OF Job_Number TEXTINPUT THAT'S CREATED IN TOP OF THE CODE
        # (file) : IT IS JUST USED TO LOOP INSIDE THE FOR LOOP (LIKE: for n in numbers)
        for file in glob.glob(self.Directory_Path.text + '\*\*' + self.Job_Number.text + '*'):
            # TO APPEND(ADD) EACH PROGRAM THAT FOUND TO THE RESULT LIST
            result_of_existing_programs.append(file)
        # PRINT FOR TESTING
        print("Directory is: " + self.Directory_Path.text)
        print("Job is: " + self.Job_Number.text.upper())
        print(result_of_existing_programs)
        # TO CHECK LIST SIZE
        print(len(result_of_existing_programs))

        #+++-----FOR ALL MACHINES(FOLDERS) LOGIC-----+++#
        # AFTER SEARCHING IS DONE (FOR LOOP IS ENDING) AND SAVE ALL RESULTS IN THE LIST(result_of_existing_programs),
        # WE USE THE LIST TO CHECK EACH SPECIFIC PATH FOR EACH FOLDER IF IT EXIST IN THE RESULT LIST OR NOT
        # (self.Directory_Path.text) :  WE USE IT TO MAKE THE APP MORE FLEXIBLE IN CASE THE DIRECTORY CHANGED
        # (self.Job_Number.text.upper()) : WE USE upper() METHOD TO MAKE ALL LETTERS CAPITAL IN CASE USER ENTER SMALL LETTERS
        # (and self.Job_Number.text !='') : USED TO KEEP THE THE LOGIC FALSE IF TEXT FIELD OF Job_Number IS EMPTY
        # USED (or,and) IN IF LOGIC STATEMENT TO COVER ALL PROBABILITIES AND OPTIONS THAT PROGRAM COULD SAVED WITH,
        ## LIKE CAPITAL OR SMALL LETTERS OR TO0 AND TO180 FOR HOREBORE PROGRAMS OR LR FOR MILLING PROGRAMS.
        # WHEN LOGIC IS FALSE, MACHINE LABELS REMAIN IN THE WHITE COLOR THAT'S INDICATE NO PROGRAM FOUND.
        # WHEN LOGIC IS TRUE, MACHINE LABELS TURN ON GREEN AND YELLOW COLORS THAT INDICATE PROGRAM FOUND,
        ## AND PRINT MESSAGE ON PYTHON CONSOLE WITH FOLDERS THAT HAVE THE PROGRAM.

        #++---HOREBORE FILE---++#
        if ((((self.Directory_Path.text + '\\HOREBORE\\P' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HOREBORE\\P' + self.Job_Number.text.upper() + 'TO0.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HOREBORE\\P' + self.Job_Number.text.upper() + 'TO180.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HOREBORE\\P' + self.Job_Number.text.upper() + 'L.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HOREBORE\\P' + self.Job_Number.text.upper() + 'R.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\HOREBORE\\P' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HOREBORE\\P' + self.Job_Number.text.upper() + 'TO0.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HOREBORE\\P' + self.Job_Number.text.upper() + 'TO180.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HOREBORE\\P' + self.Job_Number.text.upper() + 'L.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HOREBORE\\P' + self.Job_Number.text.upper() + 'R.min') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\HOREBORE\\p' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HOREBORE\\p' + self.Job_Number.text.upper() + 'TO0.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HOREBORE\\p' + self.Job_Number.text.upper() + 'TO180.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HOREBORE\\p' + self.Job_Number.text.upper() + 'L.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HOREBORE\\p' + self.Job_Number.text.upper() + 'R.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\HOREBORE\\p' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HOREBORE\\p' + self.Job_Number.text.upper() + 'TO0.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HOREBORE\\p' + self.Job_Number.text.upper() + 'TO180.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HOREBORE\\p' + self.Job_Number.text.upper() + 'L.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HOREBORE\\p' + self.Job_Number.text.upper() + 'R.min') in result_of_existing_programs)) and (self.Job_Number.text !='')):
                print(self.Job_Number.text +' IS EXIST IN HOREBORE FOLDER')
                self.Horebore.text_color = (0.0, 1.0, 0.0, 1.0)

        #++---HOREBORE ORIGINAL FILE---++#
        if ((((self.Directory_Path.text + '\\HOREBORE ORIGINAL\\P' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HOREBORE ORIGINAL\\P' + self.Job_Number.text.upper() + 'TO0.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HOREBORE ORIGINAL\\P' + self.Job_Number.text.upper() + 'TO180.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HOREBORE ORIGINAL\\P' + self.Job_Number.text.upper() + 'L.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HOREBORE ORIGINAL\\P' + self.Job_Number.text.upper() + 'R.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\HOREBORE ORIGINAL\\P' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HOREBORE ORIGINAL\\P' + self.Job_Number.text.upper() + 'TO0.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HOREBORE ORIGINAL\\P' + self.Job_Number.text.upper() + 'TO180.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HOREBORE ORIGINAL\\P' + self.Job_Number.text.upper() + 'L.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HOREBORE ORIGINAL\\P' + self.Job_Number.text.upper() + 'R.min') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\HOREBORE ORIGINAL\\p' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HOREBORE ORIGINAL\\p' + self.Job_Number.text.upper() + 'TO0.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HOREBORE ORIGINAL\\p' + self.Job_Number.text.upper() + 'TO180.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HOREBORE ORIGINAL\\p' + self.Job_Number.text.upper() + 'L.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HOREBORE ORIGINAL\\p' + self.Job_Number.text.upper() + 'R.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\HOREBORE ORIGINAL\\p' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HOREBORE ORIGINAL\\p' + self.Job_Number.text.upper() + 'TO0.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HOREBORE ORIGINAL\\p' + self.Job_Number.text.upper() + 'TO180.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HOREBORE ORIGINAL\\p' + self.Job_Number.text.upper() + 'L.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HOREBORE ORIGINAL\\p' + self.Job_Number.text.upper() + 'R.min') in result_of_existing_programs)) and (self.Job_Number.text !='')):
                print(self.Job_Number.text +' IS EXIST IN HOREBORE ORIGINAL FOLDER')
                self.Horebore_Original.text_color = (1.0, 1.0, 0.0, 1.0)

        #++---HORIZONTAL 127 FILE---++#
        if ((((self.Directory_Path.text + '\\HORIZONTAL 127\\P' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HORIZONTAL 127\\P' + self.Job_Number.text.upper() + 'TO0.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HORIZONTAL 127\\P' + self.Job_Number.text.upper() + 'TO180.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HORIZONTAL 127\\P' + self.Job_Number.text.upper() + 'L.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HORIZONTAL 127\\P' + self.Job_Number.text.upper() + 'R.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\HORIZONTAL 127\\P' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HORIZONTAL 127\\P' + self.Job_Number.text.upper() + 'TO0.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HORIZONTAL 127\\P' + self.Job_Number.text.upper() + 'TO180.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HORIZONTAL 127\\P' + self.Job_Number.text.upper() + 'L.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HORIZONTAL 127\\P' + self.Job_Number.text.upper() + 'R.min') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\HORIZONTAL 127\\p' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HORIZONTAL 127\\p' + self.Job_Number.text.upper() + 'TO0.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HORIZONTAL 127\\p' + self.Job_Number.text.upper() + 'TO180.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HORIZONTAL 127\\p' + self.Job_Number.text.upper() + 'L.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HORIZONTAL 127\\p' + self.Job_Number.text.upper() + 'R.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\HORIZONTAL 127\\p' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HORIZONTAL 127\\p' + self.Job_Number.text.upper() + 'TO0.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HORIZONTAL 127\\p' + self.Job_Number.text.upper() + 'TO180.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HORIZONTAL 127\\p' + self.Job_Number.text.upper() + 'L.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HORIZONTAL 127\\p' + self.Job_Number.text.upper() + 'R.min') in result_of_existing_programs)) and (self.Job_Number.text !='')):
                print(self.Job_Number.text + ' IS EXIST IN HORIZONTAL 127 FOLDER')
                self.Horebore_127.text_color = (0.0, 1.0, 0.0, 1.0)

        #++---HORIZONTAL 127 ORIGINAL FILE---++#
        if ((((self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\P' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\P' + self.Job_Number.text.upper() + 'TO0.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\P' + self.Job_Number.text.upper() + 'TO180.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\P' + self.Job_Number.text.upper() + 'L.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\P' + self.Job_Number.text.upper() + 'R.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\P' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\P' + self.Job_Number.text.upper() + 'TO0.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\P' + self.Job_Number.text.upper() + 'TO180.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\P' + self.Job_Number.text.upper() + 'L.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\P' + self.Job_Number.text.upper() + 'R.min') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\p' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\p' + self.Job_Number.text.upper() + 'TO0.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\p' + self.Job_Number.text.upper() + 'TO180.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\p' + self.Job_Number.text.upper() + 'L.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\p' + self.Job_Number.text.upper() + 'R.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\p' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\p' + self.Job_Number.text.upper() + 'TO0.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\p' + self.Job_Number.text.upper() + 'TO180.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\p' + self.Job_Number.text.upper() + 'L.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\HORIZONTAL 127 ORIGINAL\\p' + self.Job_Number.text.upper() + 'R.min') in result_of_existing_programs)) and (self.Job_Number.text !='')):
                print(self.Job_Number.text + ' IS EXIST IN HORIZONTAL 127 ORIGINAL FOLDER')
                self.Horebore_127_Original.text_color = (1.0, 1.0, 0.0, 1.0)

        #++---Okuma LT Lathes FILE---++#
        if ((((self.Directory_Path.text + '\\Okuma LT Lathes\\P' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Okuma LT Lathes\\P' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Okuma LT Lathes\\p' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Okuma LT Lathes\\p' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs)) and (self.Job_Number.text !='')):
              print(self.Job_Number.text + ' IS EXIST IN Okuma LT Lathes FOLDER')
              self.Okuma_Lathe.text_color = (0.0, 1.0, 0.0, 1.0)

        #++---Okuma LT Lathes Originals FILE---++#
        if ((((self.Directory_Path.text + '\\Okuma LT Lathes Originals\\P' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Okuma LT Lathes Originals\\P' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Okuma LT Lathes Originals\\p' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Okuma LT Lathes Originals\\p' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs)) and (self.Job_Number.text !='')):
              print(self.Job_Number.text + ' IS EXIST IN Okuma LT Lathes Originals FOLDER')
              self.Okuma_Lathe_Original.text_color = (1.0, 1.0, 0.0, 1.0)

        #++---MazakLathe34 FILE---++#
        if ((((self.Directory_Path.text + '\\MazakLathe34\\' + self.Job_Number.text.upper()) in result_of_existing_programs)) and (self.Job_Number.text !='')):
              print(self.Job_Number.text + ' IS EXIST IN MazakLathe34 FOLDER')
              self.Mazak.text_color = (0.0, 1.0, 0.0, 1.0)

        #++---MazakLathe34 Originals FILE---++#
        if ((((self.Directory_Path.text + '\\MazakLathe34 Originals\\P' + self.Job_Number.text.upper() + '.EIA') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\MazakLathe34 Originals\\P' + self.Job_Number.text.upper() + '.eia') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\MazakLathe34 Originals\\p' + self.Job_Number.text.upper() + '.EIA') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\MazakLathe34 Originals\\p' + self.Job_Number.text.upper() + '.eia') in result_of_existing_programs)) and (self.Job_Number.text !='')):
              print(self.Job_Number.text + ' IS EXIST IN MazakLathe34 Originals FOLDER')
              self.Mazak_Original.text_color = (1.0, 1.0, 0.0, 1.0)

        #++---Multus FILE---++#
        if ((((self.Directory_Path.text + '\\Multus\\P' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Multus\\P' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Multus\\p' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Multus\\p' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs)) and (self.Job_Number.text !='')):
              print(self.Job_Number.text + ' IS EXIST IN Multus FOLDER')
              self.Multus.text_color = (0.0, 1.0, 0.0, 1.0)

        #++---Multus Original FILE---++#
        if ((((self.Directory_Path.text + '\\Multus Original\\P' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Multus Original\\P' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Multus Original\\p' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Multus Original\\p' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs)) and (self.Job_Number.text !='')):
              print(self.Job_Number.text + ' IS EXIST IN Multus Original FOLDER')
              self.Multus_Original.text_color = (1.0, 1.0, 0.0, 1.0)

        #++---Lathe7 FILE---++#
        if ((((self.Directory_Path.text + '\\Lathe7\\P' + self.Job_Number.text.upper()) in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Lathe7\\p' + self.Job_Number.text.upper()) in result_of_existing_programs)) and (self.Job_Number.text !='')):
                print(self.Job_Number.text + ' IS EXIST IN Lathe7 FOLDER')
                self.Lathe7.text_color = (0.0, 1.0, 0.0, 1.0)

        #++---Lathe10AS FILE---++#
        if ((((self.Directory_Path.text + '\\Lathe10AS\\P' + self.Job_Number.text.upper()) in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Lathe10AS\\p' + self.Job_Number.text.upper()) in result_of_existing_programs)) and (self.Job_Number.text !='')):
                print(self.Job_Number.text + ' IS EXIST IN Lathe10AS FOLDER')
                self.Lathe10AS.text_color = (0.0, 1.0, 0.0, 1.0)

        #++---Lathe11AS FILE---++#
        if ((((self.Directory_Path.text + '\\Lathe11AS\\P' + self.Job_Number.text.upper()) in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Lathe11AS\\p' + self.Job_Number.text.upper()) in result_of_existing_programs)) and (self.Job_Number.text !='')):
                print(self.Job_Number.text + ' IS EXIST IN Lathe11AS FOLDER')
                self.Lathe11AS.text_color = (0.0, 1.0, 0.0, 1.0)

        #++---Lathe14 FILE---++#
        if ((((self.Directory_Path.text + '\\Lathe14\\P' + self.Job_Number.text.upper()) in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Lathe14\\p' + self.Job_Number.text.upper()) in result_of_existing_programs)) and (self.Job_Number.text !='')):
                print(self.Job_Number.text + ' IS EXIST IN Lathe14 FOLDER')
                self.Lathe14.text_color = (0.0, 1.0, 0.0, 1.0)

        #++---Okuma Dome Mills FILE---++#
        if ((((self.Directory_Path.text + '\\Okuma Dome Mills\\P' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Dome Mills\\P' + self.Job_Number.text.upper() + 'LR.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Dome Mills\\P' + self.Job_Number.text.upper() + 'L.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\Okuma Dome Mills\\P' + self.Job_Number.text.upper() + 'R.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Okuma Dome Mills\\P' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Dome Mills\\P' + self.Job_Number.text.upper() + 'LR.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Dome Mills\\P' + self.Job_Number.text.upper() + 'L.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\Okuma Dome Mills\\P' + self.Job_Number.text.upper() + 'R.min') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Okuma Dome Mills\\p' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Dome Mills\\p' + self.Job_Number.text.upper() + 'LR.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Dome Mills\\p' + self.Job_Number.text.upper() + 'L.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\Okuma Dome Mills\\p' + self.Job_Number.text.upper() + 'R.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Okuma Dome Mills\\p' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Dome Mills\\p' + self.Job_Number.text.upper() + 'LR.min') in result_of_existing_programs)or
             ((self.Directory_Path.text + '\\Okuma Dome Mills\\p' + self.Job_Number.text.upper() + 'L.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\Okuma Dome Mills\\p' + self.Job_Number.text.upper() + 'R.min') in result_of_existing_programs)) and (self.Job_Number.text != '')):
                print(self.Job_Number.text + ' IS EXIST IN Okuma Dome Mills FOLDER')
                self.Okuma_Dome.text_color = (0.0, 1.0, 0.0, 1.0)

        #++---Okuma Dome Originals FILE---++#
        if ((((self.Directory_Path.text + '\\Okuma Dome Originals\\P' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Dome Originals\\P' + self.Job_Number.text.upper() + 'LR.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Dome Originals\\P' + self.Job_Number.text.upper() + 'L.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\Okuma Dome Originals\\P' + self.Job_Number.text.upper() + 'R.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Okuma Dome Originals\\P' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Dome Originals\\P' + self.Job_Number.text.upper() + 'LR.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Dome Originals\\P' + self.Job_Number.text.upper() + 'L.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\Okuma Dome Originals\\P' + self.Job_Number.text.upper() + 'R.min') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Okuma Dome Originals\\p' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Dome Originals\\p' + self.Job_Number.text.upper() + 'LR.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Dome Originals\\p' + self.Job_Number.text.upper() + 'L.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\Okuma Dome Originals\\p' + self.Job_Number.text.upper() + 'R.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Okuma Dome Originals\\p' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Dome Originals\\p' + self.Job_Number.text.upper() + 'LR.min') in result_of_existing_programs)or
             ((self.Directory_Path.text + '\\Okuma Dome Originals\\p' + self.Job_Number.text.upper() + 'L.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\Okuma Dome Originals\\p' + self.Job_Number.text.upper() + 'R.min') in result_of_existing_programs)) and (self.Job_Number.text != '')):
                print(self.Job_Number.text + ' IS EXIST IN Okuma Dome Originals FOLDER')
                self.Okuma_Dome_Original.text_color = (1.0, 1.0, 0.0, 1.0)

        #++---Okuma Skirt Mills FILE---++#
        if ((((self.Directory_Path.text + '\\Okuma Skirt Mills\\P' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Skirt Mills\\P' + self.Job_Number.text.upper() + 'LR.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Skirt Mills\\P' + self.Job_Number.text.upper() + 'L.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\Okuma Skirt Mills\\P' + self.Job_Number.text.upper() + 'R.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Okuma Skirt Mills\\P' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Skirt Mills\\P' + self.Job_Number.text.upper() + 'LR.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Skirt Mills\\P' + self.Job_Number.text.upper() + 'L.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\Okuma Skirt Mills\\P' + self.Job_Number.text.upper() + 'R.min') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Okuma Skirt Mills\\p' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Skirt Mills\\p' + self.Job_Number.text.upper() + 'LR.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Skirt Mills\\p' + self.Job_Number.text.upper() + 'L.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\Okuma Skirt Mills\\p' + self.Job_Number.text.upper() + 'R.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Okuma Skirt Mills\\p' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Skirt Mills\\p' + self.Job_Number.text.upper() + 'LR.min') in result_of_existing_programs)or
             ((self.Directory_Path.text + '\\Okuma Skirt Mills\\p' + self.Job_Number.text.upper() + 'L.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\Okuma Skirt Mills\\p' + self.Job_Number.text.upper() + 'R.min') in result_of_existing_programs)) and (self.Job_Number.text != '')):
                print(self.Job_Number.text + ' IS EXIST IN Okuma Skirt Mills FOLDER')
                self.Okuma_Skirt.text_color = (0.0, 1.0, 0.0, 1.0)

        #++---Okuma Skirt Originals FILE---++#
        if ((((self.Directory_Path.text + '\\Okuma Skirt Originals\\P' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Skirt Originals\\P' + self.Job_Number.text.upper() + 'LR.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Skirt Originals\\P' + self.Job_Number.text.upper() + 'L.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\Okuma Skirt Originals\\P' + self.Job_Number.text.upper() + 'R.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Okuma Skirt Originals\\P' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Skirt Originals\\P' + self.Job_Number.text.upper() + 'LR.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Skirt Originals\\P' + self.Job_Number.text.upper() + 'L.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\Okuma Skirt Originals\\P' + self.Job_Number.text.upper() + 'R.min') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Okuma Skirt Originals\\p' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Skirt Originals\\p' + self.Job_Number.text.upper() + 'LR.MIN') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Skirt Originals\\p' + self.Job_Number.text.upper() + 'L.MIN') in result_of_existing_programs and
              (self.Directory_Path.text + '\\Okuma Skirt Originals\\p' + self.Job_Number.text.upper() + 'R.MIN') in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Okuma Skirt Originals\\p' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) or
             ((self.Directory_Path.text + '\\Okuma Skirt Originals\\p' + self.Job_Number.text.upper() + 'LR.min') in result_of_existing_programs)or
             ((self.Directory_Path.text + '\\Okuma Skirt Originals\\p' + self.Job_Number.text.upper() + 'L.min') in result_of_existing_programs and
              (self.Directory_Path.text + '\\Okuma Skirt Originals\\p' + self.Job_Number.text.upper() + 'R.min') in result_of_existing_programs)) and (self.Job_Number.text != '')):
                print(self.Job_Number.text + ' IS EXIST IN Okuma Skirt Originals FOLDER')
                self.Okuma_Skirt_Original.text_color = (1.0, 1.0, 0.0, 1.0)

        #++---TOOL 18 LOGIC---++#
        # CODE BELOW TO CHECK IF JOB (THAT SAVED IN THE RUNNING FILE) HAVE TOOL 18 OR NOT
        # FIRST IT WILL CHECK IF WE HAVE OKUMA SKIRT PROGRAM OR NOT, WE USE IF, ELIF STATEMENT TO COVER ALL PROBABILITIES AND OPTIONS THAT SKIRT PROGRAM COULD SAVED WITH, LIKE CAPITAL OR SMALL LETTER OR LR(LIKE WD-12548LR)
        # IF WE HAVE ONE IT WILL OPEN THE PROGRAM AND READ EACH LINE AND ADD IT TO THE LIST(SkirtProgram[])
        # IT WILL USE find() METHOD (BUILT IN FUNCTION) THAT'S SEARCH SPECIFIC TEXT (IT IS "T18" IN OUR CASE)
        # IF FIND "T18" INSIDE THE PROGRAM(LIST(SkirtProgram[])) IT WILL TURN ON TOOL 18 LABEL TO GREEN COLOR AND PRINT MESSAGE IN PYTHON CONSOLE
        # IF NOT, NOTHING WILL HAPPEN AND TOOL 18 LABEL REMAIN IN WHITE COLOR(ie: PROGRAM DOESN'T HAVE T18)
        # (SkirtProgram = []) :  DECLARE AN EMPTY LIST TO ADD THE SKIRT PROGRAM LINES ONE BY ONE.
        # (substr = "T18") : SUBSTRING TO SEARCH FOR, IT IS "T18" IN OUR CASE
        # (with open( PATH FILE ,'rt') as CurrentProgram:): USED TO OPEN THE FILE AND CLOSE IT WHEN CODE BLOCK END, 'rt' MEAN READ TEXT, OPEN IT AS CurrentProgram TO USE IT IN THE FOR LOOP
        # (for line in CurrentProgram:) :  FOR LOOP TO READ EACH LINE INSIDE THE PROGRAM
        # (SkirtProgram.append(line.rstrip('\n')) ) : APPEND(ADD) EACH LINE TO LIST(SkirtProgram),
        # (line.rstrip('\n')) : THAT'S HOW THE CODE KNOW THE LINE END,WE COULD USE ANYTHING INSTEAD ('\n') TO STRIP THE LINES LILE ',' OR ''(JUST SPACE),....ETC
        # (while (index == -1):) : WE USE (index = -1) AS CONDITION IN while LOOP TO CHECK T18 , WHEN FIND "T18" THE index WILL CHANGE AND EXIT THE while LOOP
        # (for line in SkirtProgram:) : WE USE FOR LOOP INSIDE THE wile LOOP TO CHECK ALL LINES IN THE SKIRT PROGRAM,
        # find() FUNCTION WILL RETURN LOCATION(index) OF THE SUPSTRING WHEN FIND IT, IF DOESN'T FIND ANYTHING IT WILL RETURN (index = -1)
        # (index = line.find(substr)) : CHANGE INDEX VALUE DEPENS ON SEARCH RESULT, WHENEVER FIND "T18" THE INDEX WILL CHANG AND BE SOMTHING ELSE -1, THEN IT WILL CHECK FOR>>
        # >>(if (index != -1):) : IF INDEX CHANGED, IT WILL break AND EXIT THE while LOOP (ie: WE HAVE TOOL 18 IN THE PROGRAM)
        # IF FOR LOOP END AND DOESN'T FIND "T18" (ie: INDEX STILL EQUAL -1), IT WILL JUMP TO NEXT LINE OF>>
        # >>(if index == -1:) : AND BECAUSE (index = -1) IT WILL BREAK THE while LOOP AND THAT' MEAN PROGRAM DOESN'T HAVE T18 AND TOOL 18 LABEL REMAIN IN WHITE COLOR

        if (((self.Directory_Path.text + '\\Okuma Skirt Mills\\P' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) and (self.Job_Number.text != '')):
            SkirtProgram = []  # DECLARE AN EMPTY LIST TO ADD PROGRAMS LINES ONE BY ONE.
            substr = "T18"  # SUBSTRING TO SEARCH FOR, IT IS "T18" IN OUR CASE
            # OPEN SKIRT PROGRAM FOR READING THE LINES.
            with open(self.Directory_Path.text + '\\Okuma Skirt Mills\\P' + self.Job_Number.text.upper() + '.MIN','rt') as CurrentProgram:
                for line in CurrentProgram:  # For each line in the file,
                    SkirtProgram.append(line.rstrip('\n'))  # strip newline and add to list.
            index = -1  # DEFINE (index = -1) TO USE IT FOR SEARCH
            while (index == -1):  # WHILE IT DOES NOT FIND THE TEXT KEEP SEARCHING , find() FUNCTION RETURN (-1) IF DOESN'T FIND WHAT IT SEARCH FOR
                for line in SkirtProgram:
                    index = line.find(substr)
                    #print(line)    LEAVE IT IF NEED IT FOR TESTING
                    #print(index)   LEAVE IT IF NEED IT FOR TESTING
                    if (index != -1):
                        print("TOOL 18 FOUND, NO ACTION NEED IT")
                        self.TOOL_18.text_color = (0.0, 1.0, 0.0, 1.0)
                        break
                if index == -1:
                    print('TOOL 18 NOT FOUND, NEED TO ADD IT TO THE PROGRAM')
                    break
        elif (((self.Directory_Path.text + '\\Okuma Skirt Mills\\P' + self.Job_Number.text.upper() + 'LR.MIN') in result_of_existing_programs) and (self.Job_Number.text != '')):
            SkirtProgram = []  # DECLARE AN EMPTY LIST TO ADD PROGRAMS LINES ONE BY ONE.
            substr = "T18"  # substring to search for, IT IS "T18" IN OUR CASE
            with open(self.Directory_Path.text + '\\Okuma Skirt Mills\\P' + self.Job_Number.text.upper() + 'LR.MIN','rt') as CurrentProgram:  # OPEN SKIRT PROGRAM FOR READING THE LINES.
                for line in CurrentProgram:  # For each line in the file,
                    SkirtProgram.append(line.rstrip('\n'))  # strip newline and add to list.
            index = -1  # DEFINE (index = -1) TO USE IT FOR SEARCH
            while (index == -1):  # WHILE IT DOES NOT FIND THE TEXT KEEP SEARCHING , find() FUNCTION RETURN (-1) IF DOESN'T FIND WHAT IT SEARCH FOR
                for line in SkirtProgram:
                    index = line.find(substr)
                    #print(line)    LEAVE IT IF NEED IT FOR TESTING
                    #print(index)   LEAVE IT IF NEED IT FOR TESTING
                    if (index != -1):
                        print("TOOL 18 FOUND, NO ACTION NEED IT")
                        self.TOOL_18.text_color = (0.0, 1.0, 0.0, 1.0)
                        break
                if index == -1:
                    print('TOOL 18 NOT FOUND, NEED TO ADD IT TO THE PROGRAM')
                    break
        elif (((self.Directory_Path.text + '\\Okuma Skirt Mills\\P' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) and (self.Job_Number.text != '')):
            SkirtProgram = []  # DECLARE AN EMPTY LIST TO ADD PROGRAMS LINES ONE BY ONE.
            substr = "T18"  # substring to search for, IT IS "T18" IN OUR CASE
            with open(self.Directory_Path.text + '\\Okuma Skirt Mills\\P' + self.Job_Number.text.upper() + '.min','rt') as CurrentProgram:  # OPEN SKIRT PROGRAM FOR READING THE LINES.
                for line in CurrentProgram:  # For each line in the file,
                    SkirtProgram.append(line.rstrip('\n'))  # strip newline and add to list.
            index = -1  # DEFINE (index = -1) TO USE IT FOR SEARCH
            while (index == -1):  # WHILE IT DOES NOT FIND THE TEXT KEEP SEARCHING , find() FUNCTION RETURN (-1) IF DOESN'T FIND WHAT IT SEARCH FOR
                for line in SkirtProgram:
                    index = line.find(substr)
                    #print(line)    LEAVE IT IF NEED IT FOR TESTING
                    #print(index)   LEAVE IT IF NEED IT FOR TESTING
                    if (index != -1):
                        print("TOOL 18 FOUND, NO ACTION NEED IT")
                        self.TOOL_18.text_color = (0.0, 1.0, 0.0, 1.0)
                        break
                if index == -1:
                    print('TOOL 18 NOT FOUND, NEED TO ADD IT TO THE PROGRAM')
                    break
        elif (((self.Directory_Path.text + '\\Okuma Skirt Mills\\P' + self.Job_Number.text.upper() + 'LR.min') in result_of_existing_programs) and (self.Job_Number.text != '')):
            SkirtProgram = []  # DECLARE AN EMPTY LIST TO ADD PROGRAMS LINES ONE BY ONE.
            substr = "T18"  # substring to search for, IT IS "T18" IN OUR CASE
            with open(self.Directory_Path.text + '\\Okuma Skirt Mills\\P' + self.Job_Number.text.upper() + 'LR.min','rt') as CurrentProgram:  # OPEN SKIRT PROGRAM FOR READING THE LINES.
                for line in CurrentProgram:  # For each line in the file,
                    SkirtProgram.append(line.rstrip('\n'))  # strip newline and add to list.
            index = -1  # DEFINE (index = -1) TO USE IT FOR SEARCH
            while (index == -1):  # WHILE IT DOES NOT FIND THE TEXT KEEP SEARCHING , find() FUNCTION RETURN (-1) IF DOESN'T FIND WHAT IT SEARCH FOR
                for line in SkirtProgram:
                    index = line.find(substr)
                    #print(line)    LEAVE IT IF NEED IT FOR TESTING
                    #print(index)   LEAVE IT IF NEED IT FOR TESTING
                    if (index != -1):
                        print("TOOL 18 FOUND, NO ACTION NEED IT")
                        self.TOOL_18.text_color = (0.0, 1.0, 0.0, 1.0)
                        break
                if index == -1:
                    print('TOOL 18 NOT FOUND, NEED TO ADD IT TO THE PROGRAM')
                    break
        elif (((self.Directory_Path.text + '\\Okuma Skirt Mills\\p' + self.Job_Number.text.upper() + '.MIN') in result_of_existing_programs) and (self.Job_Number.text != '')):
            SkirtProgram = []  # DECLARE AN EMPTY LIST TO ADD PROGRAMS LINES ONE BY ONE.
            substr = "T18"  # substring to search for, IT IS "T18" IN OUR CASE
            with open(self.Directory_Path.text + '\\Okuma Skirt Mills\\p' + self.Job_Number.text.upper() + '.MIN','rt') as CurrentProgram:  # OPEN SKIRT PROGRAM FOR READING THE LINES.
                for line in CurrentProgram:  # For each line in the file,
                    SkirtProgram.append(line.rstrip('\n'))  # strip newline and add to list.
            index = -1  # DEFINE (index = -1) TO USE IT FOR SEARCH
            while (index == -1):  # WHILE IT DOES NOT FIND THE TEXT KEEP SEARCHING , find() FUNCTION RETURN (-1) IF DOESN'T FIND WHAT IT SEARCH FOR
                for line in SkirtProgram:
                    index = line.find(substr)
                    #print(line)    LEAVE IT IF NEED IT FOR TESTING
                    #print(index)   LEAVE IT IF NEED IT FOR TESTING
                    if (index != -1):
                        print("TOOL 18 FOUND, NO ACTION NEED IT")
                        self.TOOL_18.text_color = (0.0, 1.0, 0.0, 1.0)
                        break
                if index == -1:
                    print('TOOL 18 NOT FOUND, NEED TO ADD IT TO THE PROGRAM')
                    break
        elif (((self.Directory_Path.text + '\\Okuma Skirt Mills\\p' + self.Job_Number.text.upper() + 'LR.MIN') in result_of_existing_programs) and (self.Job_Number.text != '')):
            SkirtProgram = []  # DECLARE AN EMPTY LIST TO ADD PROGRAMS LINES ONE BY ONE.
            substr = "T18"  # substring to search for, IT IS "T18" IN OUR CASE
            with open(self.Directory_Path.text + '\\Okuma Skirt Mills\\p' + self.Job_Number.text.upper() + 'LR.MIN','rt') as CurrentProgram:  # OPEN SKIRT PROGRAM FOR READING THE LINES.
                for line in CurrentProgram:  # For each line in the file,
                    SkirtProgram.append(line.rstrip('\n'))  # strip newline and add to list.
            index = -1  # DEFINE (index = -1) TO USE IT FOR SEARCH
            while (index == -1):  # WHILE IT DOES NOT FIND THE TEXT KEEP SEARCHING , find() FUNCTION RETURN (-1) IF DOESN'T FIND WHAT IT SEARCH FOR
                for line in SkirtProgram:
                    index = line.find(substr)
                    #print(line)    LEAVE IT IF NEED IT FOR TESTING
                    #print(index)   LEAVE IT IF NEED IT FOR TESTING
                    if (index != -1):
                        print("TOOL 18 FOUND, NO ACTION NEED IT")
                        self.TOOL_18.text_color = (0.0, 1.0, 0.0, 1.0)
                        break
                if index == -1:
                    print('TOOL 18 NOT FOUND, NEED TO ADD IT TO THE PROGRAM')
                    break
        elif (((self.Directory_Path.text + '\\Okuma Skirt Mills\\p' + self.Job_Number.text.upper() + '.min') in result_of_existing_programs) and (self.Job_Number.text != '')):
            SkirtProgram = []  # DECLARE AN EMPTY LIST TO ADD PROGRAMS LINES ONE BY ONE.
            substr = "T18"  # substring to search for, IT IS "T18" IN OUR CASE
            with open(self.Directory_Path.text + '\\Okuma Skirt Mills\\p' + self.Job_Number.text.upper() + '.min','rt') as CurrentProgram:  # OPEN SKIRT PROGRAM FOR READING THE LINES.
                for line in CurrentProgram:  # For each line in the file,
                    SkirtProgram.append(line.rstrip('\n'))  # strip newline and add to list.
            index = -1  # DEFINE (index = -1) TO USE IT FOR SEARCH
            while (index == -1):  # WHILE IT DOES NOT FIND THE TEXT KEEP SEARCHING , find() FUNCTION RETURN (-1) IF DOESN'T FIND WHAT IT SEARCH FOR
                for line in SkirtProgram:
                    index = line.find(substr)
                    #print(line)    LEAVE IT IF NEED IT FOR TESTING
                    #print(index)   LEAVE IT IF NEED IT FOR TESTING
                    if (index != -1):
                        print("TOOL 18 FOUND, NO ACTION NEED IT")
                        self.TOOL_18.text_color = (0.0, 1.0, 0.0, 1.0)
                        break
                if index == -1:
                    print('TOOL 18 NOT FOUND, NEED TO ADD IT TO THE PROGRAM')
                    break
        elif (((self.Directory_Path.text + '\\Okuma Skirt Mills\\p' + self.Job_Number.text.upper() + 'LR.min') in result_of_existing_programs) and (self.Job_Number.text != '')):
            SkirtProgram = []  # DECLARE AN EMPTY LIST TO ADD PROGRAMS LINES ONE BY ONE.
            substr = "T18"  # substring to search for, IT IS "T18" IN OUR CASE
            with open(self.Directory_Path.text + '\\Okuma Skirt Mills\\p' + self.Job_Number.text.upper() + 'LR.min','rt') as CurrentProgram:  # OPEN SKIRT PROGRAM FOR READING THE LINES.
                for line in CurrentProgram:  # For each line in the file,
                    SkirtProgram.append(line.rstrip('\n'))  # strip newline and add to list.
            index = -1  # DEFINE (index = -1) TO USE IT FOR SEARCH
            while (index == -1):  # WHILE IT DOES NOT FIND THE TEXT KEEP SEARCHING , find() FUNCTION RETURN (-1) IF DOESN'T FIND WHAT IT SEARCH FOR
                for line in SkirtProgram:
                    index = line.find(substr)
                    #print(line)    LEAVE IT IF NEED IT FOR TESTING
                    #print(index)   LEAVE IT IF NEED IT FOR TESTING
                    if (index != -1):
                        print("TOOL 18 FOUND, NO ACTION NEED IT")
                        self.TOOL_18.text_color = (0.0, 1.0, 0.0, 1.0)
                        break
                if index == -1:
                    print('TOOL 18 NOT FOUND, NEED TO ADD IT TO THE PROGRAM')
                    break

        # Oilhole2_3 FILE
        if ((((self.Directory_Path.text + '\\Oilhole2_3\\P' + self.Job_Number.text.upper()) in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Oilhole2_3\\p' + self.Job_Number.text.upper()) in result_of_existing_programs)) and (self.Job_Number.text != '')):
                print(self.Job_Number.text + ' IS EXIST IN Oilhole2_3 FOLDER')
                self.OilHole2_3.text_color = (0.0, 1.0, 0.0, 1.0)

        # Oilhole2_3AS FILE
        if ((((self.Directory_Path.text + '\\Oilhole2_3AS\\P' + self.Job_Number.text.upper()) in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Oilhole2_3AS\\p' + self.Job_Number.text.upper()) in result_of_existing_programs)) and (self.Job_Number.text != '')):
                print(self.Job_Number.text + ' IS EXIST IN Oilhole2_3AS FOLDER')
                self.OilHole2_3_AS.text_color = (0.0, 1.0, 0.0, 1.0)

        # Takisawa 64 FILE
        if ((((self.Directory_Path.text + '\\Takisawa 64\\P' + self.Job_Number.text.upper()) in result_of_existing_programs) or
            ((self.Directory_Path.text + '\\Takisawa 64\\p' + self.Job_Number.text.upper()) in result_of_existing_programs)) and (self.Job_Number.text != '')):
                print(self.Job_Number.text + ' IS EXIST IN Takisawa 64 FOLDER')
                self.Takisawa_64.text_color = (0.0, 1.0, 0.0, 1.0)

        # IF USER CLICK SEARCH BUTTON AND THERE ARE NO DIRECTORY PATH OR JOB NUMBER ENTERED IN TEXT FIELDS,THEN GO TO (ShowResult) FUNCTION TO SHOW MESSAGE THAT NEED TO ENTER THEM
        # (self.ShowResult(obj)) : NEED TO PUT (obj) TO USE THE FUNCTION
        if ((self.Directory_Path.text == "") or (self.Job_Number.text == "")):
            self.ShowResult(obj)
        # IF USER CLICK SEARCH BUTTON AND THERE IS NO PROGRAM FOUND(ie:RESULT LIST IS EMPTY),THEN GO TO (ShowResult) FUNCTION TO SHOW MESSAGE OF NO PROGRAM FOUND
        elif ((result_of_existing_programs == [])):
            self.ShowResult(obj)

    # CREATE FUNCTION TO RESET MACHINE LABELS COLOR TO BACK TO WHITE, TO LET USER CAN USE SEARCH BUTTON TO SEARCH JOB WITHOUT CLICK ON RESET BUTTON EVERY TIME
    # THIS FUNCTION CALLED WHEN USER PRESS THE SEARCH BUTTON(BEFORE RELEASE IT)
    def ResetMachinesLabels(self, obj):
        self.Horebore.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Horebore_Original.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Horebore_127.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Horebore_127_Original.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Okuma_Lathe.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Okuma_Lathe_Original.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Mazak.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Mazak_Original.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Multus.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Multus_Original.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Lathe7.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Lathe10AS.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Lathe11AS.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Lathe14.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Okuma_Dome.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Okuma_Dome_Original.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Okuma_Skirt.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Okuma_Skirt_Original.text_color = (1.0, 1.0, 1.0, 1.0)
        self.TOOL_18.text_color = (1.0, 1.0, 1.0, 1.0)
        self.OilHole2_3.text_color = (1.0, 1.0, 1.0, 1.0)
        self.OilHole2_3_AS.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Takisawa_64.text_color = (1.0, 1.0, 1.0, 1.0)

    # CREATE FUNCTION TO CLEAR MACHINE LABELS COLOR TO BACK TO WHITE AND CLEAR JOB NUMBER FIELD TO BE EMPTY, TO START OVER THE SEARCH.
    # THIS FUNCTION CALLED WHEN USER PRESS THE RESET BUTTON, OR PRESS 'escabe' KEY FROM KEYBOARD
    def ClearEverything(self, obj):
        self.Job_Number.text = ''
        self.Horebore.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Horebore_Original.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Horebore_127.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Horebore_127_Original.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Okuma_Lathe.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Okuma_Lathe_Original.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Mazak.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Mazak_Original.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Multus.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Multus_Original.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Lathe7.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Lathe10AS.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Lathe11AS.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Lathe14.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Okuma_Dome.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Okuma_Dome_Original.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Okuma_Skirt.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Okuma_Skirt_Original.text_color = (1.0, 1.0, 1.0, 1.0)
        self.TOOL_18.text_color = (1.0, 1.0, 1.0, 1.0)
        self.OilHole2_3.text_color = (1.0, 1.0, 1.0, 1.0)
        self.OilHole2_3_AS.text_color = (1.0, 1.0, 1.0, 1.0)
        self.Takisawa_64.text_color = (1.0, 1.0, 1.0, 1.0)

    # CREATE FUNCTION TO DISPLAY ALL FOLDERS FOUND THAT HAVE THE JOB, AND SHOW THEN IN DIALOG WINDOW
    # THIS FUNCTION CALLED WHEN USER PRESS THE SHOW ALL BUTTON, OR PRESS 'enter' KEY FROM KEYBOARD AND NO PROGRAM FOUND OR NEED TO ENTER THE DIRECTORY OR JOB NUMBER
    def ShowResult(self, obj):
        # print('ShowResult function called') LEAVE IT IN CASE NEED IT FOR TESTING

        # WE DEFINE LINE BELOW TO CHECK IF DIALOG WINDOW CLOSED OR NOT, NEED IT TO AVOID DUPLICATE DIALOG WINDOW IF USER PRESS enter KEY WHILE IT IS OPEN
        # MAKE IT True TO INDICATE THE DIALOG WINDOW IS OPEN
        self.CloseDialog_has_been_called = True

        # CREATE CLOSE BUTTON INSIDE THE DIALOG WINDOW
        # WHEN PRESS THE BUTTON , IT CALLED CloseDialog FUNCTION TO CLOSE THE DIALOG WINDOW
        Close_Button= MDRectangleFlatButton(text='Close', on_release=self.CloseDialog)
        # IF DIRECTORY OR JOB NUMBER FIELDS ARE EMPTY, IT WILL OPEN THE DIALOG WITH MESSAGE THAT NEED TO ENTER THEM
        # ('[color=ffffff]Programs Found:[/color]'): TO CHANGE COLOR OF title TEXT, (ffffff): IS THE WHITE COLOR
        # (auto_dismiss= False) : TO TURN OFF THE AUTO CLOSE DIALOG WHEN USER CLICK ON SPACE,*ie: THE ONLY WAY TO CLOSE IT TO CLICK THE Close BUTTOM*
        if ((self.Directory_Path.text is "") or (self.Job_Number.text is "")):
            self.Search_Result = MDDialog(title='[color=ffffff]Programs Found:[/color]', text=("Please Enter Directory Path and Job Number"),
                                          size_hint=(0.7, 1.0), buttons=[Close_Button], auto_dismiss= False)
            # TO OPEN THE DIALOG WINDOW
            self.Search_Result.open()

        # IF THERE IS NO PROGRAM FOUND(ie:RESULT LIST IS EMPTY), IT WILL OPEN THE DIALOG WITH MESSAGE THAT "NO Programs Found"
        elif ((result_of_existing_programs == [])):
            self.Search_Result = MDDialog(title='[color=ffffff]Programs Found:[/color]', text=("NO Programs Found"),
                                          size_hint=(0.7, 1.0), buttons=[Close_Button], auto_dismiss= False)
            # TO OPEN THE DIALOG WINDOW
            self.Search_Result.open()

        # IF THERE ARE PROGRAM FOUND(ie:RESULT LIST IS NOT EMPTY) AND LENGTH OF LEST IS LESS THAN 50(MAX LINES CAN DIALOG SHOW)
        # THEN SHOW ALL PROGRAMS FOUND IN DIALOG WINDOW
        # ('\n'.join(result_of_existing_programs) : IT USED TO PRINT EACH ITEM IN THE LIST IN SEPARATE LINE INSTEAD ALL OF THEM IN THE SAME LINE(THE DEFAULT)
        elif ((result_of_existing_programs != []) and len(result_of_existing_programs) <= 50):
            self.Search_Result = MDDialog(title='[color=ffffff]Programs Found:[/color]',
                                          text=('[color=ffffff]' + '\n'.join(result_of_existing_programs) + '[/color]'),
                                          size_hint=(0.7, 1.0), buttons=[Close_Button])
            # TO OPEN THE DIALOG WINDOW
            self.Search_Result.open()

        # IF THERE ARE PROGRAM FOUND(ie:RESULT LIST IS NOT EMPTY) AND LENGTH OF LEST IS MORE THAN OR EQUAL 50(MAX LINES CAN DIALOG SHOW)
        # THEN, IT WILL OPEN THE DIALOG WITH MESSAGE SAYS THAT CANT SHOW THE RESULT AND NEED TO BE MORE SPECIFIC, NEED TO AVOID APP CRASH FOR EXCEEDING MEMORY
        elif ((result_of_existing_programs != []) and len(result_of_existing_programs) >= 50):
            print('Results is more than the window can display, Please be more SPECIFIC. /    ^__^    \ ')
            self.Search_Result = MDDialog(title='[color=ffffff]Programs Found:[/color]', text=("Results is more than the window can display, Please be more SPECIFIC. /    ^__^    \ "),
                                            size_hint=(0.7, 1.0), buttons=[Close_Button], auto_dismiss= False)
            # TO OPEN THE DIALOG WINDOW
            self.Search_Result.open()

        else:
            try:
                pass
            # TO HANDLE ALL KINDS OF ERRORS COULD HAPPEN
            except (RuntimeError, TypeError, NameError,ValueError,SyntaxError, OSError ,ImportError,IndexError,KeyError,KeyboardInterrupt,
                    NotImplementedError,MemoryError, ZeroDivisionError,FileNotFoundError,AssertionError,AttributeError,EOFError,FloatingPointError,
                    GeneratorExit,OverflowError,ReferenceError,StopIteration,IndentationError,TabError,SystemError,SystemExit,UnboundLocalError,
                    UnicodeError,UnicodeEncodeError,UnicodeDecodeError,UnicodeTranslateError,):
                self.Search_Result = MDDialog(title='[color=990000]Warning Message[/color]', text=("Unexpected error:", err),
                                              size_hint=(0.7, 1.0), buttons=[Close_Button], auto_dismiss= False)
                # TO OPEN THE RESULT WINDOW
                self.Search_Result.open()

    # CREATE FUNCTION TO CLOSE THE DIALOG WINDOW
    # FUNCTION CALLED WHEN USER PRESS CLOSE BUTTON,OR PRESS 'escabe' KEY FROM KEYBOARD WHILE THE DIALOG IS OPEN
    # (self.Search_Result.dismiss()): dismiss() USED AS CLOSE FUNCTION
    def CloseDialog(self, obj):
        self.Search_Result.dismiss()
        # WE DEFINE LINE BELOW TO CHECK IF DIALOG WINDOW CLOSED OR NOT, NEED IT TO AVOID DUPLICATE DIALOG WINDOW IF USER PRESS enter KEY WHILE IT IS OPEN
        # MAKE IT False TO INDICATE THE DIALOG WINDOW IS CLOSE
        self.CloseDialog_has_been_called = False

    # WE USE BUILT IN FUNCTIONS INSIDE KIVY TO USE THE KEYBOARD
    # (super(WisecoProgramsFinder, self).__init__(**kwargs)) : WisecoProgramsFinder IS THE CLASS NAME
    def __init__(self, **kwargs):
        super(WisecoProgramsFinder, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        ## LEAVE IN CASE NEED IT LATER
        # if self._keyboard.widget:
        #     # If it exists, this widget is a VKeyboard object which you can use           __init__    _keyboard_closed    _on_keyboard_down
        #     # to change the keyboard layout.
        #     pass
        ## TO ACTIVATE THE KEYBOARD TO BE ABLE TO USE
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        # WE DEFINE LINE BELOW TO CHECK IF DIALOG WINDOW CLOSED OR NOT, NEED IT TO AVOID DUPLICATE DIALOG WINDOW IF USER PRESS enter KEY WHILE IT IS OPEN
        # MAKE IT False TO INDICATE THE DIALOG WINDOW IS CLOSE, (PROBABLY THE START POINT)
        self.CloseDialog_has_been_called = False

    # IT WILL NOT DO ANYTHING BUT WE NEED IT THERE TO MAKE KEYBOARD FUNCTIONS WORK
    def _keyboard_closed(self):
        pass
        ## LEAVE IN CASE NEED IT LATER
        # print('My keyboard have been closed!')
        # self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        #     self.__init__()
        # self._keyboard = None

    # FUNCTION THAT READ THE KEYBOARD KEYS
    # FUNCTION CALLED WHEN PRESS ANY KEY FROM KEYBOARD
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('The key', keycode, 'have been pressed')
        ## LEAVE IN CASE NEED IT LATER
        # print(' - text is %r' % text)
        # print(' - modifiers are %r' % modifiers)

        ## Keycode[integer, 'text'] is Tubal HAVE TOW PARAMETERS,(integer) IS THE KEY UNICODE VALUE,AND ('text') IS DESCRIPTION OF THE KEY
        # IF WE PRESSED escape KEY,AND DIALOG WINDOW IS OPEN (True INDICATE THE DIALOG WINDOW IS OPEN)
        # THEN IT WILL CALL CloseDialog FUNCTION TO CLOSE THE DIALOG WINDOW
        # (self.CloseDialog(object)) : WE NEED TO USE (object) BECAUSE WE CALL IT INSIDE ANOTHER FUNCTION
        if ((keycode[1] == 'escape') and (self.CloseDialog_has_been_called == True)):
            print("Escape KEY PRESSED TO CLOSE THE DIALOG WINDOW")
            self.CloseDialog(object)

        # IF WE PRESSED escape KEY,AND DIALOG WINDOW IS CLOSED (False INDICATE THE DIALOG WINDOW IS CLOSED)
        # THEN IT WILL CALL ClearEverything FUNCTION TO CLEAR EVERYTHING AND START OVER THE SEARCH
        # (self.ClearEverything(object)) : WE NEED TO USE (object) BECAUSE WE CALL IT INSIDE ANOTHER FUNCTION
        elif ((keycode[1] == 'escape') and (self.CloseDialog_has_been_called == False)):
            print("Escape KEY PRESSED TO CLEAR EVERYTHING")
            self.ClearEverything(object)

        # IF WE PRESSED enter KEY,AND DIALOG WINDOW IS CLOSED (False INDICATE THE DIALOG WINDOW IS CLOSED)>>
        # >>(NEED THIS CONDITION TO AVOID DUPLICATE DIALOG WINDOW IF USER PRESS enter KEY WHILE IT IS OPEN)
        # THEN IT WILL CALL self.ResetMachinesLabels(object) TO RESET THE COLORS TO WHITE,AND self.SearchFile(object) TO SEARCH THE JOB
        # ('enter') : INDICATE THE ENTER KEY THAT NEAR THE LETTERS, ('numpadenter') : INDICATE THE ENTER KEY THAT NEAR THE NUMBERS ON KEYBOARD
        if ((keycode[1] == 'enter' or keycode[1] == 'numpadenter') and (self.CloseDialog_has_been_called == False)):
            print("Enter KEY BUTTON HAS BEEN PRESSED")
            self.ResetMachinesLabels(object)
            self.SearchFile(object)

        # IF WE PRESSED tab KEY, IT WILL FOCUS ON JOB NUMBER FIELD TO LET USER ABLE TO ENTER THE JOB NUMBER WITHOUT USE THE MOUSE EVERY TIME
        # (self.Job_Number.focus = True) : IT WILL ACTIVATE THE FOCUS MODE ON JOB NUMBER FIELD
        if (keycode[1]=='tab'):
            print('Tap KEY BUTTON HAS BEEN PRESSED')
            self.Job_Number.focus = True
        # RETURN True OF (_on_keyboard_down) FUNCTION TO ACCEPT THE KEY. OTHERWISE,IT WILL USED BY THE SYSTEM.
        return True

## LEAVE IT IN CASE WE NEED IT LATER
# if __name__ == '__Main__':
## TO BE ABLE RUN THE APP
WisecoProgramsFinder().run()
#+++++-------Code Ending-------+++++#


#+++++-------RESOURCES-------+++++#
## Kivy Website
# https://kivy.org/doc/stable/#
## KivyMD Website
# https://kivymd.readthedocs.io/en/latest/
## Fixed window size for Kivy programs
# https://stackoverflow.com/questions/37164410/fixed-window-size-for-kivy-programs
## Keyboard Function
# https://kivy.org/doc/stable/api-kivy.core.window.html
## Kivy Tutorial
# https://www.youtube.com/watch?v=RYF73CKGV6c
#++-----++#
## Python Glob() Function To Match Path, Directory, File Names with Examples
# https://www.poftut.com/python-glob-function-to-match-path-directory-file-names-with-examples/
# https://pymotw.com/2/glob/
## How to extract specific portions of a text file using Python
# https://www.computerhope.com/issues/ch001721.htm
## Find size of a list in Python
# https://www.geeksforgeeks.org/find-size-of-a-ist-in-python/
## Python — How to Tell if a Function Has Been Called
# https://dzone.com/articles/python-how-to-tell-if-a-function-has-been-called
## Print lists in Python (4 Different Ways)
# https://www.geeksforgeeks.org/print-lists-in-python-4-different-ways/
## Python Errors and Built-in Exceptions
# https://www.programiz.com/python-programming/exceptions
## Colors RGB
# https://www.w3schools.com/colors/colors_rgb.asp

