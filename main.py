import pygame
from datetime import datetime,date,timedelta
from math import sqrt,floor
from Events import *
from TimeTable import TimeTable as TTable
from TimeTable import *

# Initialize pygame
pygame.init()

# Window
window_width = 1000
window_height = 600
white_background = (255, 255, 255)
screen = pygame.display.set_mode((window_width, window_height))
screen.fill(white_background)
pygame.display.set_caption("Planner")

# Colours
Dark_Gray = (64, 64, 64)
Light_Gray = (192, 192, 192)
Slate_Gray = (112, 128, 144)
Charcoal = (54, 69, 79)
Steel_Blue = (70, 130, 180)
Navy_Blue = (0, 0, 128)
Royal_Blue = (65, 105, 225)
Deep_Green = (0, 100, 0)
Olive_Green = (128, 128, 0)
Burgundy = (128, 0, 32)

# Events
DymEvents = []
FixEvents = []

# timetable boxes
timetable_y_pos = 50

# UserGUI Variables
font_size = int(0.02 * sqrt(window_width ** 2 + window_height ** 2))
Small_font = pygame.font.Font(None, int(0.8 * font_size))
test_font = pygame.font.Font(None, font_size)
UserEventGUI = False



# Button
class SideButton:
    def __init__(self, position_x, position_y, width_x, height_y, text):
        self.x = position_x
        self.y = position_y
        self.height = height_y
        self.width = width_x
        self.colour = (200,0,0)
        self.text = text
        self.surface = pygame.Surface((width_x, height_y))
        self.isClicked = False
        self.isHovered = False

    def draw(self, screen):
        if self.isHovered:
            button_color = (160, 0, 0)  # Change color if hovered over
        else:
            button_color = self.colour
        pygame.draw.rect(self.surface, button_color, pygame.Rect(0, 0, self.width, self.height))
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 2))
        self.surface.blit(text_surface, text_rect)
        screen.blit(self.surface, (self.x, self.y))  # Blit the button surface onto the screen

    def is_clicked(self, mouse_pos):
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return button_rect.collidepoint(mouse_pos)

    def is_hovered_over(self, mouse_pos):
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return button_rect.collidepoint(mouse_pos)

#scroll bar
class scrollBar:
    def __init__(self, position_x, position_y, width_x, height_y):
        self.x = position_x
        self.y = position_y
        self.width = width_x
        self.height = height_y
        #self.icon = icon
        self.isHovered = False
        self.isClicked = False
        self.colour = (220,220,220)
        self.bar_colour = (169,169,169)
        self.bar_pos_x = position_x
        self.bar_pos_y = position_y
        self.bar_height = 75
        self.barisDragged = False
        self.offset_x = 0
        self.offset_y = 0

    def draw(self,screen):
        if(self.isHovered):
            self.bar_colour = (64,64,64)
        else:
            self.bar_colour = (169,169,169)
        pygame.draw.rect(screen, self.colour, pygame.Rect(self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen,self.bar_colour,pygame.Rect(self.bar_pos_x,self.bar_pos_y,self.width,self.bar_height))

    def is_hovered_over(self,mouse_pos):
        scroll_bar_rect = pygame.Rect(self.bar_pos_x,self.bar_pos_y,self.width,self.bar_height)
        return scroll_bar_rect.collidepoint(mouse_pos)

    def is_dragged(self,mouse_pos):
        scroll_bar_rect = pygame.Rect(self.bar_pos_x, self.bar_pos_y, self.width, self.bar_height)
        return scroll_bar_rect.collidepoint(mouse_pos)

    def detect_scroll(self,mouse_pos):
        if self.is_dragged(mouse_pos):
            self.barisDragged = True
            self.offset_y = self.bar_pos_y - mouse_pos[1]

    def scrolling(self,mouse_pos):
        self.bar_pos_y = mouse_pos[1] + self.offset_y
        if(self.bar_pos_y <= 50):
            self.bar_pos_y = 50
            return
        if(self.bar_pos_y >= 525):
            self.bar_pos_y = 525
            return
        #testing
        # Update the position of the test rectangle based on the scroll bar position

        global timetable_y_pos
        factor = 5  # Adjust this factor according to how much you want to increase timetable_y_pos
        timetable_y_pos = 50 - (self.bar_pos_y - 50) * factor * (1000 - window_height) / (600 - 50 - self.bar_height)

    def stop_scrolling(self,mouse_pos):
        self.barisDragged = False


rightScrollBar = scrollBar(975,50,25,600)
scrollBars = [rightScrollBar]






# Create a font object
font = pygame.font.Font(None, 24)
datefont = pygame.font.Font(None, 30)

#dateTime
def draw_monthYear():
    # Get the current date
    now = datetime.datetime.now()
    month = now.strftime("%B")
    year = now.strftime("%Y")
    day = now.strftime("%A")
    current_time = now.strftime("%H:%M:%S")

    month_string = now.strftime("%B %Y")
    # Render the text
    text_surface = datefont.render(month_string, True, (0, 0, 0))
    # Blit the text surface onto the screen
    screen.blit(text_surface, (0, 20))  # Adjust the position as needed

def get_monday_date():
    # Get today's date
    today = datetime.datetime.now()
    # Calculate the difference between today's weekday and Monday (0: Monday, 1: Tuesday, ..., 6: Sunday)
    days_to_monday = today.weekday()
    # Subtract the difference to get the date of Monday of the current week
    monday_date = today - timedelta(days=days_to_monday)
    return monday_date

def draw_dayDate(x, y):
    # Get the date of Monday of the current week
    monday_date = get_monday_date()
    # Iterate over each day of the week
    for i in range(7):
        # Get the date for the current day in the loop
        current_date = monday_date + timedelta(days=i)

        # Format the date string
        day_DateString = current_date.strftime("%a %d")
        # Render the text
        text_surface = datefont.render(day_DateString, True, (0, 0, 0))

        # Blit the text surface onto the screen
        # Change colour of today's date to highlight it
        now = datetime.datetime.now()
        if (current_date.day == now.day):
            text_surface = datefont.render(day_DateString, True, (255, 0, 0))  # Change color to red
        screen.blit(text_surface, (x + (120 * i), y))


# UserGUIClasses

class TextBox(object):
    ObjectType = 0
    status = False
    Colours = [pygame.Color('lightskyblue3'), pygame.Color('grey15')]


    def __init__(self, height, width, x, y, header, DefText, TextMode = 0,textMax = 30):
        self.height = height * font_size
        self.width = width * font_size
        self.x = x
        self.y = y
        self.text = ''
        self.textMax = textMax
        self.header = header
        self.box_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.DefText = DefText
        self.TextMode = TextMode

    def checkStatus(self,MousePos):
        # Check Collision
        if self.box_rect.collidepoint(MousePos):
            self.status = True
        else:
            self.status = False

    def updateText(self, Mode, char):
        if Mode == 0:
            self.text = self.text[:-1]
        elif Mode == 1:
            if self.TextMode:
                try:
                    int(char)
                except ValueError:
                    return 1
                except:
                    return 2
            if (len(self.text) >= self.textMax):
                return 0
            self.text += char

    def Draw(self):
        # Drawing Box
        pygame.draw.rect(screen, 'white', self.box_rect)
        pygame.draw.rect(screen, self.Colours[0 if self.status else 1], self.box_rect,2)

        # Drawing Header
        header_surface = test_font.render(self.header, True, 'black')
        screen.blit(header_surface, (self.box_rect.x, self.box_rect.y - 0.8*font_size))

        # Drawing Default Text
        #DefText_surface = test_font.render(self.BoxText, True, 'black')
        #screen.blit(DefText_surface, ((self.box_rect.x + 5, self.box_rect.y + 5)))

        # Drawing Text
        #text_surface = test_font.render(self.text, True, 'black')
        #screen.blit(text_surface, (self.box_rect.x + 5, self.box_rect.y + 5))

        # Merged Commented Code

        # Drawing Text/ Default Text
        if len(self.text) == 0:
            text_surface = test_font.render(self.DefText, True, 'grey')
        else:
            text_surface = test_font.render(self.text, True, 'black')
        screen.blit(text_surface, (self.box_rect.x + 5, self.box_rect.y + 5))

class DropBox(TextBox):
    ObjectType = 1
    Cycle = 0
    ScrollSen = 2
    def __init__(self, height, width, x, y, header,DefText,Content,MaxCycle):
        super().__init__(height, width, x, y, header,DefText)
        self.DDBox_Rect = pygame.Rect(self.x,self.y-self.height, self.width,self.height*3)
        self.Content = Content
        self.MaxCycle = MaxCycle

    def checkStatus(self,MousePos):
        # Check Collision
        if self.box_rect.collidepoint(MousePos):
            if self.status:
                self.status = False
            else:
                self.status = True
        else:
            self.status = False

    def DrawDDBox(self):
        self.Draw()
        if self.status and self.MaxCycle:
            pygame.draw.rect(screen, 'purple', self.DDBox_Rect)
            for i in range(3):
                if i == 1:
                    pygame.draw.rect(screen, 'purple', self.box_rect)
                    pygame.draw.rect(screen, self.Colours[0 if self.status else 1], self.box_rect, 2)
                text_surface = test_font.render(f"{self.Content[(floor(self.Cycle/self.ScrollSen)+(i-1))%self.MaxCycle]:02d}", True, 'black')
                screen.blit(text_surface, (self.DDBox_Rect.x + 5, self.box_rect.y + 5 + (i-1)*self.height))

            #Update the TextBox
            self.text = f"{self.Content[floor(self.Cycle/self.ScrollSen)]:02d}"

        elif self.status and not self.MaxCycle: # ONLY FOR DD MM YYYY
            small_font = pygame.font.Font(None, 16)
            text_surface = small_font.render('Enter Month and Year first!', True, 'red')
            screen.blit(text_surface, (self.DDBox_Rect.x + 5, self.box_rect.y + self.height+5))




    def CheckDayMon(self):
        if self.header == 'Date' or self.header == 'Month':
            if len(self.Content) == 0:
                return 1

        return 0

class TickBox(object):
    ObjectType = 2
    status = False
    Tick_Status = False

    Colours = ['white','red']

    def __init__(self,x,y,header):
        self.x = x
        self.y = y
        self.header = header
        self.box_rect = pygame.Rect(self.x,self.y,30,30)

    def checkStatus(self,MousePos):
        # Check Collision
        if self.box_rect.collidepoint(MousePos):
            self.status = True
            if self.Tick_Status:
                self.Tick_Status = False
            else:
                self.Tick_Status = True
        else:
            self.status = False

    def Draw(self):
        # Drawing Box
        pygame.draw.rect(screen, self.Colours[1 if self.Tick_Status else 0], self.box_rect)
        pygame.draw.rect(screen, 'black', self.box_rect, 2)

        # Drawing Header
        header_surface = test_font.render(self.header, True, 'black')
        screen.blit(header_surface, (self.x + 35, self.y))

class UserInputGUI(object):
    # User GUI Window
    # GUI Size
    BG_Width = 0.8*window_width
    BG_Height = 0.8*window_height

    # (0,0) Position on Background is ( (window_width-BG_Width)/2 , window_height-BG_Height)/2 )
    BG_x = (window_width - BG_Width) / 2
    BG_y = (window_height - BG_Height) / 2

    Background = pygame.Rect(BG_x, BG_y, BG_Width, BG_Height)
    Exit_Rect = pygame.Rect(BG_x + BG_Width - 50, BG_y + 10, font_size, font_size)
    Save_Rect = pygame.Rect(BG_x + font_size, BG_y + font_size, 2 * font_size, font_size)

    DefDict = {}
    RecurDict = {}
    FixDict = {}
    DymDict = {}

    DD_Mins = [00,15,30,45]
    DD_Hours = [x for x in range(24)]
    DD_Year = [x + 2020 for x in range(50)]
    DD_Month = [x + 1 for x in range(12)]
    DD_Days = [x + 1 for x in range(31)]
    DD_MthDay = [31,28,31,30,31,30,31,31,30,31,30,31]

    """ Start of Merging"""
    Mode = 0 # 0 for Fixed 1 for Dynamic

    DefParaStr = ['Event','Location','Description']
    DefParaDB = ['Priority',['Day','Month','Year']]
    DefParaTB = ['Dynamic Event']

    FixParaStr = ['Period','Cycle']
    FixParaDB = [['StartHr','StartMin'],['EndHr','EndMin']]
    FixParaTB = ['Recurrent']

    DymParaDB = [['DurHr','DurMin']]



    """ End of Merging"""


    def __init__(self):
        """ Start of Merging"""
        # Default parameters
        # Strings: name,location,description
        # DropBoxes: priority

        # Fixed parameters
        # Strings: recurring (add textbox if true)
        # DropBoxes: start time,end time,date,
        # TickBoxes: recurring

        # Dynamic parameters
        # Strings
        # DropBoxes: expiry date,duration (datetime.time format)

        # Default Boxes
        # Event Type
        self.DefDict[self.DefParaTB[0]] = TickBox(self.BG_x + 6 * font_size, self.BG_y + font_size, self.DefParaTB[0])

        # Event Name
        self.DefDict[self.DefParaStr[0]] = TextBox(1, 20, self.BG_x + font_size, self.BG_y + 4 * font_size, self.DefParaStr[0],
                                              'Enter the Event')

        # Event Location
        self.DefDict[self.DefParaStr[1]] = TextBox(1, 20, self.BG_x + font_size, self.BG_y + 6 * font_size, self.DefParaStr[1],
                                                'Enter the Location')

        # Event Description
        self.DefDict[self.DefParaStr[2]] = TextBox(3, 20, self.BG_x + font_size, self.BG_y + 8 * font_size, self.DefParaStr[2],
                                                'Enter the Description',textMax=30)

        # Priority Dropbox
        self.DefDict[self.DefParaDB[0]] = DropBox(1, 2, self.BG_x + 22 * font_size, self.BG_y + 4 * font_size, self.DefParaDB[0],
                                               '0', [0,1,2,3], 4)
        # Date
        self.DefDict[self.DefParaDB[1][0]] = DropBox(1, 2, self.BG_x + 4.5 * font_size, self.BG_y + 12 * font_size,
                                                     self.DefParaDB[1][0],
                                                  'DD', self.DD_Days, 0)
        self.DefDict[self.DefParaDB[1][1]] = DropBox(1, 2, self.BG_x + 7 * font_size, self.BG_y + 12 * font_size,
                                                     self.DefParaDB[1][1],
                                                  'MM', self.DD_Month, 12)
        self.DefDict[self.DefParaDB[1][2]] = DropBox(1, 2, self.BG_x + 9.5 * font_size, self.BG_y + 12 * font_size,
                                                     self.DefParaDB[1][2],
                                                  'YYYY', self.DD_Year, 50)



        # Fixed Boxes
        # Recurrent Start
        self.RecurDict[self.FixParaStr[0]] = TextBox(1, 2, self.BG_x + 29 * font_size, self.BG_y + 6 * font_size, self.FixParaStr[0],
                                                '00',1,2)
        self.RecurDict[self.FixParaStr[1]] = TextBox(1, 2, self.BG_x + 26 * font_size, self.BG_y + 6 * font_size, self.FixParaStr[1],
                                                '00',1,2)
        self.FixDict[self.FixParaTB[0]] = TickBox(self.BG_x + 14 * font_size, self.BG_y + font_size, self.FixParaTB[0])
        # Recurrent End

        # Time
        # Start Time
        self.FixDict[self.FixParaDB[0][0]] = DropBox(1, 2, self.BG_x + 4.5 * font_size, self.BG_y + 16 * font_size, 'Hour',
                                                  'Hrs', self.DD_Hours, 24)
        self.FixDict[self.FixParaDB[0][1]] = DropBox(1, 2, self.BG_x + 7 * font_size, self.BG_y + 16 * font_size, 'Min',
                                                  'Mins', self.DD_Mins, 4)
        # End Time
        self.FixDict[self.FixParaDB[1][0]] = DropBox(1, 2, self.BG_x + 15 * font_size, self.BG_y + 16 * font_size, 'Hour',
                                                  'Hrs', self.DD_Hours, 24)
        self.FixDict[self.FixParaDB[1][1]] = DropBox(1, 2, self.BG_x + 17.5 * font_size, self.BG_y + 16 * font_size, 'Min',
                                                  'Mins', self.DD_Mins, 4)

        # Dynamic Boxes
        self.DymDict[self.DymParaDB[0][0]] = DropBox(1, 2, self.BG_x + 4.5 * font_size, self.BG_y + 16 * font_size, 'Hour',
                                                  'Hrs', self.DD_Hours, 24)
        self.DymDict[self.DymParaDB[0][1]] = DropBox(1, 2, self.BG_x + 7 * font_size, self.BG_y + 16 * font_size, 'Min',
                                                  'Mins', self.DD_Mins, 4)

        """ End of Merging"""

    def Draw(self):
        Colours = [pygame.Color('lightskyblue3'), pygame.Color('grey15')]

        # Background
        pygame.draw.rect(screen, 'blue', self.Background)

        # Exit Button
        pygame.draw.rect(screen, 'red', self.Exit_Rect)
        Exit_font = pygame.font.Font(None, self.Exit_Rect.width)
        Exit_surface = Exit_font.render('x', True, 'white')
        screen.blit(Exit_surface, (self.Exit_Rect.x + 0.25 * font_size, self.Exit_Rect.y))

        # Save Button
        pygame.draw.rect(screen, 'red', self.Save_Rect)
        Save_Surface = test_font.render('Save', True, 'white')
        screen.blit(Save_Surface, (self.Save_Rect.x, self.Save_Rect.y))

        # Priority Text
        Priority = ['Low', 'Medium', 'High', 'Urgent']
        Priority_Class = self.DefDict['Priority']

        for i in range(4):
            Priority_Surface = Small_font.render(f'{i} - {Priority[i]}', True, 'White')
            screen.blit(Priority_Surface,
                        (Priority_Class.x + 3 * font_size, Priority_Class.y - font_size + i * 0.5 * font_size))

        # Date Text
        Date_Class = self.DefDict['Day']
        DateTitle_Surface = test_font.render('Date:', True, 'white')
        screen.blit(DateTitle_Surface, (Date_Class.x - 3 * font_size, Date_Class.y))

        # Default Drawing
        for item in self.DefDict.values():
            if item.ObjectType == 1:
                item.DrawDDBox()
            else:
                item.Draw()

        # Dynamic Drawing
        if self.Mode:
            Time_Class = self.DymDict['DurHr']
            TimeTitle_Surface = test_font.render('Duration:', True, 'white')
            screen.blit(TimeTitle_Surface, (Time_Class.x - 3 * font_size, Time_Class.y))

            for item in self.DymDict.values():
                if item.ObjectType == 1:
                    item.DrawDDBox()
                else:
                    item.Draw()

        else:
            Time_Class = self.FixDict['StartHr']
            TimeTitle_Surface = test_font.render('Start:', True, 'white')
            screen.blit(TimeTitle_Surface, (Time_Class.x - 3 * font_size, Time_Class.y))

            Time_Class = self.FixDict['EndHr']
            TimeTitle_Surface = test_font.render('End:', True, 'white')
            screen.blit(TimeTitle_Surface, (Time_Class.x - 3 * font_size, Time_Class.y))

            if self.FixDict['Recurrent'].Tick_Status:
                Recurrent_Class = self.RecurDict['Cycle']
                RecurTitle_Surface = test_font.render('Recurrent:', True, 'white')
                screen.blit(RecurTitle_Surface, (Recurrent_Class.x - 4 * font_size, Recurrent_Class.y))
                RecurText_Surface = Small_font.render(f'Cycle: 0 - Forver '
                                                      f'          N - N Times', True, 'White')
                screen.blit(RecurText_Surface,
                            (Recurrent_Class.x - 4 * font_size, Recurrent_Class.y + 1.1 * font_size))
                RecurText_Surface = Small_font.render(f'Perid: 1 - Every Day'
                                                      f'       7 - Every Week', True, 'White')
                screen.blit(RecurText_Surface,
                            (Recurrent_Class.x - 4 * font_size, Recurrent_Class.y + 1.6 * font_size))

                for item in self.RecurDict.values():
                    if item.ObjectType == 1:
                        item.DrawDDBox()
                    else:
                        item.Draw()

            for item in self.FixDict.values():
                if item.ObjectType == 1:
                    item.DrawDDBox()
                else:
                    item.Draw()

    def UserClick(self, MousePos):
        if self.Exit_Rect.collidepoint(MousePos):
            return 1

        if self.Save_Rect.collidepoint(MousePos):
            if self.CheckFilled():
                return 0
            else:
                self.DeactiveAll()
                return 2

        for item in self.DefDict.values():
            item.checkStatus(MousePos)

        TempDict = self.DymDict if self.Mode else self.FixDict
        for item in TempDict.values():
            item.checkStatus(MousePos)
        if not self.Mode and self.FixDict['Recurrent'].Tick_Status:
            for item in self.RecurDict.values():
                item.checkStatus(MousePos)

        return 0

    def EditText(self, Mode, Char):
        for item in self.DefDict.values():
            if item.status and item.ObjectType == 0:
                item.updateText(Mode, Char)

        TempDict = self.DymDict if self.Mode else self.FixDict
        for item in TempDict.values():
            if item.status and item.ObjectType == 0:
                item.updateText(Mode, Char)
        if not self.Mode and self.FixDict['Recurrent'].Tick_Status:
            for item in self.RecurDict.values():
                if item.status and item.ObjectType == 0:
                    item.updateText(Mode, Char)

    def ScrollDD(self, UpDown, MousePos):
        for item in self.DefDict.values():
            self.ScrollFunc(item, UpDown)

        TempDict = self.DymDict if self.Mode else self.FixDict
        for item in TempDict.values():
            self.ScrollFunc(item, UpDown)
        if not self.Mode and self.FixDict['Recurrent'].Tick_Status:
            for item in self.RecurDict.values():
                self.ScrollFunc(item, UpDown)

        self.UpdateDay()

    def ScrollFunc(self, item, UpDown):
        if item.status and item.ObjectType == 1:
            if item.CheckDayMon():
                return
            if UpDown == 4:  # Scroll Up
                item.Cycle -= 1
            else:  # Scroll Down
                item.Cycle += 1
            if item.Cycle == item.ScrollSen * item.MaxCycle:  # Cycle from last to first
                item.Cycle = 0
            if item.Cycle == -1:  # Cycle from first to last
                item.Cycle = item.ScrollSen * item.MaxCycle - 1

    def UpdateDay(self):
        Year = self.DefDict.get('Year')
        Month = self.DefDict.get('Month')
        Day = self.DefDict.get('Day')
        if not Year or not Month:
            return
        if Year.status or Month.status:
            if Year.text != '' and Month.text != '':
                if (int(Year.text) - 2024) % 4 == 0:
                    Leap = 1
                else:
                    Leap = 0
                MthDay = int(Month.text) - 1
                MaxDays = self.DD_MthDay[MthDay] if MthDay != 1 else (self.DD_MthDay[MthDay] + Leap)
                #print(MaxDays)
                Day.MaxCycle = MaxDays
                Day.Cycle = 0
                Day.text = '01'
            else:
                Day.MaxCycle = 0
                Day.Cycle = 0

    def UpdateEventType(self):
        if self.DefDict['Dynamic Event'].Tick_Status:
            self.Mode = 1
        else:
            self.Mode = 0
        return

    def Update(self):
        self.UpdateEventType()
        self.UpdateDay()

    def DeactiveAll(self):
        for item in self.DefDict.values():
            item.status = False

    def CheckFilled(self):
        for item in self.DefDict.values():
            if item.ObjectType != 2 and item.text == '':
                return 1

        TempDict = self.DymDict if self.Mode else self.FixDict
        for item in TempDict.values():
            if item.ObjectType != 2 and item.text == '':
                return 1


        if not self.Mode and self.FixDict['Recurrent'].Tick_Status:
            for item in self.RecurDict.values():
                if item.ObjectType != 2 and item.text == '':
                    return 1
        return 0

    def CreateEvent(self):
        if self.CheckFilled():
            print("Please Fill Boxes")
            return
        EventName = self.DefDict['Event'].text
        EventLoc = self.DefDict['Location'].text
        EventDes = self.DefDict['Description'].text
        _Priority = Priority(int(self.DefDict['Priority'].text))
        Date = datetime.date(int(self.DefDict['Year'].text),int(self.DefDict['Month'].text),int(self.DefDict['Day'].text))

        if self.Mode:
            EventDur = datetime.time(int(self.DymDict['DurHr'].text),int(self.DymDict['DurMin'].text))

            Event = DynamicEvent(name=EventName,
                                 duration=EventDur,
                                 expiry_date=Date,
                                 location=EventLoc,
                                 description=EventDes,
                                 priority_tag=_Priority)

        else:
            if self.FixDict['Recurrent'].Tick_Status:
                Period = int(self.RecurDict['Period'].text)
                Cycle = int(self.RecurDict['Cycle'].text)
            else:
                Period = 0
                Cycle = 0
            StartTime = datetime.time(int(self.FixDict['StartHr'].text),int(self.FixDict['StartMin'].text))
            EndTime = datetime.time(int(self.FixDict['EndHr'].text), int(self.FixDict['EndMin'].text))


            Event = FixedEvent(name=EventName,
                               start_time=StartTime,
                               end_time=EndTime,
                               date=Date,
                               recur_period=Period,
                               recur_cycle=Cycle,
                               location=EventLoc,
                               description=EventDes,
                               priority_tag=_Priority)
        return Event

    def Clear_Input(self):
        output = self.Mode
        self.FixDict.clear()
        self.DefDict.clear()
        self.DymDict.clear()
        self.__init__()
        return output


# Initialize Timetable
TTableObject = TTable(150,50)
TTableObject.load_data_CSV()
print(len(TTableObject.dynamic_events),len(TTableObject.fixed_events))
# Loading Data from storage



# Initialize Variables
sideBar = pygame.Rect(0,0,150,600)
dayBar = pygame.Rect(150,0,850,50)

# To add buttons just add here and chagne the array
# Buttons
inputButton = SideButton(0, 50, 100, 40, "INPUT")
sortButton = SideButton(0, 90, 100, 40, "SORT")
deleteButton = SideButton(0,130,100,40,"DELETE")
editButton = SideButton(0,170,100,40,"EDIT")

#upButton = SideButton(0,555,100,20,"UP")
#downButton = SideButton(0,575,100,20,"DOWN")

PlannerButtons = [sortButton, inputButton,deleteButton,editButton]


# Initialise UserInputGUI
UserGUIObject = UserInputGUI()



# Initialise Dummy Events
for i in range(0,11,2):
    a = i+1
    Event = FixedEvent(name='Fix'+str(i),
                       start_time=datetime.time(i,0,0),
                       end_time=datetime.time(i,30,0),
                       date=datetime.datetime.now(),
                       recur_period=0,
                       recur_cycle=0,
                       location='Fix'+str(i),
                       description='Fix'+str(i),
                       priority_tag=Priority(i%4))
    TTableObject.add_fixed_event(Event)

    Event = FixedEvent(name='Fix' + str(i),
                       start_time=datetime.time(i, 0, 0),
                       end_time=datetime.time(i, 30, 0),
                       date=datetime.date(2024,3,20),
                       recur_period=0,
                       recur_cycle=0,
                       location='Fix' + str(i),
                       description='Fix' + str(i),
                       priority_tag=Priority(i % 4))
    TTableObject.add_fixed_event(Event)

    Event = DynamicEvent(name='Dym'+str(a),
                         duration=datetime.time(0,30,0),
                         expiry_date=datetime.datetime.now(),
                         location='Fix'+str(i),
                         description='Dym'+str(a),
                         priority_tag=Priority(a%4))
    Event._start_time = datetime.time(a,0,0)
    Event._date = datetime.datetime.now()
    TTableObject.add_dynamic_event(Event)

    Event = DynamicEvent(name='Dym' + str(a),
                         duration=datetime.time(0, 30, 0),
                         expiry_date=datetime.date(2024,3,20),
                         location='Fix' + str(i),
                         description='Dym' + str(a),
                         priority_tag=Priority(a % 4))
    Event._start_time = datetime.time(a, 0, 0)
    Event._date = datetime.date(2024,3,20)
    TTableObject.add_dynamic_event(Event)
'''

#TTableObject.remove_fixed_event(4)

for item in TTableObject.dynamic_events:
        item.print_event()
        #print(item._unique_id)
for item in TTableObject.fixed_events:
        item.print_event()
        #print(item._unique_id)
TTableObject.sort_fixed_events()
TTableObject.sort_dynamic_events()
print('\n')
for item in TTableObject.dynamic_events:
        item.print_event()
        #print(item._unique_id)
for item in TTableObject.fixed_events:
        item.print_event()
        #print(item._unique_id)

'''

# Input handling
def handle_input():
    global running, window_height, window_width, screen,PlannerButtons, UserEventGUI
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            TTableObject.save_data_CSV()
            running = False

        # Seperated Main input with GUI Input
        if not UserEventGUI:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    for _button in PlannerButtons:
                        if _button.is_clicked(mouse_pos):
                            if _button.text == "INPUT":
                                UserEventGUI = True
                            _button.isClicked = True
                    for _scrollbar in scrollBars:
                        _scrollbar.detect_scroll(mouse_pos)

                elif event.button == 4:  # Scroll up
                    # Move the timetable and scroll bar up by a certain amount
                    if rightScrollBar.bar_pos_y <= 50:
                        rightScrollBar.bar_pos_y = 50
                        return
                    elif rightScrollBar.bar_pos_y >= 525:
                        rightScrollBar.bar_pos_y = 525
                        return
                    if (rightScrollBar.bar_pos_y >= 40 and rightScrollBar.bar_pos_y <= 525):
                        timetable_y_pos += SCROLL_SPEED
                        rightScrollBar.bar_pos_y -= SCROLL_SPEED / 3

                elif event.button == 5:  # Scroll down

                    if rightScrollBar.bar_pos_y >= 525:
                        rightScrollBar.bar_pos_y = 523
                        return
                    if (rightScrollBar.bar_pos_y >= 50 and rightScrollBar.bar_pos_y <= 525):
                        # Move the timetable and scroll bar down by a certain amount
                        timetable_y_pos -= SCROLL_SPEED
                        rightScrollBar.bar_pos_y += SCROLL_SPEED / 3


            elif event.type == pygame.MOUSEBUTTONUP:
                #stop scrolling
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    for _scrollbar in scrollBars:
                        _scrollbar.stop_scrolling(mouse_pos)

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                # Check if mouse is hovering over any button
                for _button in PlannerButtons:
                    _button.isHovered = _button.is_hovered_over(pygame.mouse.get_pos())
                # Check if mouse is hovering over scroll bar
                for _scrollbar in scrollBars:
                    _scrollbar.isHovered = _scrollbar.is_hovered_over(pygame.mouse.get_pos())
                    if _scrollbar.barisDragged:
                        _scrollbar.scrolling(mouse_pos)


        if  UserEventGUI:
            UserGUIObject.Update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    UserGUIObject.DeactiveAll()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Value = UserGUIObject.UserClick(event.pos)
                    if Value == 1:
                        UserEventGUI = False
                    elif Value == 2:
                        Event = UserGUIObject.CreateEvent()
                        Event.print_event()
                        print(len(TTableObject.dynamic_events),len(TTableObject.fixed_events))
                        # Output 0/1 for Fix/Dym for adding
                        if UserGUIObject.Clear_Input():
                            TTableObject.add_dynamic_event(Event)
                        else:
                            TTableObject.add_fixed_event(Event)

                        print(len(TTableObject.dynamic_events), len(TTableObject.fixed_events))
                        UserEventGUI = False

                if event.button in [4, 5]:
                    #print(event.button)
                    UserGUIObject.ScrollDD(event.button, event.pos)

        if event.type == pygame.KEYDOWN:
            if UserEventGUI:
                if event.key == pygame.K_BACKSPACE:
                    UserGUIObject.EditText(0, event.unicode)
                else:
                    UserGUIObject.EditText(1, event.unicode)



def update():
    global PlannerButtons

    pygame.display.update()
    for button in PlannerButtons:
        if(inputButton.isClicked):
            print("CLICK INPUT")
            inputButton.isClicked = False;
        if (sortButton.isClicked):
            print("CLICK SORT")
            sortButton.isClicked = False;
        if (deleteButton.isClicked):
            print("CLICK DELETE")
            deleteButton.isClicked = False;
        if (editButton.isClicked):
            print("CLICK EDIT")
            editButton.isClicked = False;


testEvent(FixEvents, DymEvents)

combinedArray = []
a = 0
b = 0
while (a < len(FixEvents) and b < len(DymEvents)):
    # print("Dym: ")
    # print(DymEvents[b]._date)
    # print("Fix: ")
    # print(FixEvents[a]._date)
    if (FixEvents[a]._date < DymEvents[b]._date):

        combinedArray.append((FixEvents[a]))
        a += 1

    elif FixEvents[a]._date > DymEvents[b]._date:
        combinedArray.append((DymEvents[b]))
        b += 1
    else:
        if FixEvents[a]._start_time < DymEvents[b]._start_time:
            combinedArray.append(FixEvents[a])
            a += 1
        else:
            combinedArray.append((DymEvents[b]))
            b += 1

if (a == len(FixEvents)):
    while (b < len(DymEvents)):
        combinedArray.append((DymEvents[b]))
        b += 1
else:
    while (a < len(FixEvents)):
        combinedArray.append((FixEvents[a]))
        a += 1

print("b4")
print((combinedArray[1]._date.day) == (combinedArray[0]._date.day))
# for i in combinedArray:
#     print(i._date)
print("after")


def draw():
    global PlannerButtons, screen
    # Clear the screen
    screen.fill(white_background)

    mouse_position = pygame.mouse.get_pos()
    current_day = combinedArray[0]._date.day
    k = 0
    j = 0
    for i in range(len(combinedArray)):
        if current_day != combinedArray[i]._date.day:
            k += 1
            j = 0
            current_day = combinedArray[i]._date.day
        hello = timetableBox((100 * k) + 150, (100 * j) + timetable_y_pos, 100, 100, combinedArray[i], screen)
        mouse_pos = pygame.mouse.get_pos()
        hello.isHovered = hello.is_hovered_over(mouse_pos)
        hello.draw(mouse_position)
        j += 1
        # print(j)


    #draw Bars
    pygame.draw.rect(screen,(112,128,144),sideBar)
    pygame.draw.rect(screen,Slate_Gray,dayBar)

    draw_monthYear()
    draw_dayDate(150,30)

    #draw buttons
    for _button in PlannerButtons:
        _button.draw(screen)

    #draw scroll bar
    for _scrollbar in scrollBars:
        _scrollbar.draw(screen)

    if UserEventGUI:
        UserGUIObject.Draw()

# Program Loop
running = True
while running:
    handle_input()
    draw()

    update()

# Quit
pygame.quit()