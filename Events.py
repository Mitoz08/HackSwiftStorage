import datetime
from enum import Enum


class Priority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    URGENT = 3


class Event:
    # Assumption that events are only for a single day
    def __init__(self,name: str,
                 start_time: datetime.time,
                 end_time: datetime.time,
                 date: datetime.date,
                 location: str,
                 description: str,
                 priority_tag: Priority = Priority.LOW):
        self._name = name
        self._start_time = start_time
        self._end_time = end_time
        self._date = date
        self._location = location
        self._description = description
        self._priority_tag = priority_tag
        self._unique_id = 0

    # Getters / Setters
    def get_name(self):
        return self._name

    def get_start_time(self):
        return self._start_time

    def get_date(self):
        return self._date

    def get_location(self):
        return self._location

    def get_description(self):
        return self._description

    def get_priority(self):
        return self._priority_tag

    def get_end_time(self):
        return self._end_time

    def set_name(self, name: str):
        self._name = name

    def set_start_time(self, start_time):
        self._start_time = start_time

    def set_date(self, date):
        self._date = date

    def set_location(self, location: str):
        self._location = location

    def set_description(self, description: str):
        self._description = description

    def set_priority(self, priority_tag: Priority):
        self._priority_tag = priority_tag

    def set_end_time(self, end_time):
        self._end_time = end_time

    # For Checking Events
    def print_event(self):
        print(self.get_name(),self._date,self._start_time,self.get_priority())

    # To be called by Dynamic Events to find End Time
    def find_end_time(self,duration):
        hours = duration.hour
        mins = duration.minute
        _StartTime = datetime.datetime.combine(self._date, self._start_time)
        _TimeDelta = datetime.timedelta(hours=hours,minutes=mins)
        return (_StartTime + _TimeDelta).time()

    # To be called by Fixed Events to find Duration
    def find_duration(self):
        _StartTime = datetime.datetime.combine(self._date, self._start_time)
        _EndTime = datetime.datetime.combine(self._date, self._end_time)
        return (_EndTime-_StartTime)

# This actually violates Liskov Substitution Principle, but we're not gonna store events anyways, we're storing FixedEvents and DynamicEvents seperately
# recurring_period is a number of days between each event instance
# For example, if recurring_period is 7, the event will occur every week
# If recurring_period is 0 or below, the event will not recur
class FixedEvent(Event):
    def __init__(self,name: str,
                 start_time: datetime.time,
                 end_time: datetime.time,
                 date: datetime.date,
                 recur_period: int,
                 recur_cycle: int,
                 location: str,
                 description: str,
                 priority_tag: Priority = Priority.LOW):
        super().__init__(name=name,start_time=start_time,date=date,location=location,description=description,
                         priority_tag=priority_tag,end_time= end_time)
        self._recur_period = recur_period
        self._recur_cycle = recur_cycle
        self.priority_tag = priority_tag

    def is_recurring(self):
        return self._recur_period > 0

    def get_next_date(self):
        return self._date + datetime.timedelta(days=self._recur_period)

    def get_duration(self):
        return self.find_duration()

    # Getters / Setters
    def get_recur_period(self):
        return self._recur_period

    def get_recur_cycle(self):
        return self._recur_cycle

    def set_recur_period(self, recurring_period):
        self._recur_period = recurring_period

    def set_recur_cycle(self, recurring_cycle):
        self._recur_cycle = recurring_cycle




# Events that don't occur on a particular date / time, but have a duration
# It's start_date and start_time are only set when the event is scheduled using the TimeTable class
class DynamicEvent(Event):
    def __init__(self,name: str,
                 duration: datetime.time,
                 expiry_date: datetime.date,
                 location: str,
                 description: str,
                 priority_tag: Priority = Priority.LOW):
        super().__init__(name=name, start_time=None, date=None, location=location, description=description,
                         priority_tag=priority_tag,end_time=None)
        self._duration = duration
        self._expiry_date = expiry_date
        self.priority_tag = priority_tag

    # Getters / Setters
    def get_duration(self):
        return self._duration

    def get_expiry_date(self):
        return self._expiry_date

    def set_duration(self, duration):
        self._duration = duration

    def set_expiry_date(self, expiry_date):
        self._expiry_date = expiry_date
