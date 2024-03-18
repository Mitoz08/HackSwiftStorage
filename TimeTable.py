import Events
from Events import Priority, FixedEvent, DynamicEvent, Event
import datetime
import pygame
from enum import Enum
from datetime import date, time, timedelta

import csv


# TODO: Complete TimeTable class
# TODO: Add function to get empty time ranges in the timetable

# Each TimeTable object is a collection of FixedEvent and DynamicEvent objects seperately.
# Balanced Load:
# Load Factor = 5 * Min( [Free Time - Work : weekdays] ) + 2 * WeekEndScaleFactor * Min( [Free Time - Work : weekends] )

class TimeTable:
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
        self.id_counter = 0
        self.width = 0
        self.height = 0
        self.events = 0
        self.fixed_events = []
        self.dynamic_events = []

    @staticmethod
    def data_get_priority(Item):
        if Item == 'Priority.LOW':
            return Priority(0)
        elif Item == 'Priority.MEDIUM':
            return Priority(1)
        elif Item == 'Priority.HIGH':
            return Priority(2)
        else:
            return Priority(3)

    def load_data_CSV(self):
        try:
            with open('FixedEvent.csv', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)
                for line in csv_reader:
                    Event = FixedEvent(name=line[0],
                                       start_time=datetime.time(int(line[1]), int(line[2]), 0),
                                       end_time=datetime.time(int(line[3]), int(line[4]), 0),
                                       date=datetime.date(int(line[5]), int(line[6]), int(line[7])),
                                       location=line[8],
                                       description=line[9],
                                       priority_tag=self.data_get_priority(line[10]),
                                       recur_period=int(line[11]),
                                       recur_cycle=int(line[12]))
                    self.add_fixed_event(Event)
            csv_file.close()
        except FileNotFoundError:
            with open('FixedEvent.csv', 'w', newline='') as new_file:
                csv_writer = csv.writer(new_file)

                line = ['Name', 'StartHour', 'StartMinute', 'EndHour', 'EndMinute', 'DateYear', 'DateMonth', 'DateDay',
                        'Location', 'Description', 'Priority_Tag',
                        'Recur_Period', 'Recur_Cycle']
                csv_writer.writerow(line)
                new_file.close()
                return

        try:
            with open('DynamicEvent.csv', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)
                for line in csv_reader:
                    Event = DynamicEvent(name=line[0],
                                         location=line[8],
                                         duration=datetime.time(int(line[11]), int(line[12])),
                                         expiry_date=datetime.date(int(line[13]), int(line[14]), int(line[15])),
                                         description=line[9],
                                         priority_tag=self.data_get_priority(line[10]))

                    Event.set_start_time(datetime.time(int(line[1]), int(line[2]), 0))
                    Event.set_end_time(datetime.time(int(line[3]), int(line[4]), 0))
                    Event.set_date(datetime.date(int(line[5]), int(line[6]), int(line[7])))
                    self.add_dynamic_event(Event)
            csv_file.close()
        except FileNotFoundError:
            with open('DynamicEvent.csv', 'w', newline='') as new_file:
                csv_writer = csv.writer(new_file)

                line = ['Name', 'StartHour', 'StartMinute', 'EndHour', 'EndMinute', 'DateYear', 'DateMonth', 'DateDay',
                        'Location', 'Description', 'Priority_Tag',
                        'DurationHour', 'DurationMinute', 'ExpiryDateYear', 'ExpiryDateMonth', 'ExpiryDateDay']
                csv_writer.writerow(line)
                new_file.close()
                csv_file.close()
                return

    def save_data_CSV(self):
        with open('FixedEvent.csv', 'w', newline='') as new_file:
            csv_writer = csv.writer(new_file)

            line = ['Name', 'StartHour', 'StartMinute', 'EndHour', 'EndMinute', 'DateYear', 'DateMonth', 'DateDay',
                    'Location', 'Description',
                    'Priority_Tag', 'Recur_Period', 'Recur_Cycle']
            csv_writer.writerow(line)

            for item in self.fixed_events:
                line = [item.get_name(),
                        str(item.get_start_time().hour), str(item.get_start_time().minute),
                        str(item.get_end_time().hour), str(item.get_end_time().minute),
                        str(item.get_date().year), str(item.get_date().month), str(item.get_date().day),
                        item.get_location(), item.get_description(),
                        item.get_priority(), str(item.get_recur_period()), str(item.get_recur_cycle())]
                csv_writer.writerow(line)
            new_file.close()

        with open('DynamicEvent.csv', 'w', newline='') as new_file:
            csv_writer = csv.writer(new_file)

            line = ['Name', 'StartHour', 'StartMinute', 'EndHour', 'EndMinute', 'DateYear', 'DateMonth', 'DateDay',
                    'Location', 'Description',
                    'Priority_Tag', 'DurationHour', 'DurationMinute', 'ExpiryDateYear', 'ExpiryDateMonth',
                    'ExpiryDateDay']
            csv_writer.writerow(line)

            for item in self.dynamic_events:
                # time = (datetime.datetime.combine(datetime.date(2024,1,1),
                # datetime.time(0,0,0))+item.get_duration()).time()
                if item.get_end_time() == None:
                    time = datetime.time(0, 0, 0)
                else:
                    time = item.get_end_time()

                if item.get_start_time() == None:
                    time1 = datetime.time(0, 0, 0)
                else:
                    time1 = item.get_start_time()

                if item.get_date() == None:
                    date = datetime.date(2024, 1, 1)
                else:
                    date = item.get_date()

                line = [item.get_name(),
                        str(time1.hour), str(time1.minute),
                        str(time.hour), str(time.minute),
                        str(date.year), str(date.month), str(date.day),
                        item.get_location(), item.get_description(),
                        item.get_priority(), str(item.get_duration().hour), str(item.get_duration().minute),
                        str(item.get_expiry_date().year), str(item.get_expiry_date().month),
                        str(item.get_expiry_date().day)]
                csv_writer.writerow(line)
            new_file.close()

    def sort_fixed_events(self):
        TNow = datetime.datetime.now()
        TempList = []
        OutputList = []
        for item in self.fixed_events:
            TDiff = datetime.datetime.combine(item.get_date(), item.get_start_time()) - TNow
            TimeTillEvent = TDiff.days * (24 * 60 * 60) + TDiff.seconds
            TempList.append((TimeTillEvent, item))
        TempList.sort()
        for item in TempList:
            OutputList.append(item[1])
        self.fixed_events = OutputList

    def sort_dynamic_events(self):
        TNow = datetime.datetime.now()
        TempList = []
        OutputList = []
        for item in self.dynamic_events:
            TDiff = datetime.datetime.combine(item.get_date(), item.get_start_time()) - TNow
            TimeTillEvent = TDiff.days * (24 * 60 * 60) + TDiff.seconds
            TempList.append((TimeTillEvent, item))
        TempList.sort()
        for item in TempList:
            OutputList.append(item[1])
        self.dynamic_events = OutputList

    def add_fixed_event(self, event: FixedEvent):
        event._unique_id = self.id_counter
        self.fixed_events.append(event)
        self.id_counter += 1
        pass

    def add_dynamic_event(self, event: DynamicEvent):
        event._unique_id = self.id_counter
        self.dynamic_events.append(event)
        self.id_counter += 1
        pass

    def remove_fixed_event(self, id: int):
        if len(self.fixed_events) == 0:
            return 0
        for event in self.fixed_events:
            if event._unique_id == id:
                self.fixed_events.remove(event)
                return 1
        # Check equality id

    def remove_dynamic_event(self, id: int):
        if len(self.dynamic_events) == 0:
            return 0
        for event in self.dynamic_events:
            if event._unique_id == id:
                self.dynamic_events.remove(event)
                return 1
        # Check equality id

    def get_fixed_events_by_week(self, week: datetime.date):
        output = []
        today = datetime.datetime.now()
        days_to_monday = today.weekday()
        monday_date = today - datetime.timedelta(days=days_to_monday)
        self.sort_fixed_events()

        end_date = monday_date + datetime.timedelta(days=7)
        for item in self.fixed_events:
            if item.get_date() < end_date:
                output.append(item)
            else:
                break
        return output

    def get_dynamic_events_by_week(self, week: datetime.date):
        output = []
        today = datetime.datetime.now()
        days_to_monday = today.weekday()
        monday_date = today - datetime.timedelta(days=days_to_monday)
        self.sort_dynamic_events()

        end_date = monday_date + datetime.timedelta(days=7)
        for item in self.fixed_events:
            date = datetime.date(item.get_date().year, item.get_date().month, item.get_date().day)
            if item.get_date() < end_date:
                output.append(item)
            else:
                break
        return output

    def get_empty_time_ranges(self):
        pass

    def shedule_dynamic_events(self):
        pass


class Priority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    URGENT = 3


def testEvent(FixArray, DymArray):
    for i in range(0, 11, 2):
        a = i + 1
        Event = FixedEvent(name='Fix' + str(i),
                           start_time=datetime.time(i, 0, 0),
                           end_time=datetime.time(i, 30, 0),
                           date=datetime.datetime.now(),
                           recur_period=0,
                           recur_cycle=0,
                           location='Fix' + str(i),
                           description='Fix' + str(i),
                           priority_tag=Priority(i % 4))
        FixArray.append(Event)

        Event1 = DynamicEvent(name='Dym' + str(a),
                              duration=datetime.time(0, 30, 0),
                              expiry_date=datetime.datetime.now(),
                              location='Dym' + str(i),
                              description='Dym' + str(a),
                              priority_tag=Priority(a % 4))
        Event1._start_time = datetime.time(a, 0, 0)
        Event1._date = datetime.datetime.now()
        DymArray.append(Event1)

    for item in FixArray:
        item.print_event()

    for item in DymArray:
        item.print_event()
        print(type(item))
    print(type(DymArray[0]))


class timetableBox():

    def __init__(self, x, y, height, width, Event, screen):
        box_image = pygame.Surface((height, width))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = box_image
        self.rect = pygame.Rect(x, y, width, height)

        self.nameText = Event.get_name()
        self.start_timeText = Event.get_start_time()
        self.priority = Event.get_priority()
        self.dateText = Event.get_date()
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.locationText = Event.get_location()
        self.descriptionText = Event.get_description()
        self.isHovered = False
        # self.end_timeText =
        # self.durationText =
        # self.expiry_dateText =

    def draw(self, mouse_position):
        Yellow = (255, 255, 0)
        Green = (0, 255, 0)
        Red = (255, 0, 0)
        DarkGreen = (0, 128, 0)
        colour = Green
        # classify priority

        if self.priority == Priority(0):
            colour = DarkGreen
        elif self.priority == Priority(1):
            colour = Green
        elif self.priority == Priority(2):
            colour = Yellow
        elif self.priority == Priority(3):
            colour = Red

        pygame.draw.rect(self.screen, colour, self.rect)

        if self.isHovered:
            # Adjust font size to fit text within box
            font_size = 15
            font = pygame.font.Font(None, font_size)

            # Split description into multiple lines
            description_lines = self.split_text_into_lines(str(self.descriptionText), font, self.width)

            # Render each line of description text
            y_offset = -10
            for line in description_lines:
                description_text_surface = font.render(line, True, (0, 0, 0))
                text_rect = description_text_surface.get_rect(midtop=(self.rect.centerx, self.rect.centery + y_offset))
                self.screen.blit(description_text_surface, text_rect)
                y_offset += font.get_height()  # Increment y offset for next line

        else:
            text_surface = self.font.render(self.nameText, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery - 12))
            self.screen.blit(text_surface, text_rect)

            text_surface = self.font.render(str(self.start_timeText), True, (0, 0, 0))
            text_rect = text_surface.get_rect(midtop=(self.rect.centerx, self.rect.centery - 0))
            self.screen.blit(text_surface, text_rect)

            text_surface = self.font.render(str(self.locationText), True, (0, 0, 0))
            text_rect = text_surface.get_rect(midtop=(self.rect.centerx, self.rect.centery + 20))
            self.screen.blit(text_surface, text_rect)

    def split_text_into_lines(self, text, font, max_width):
        lines = []
        words = text.split()
        current_line = ""
        for word in words:
            if font.size(current_line + word)[0] <= max_width:
                current_line += (word + " ")
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)  # Add the last line
        return lines

    def is_hovered_over(self, mouse_pos):
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return button_rect.collidepoint(mouse_pos)
