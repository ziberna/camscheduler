#    camscheduler (scheduler for capturing images from camera)
#    Copyright (C) 2011 Kantist
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.
#    If not, see http://www.gnu.org/licenses/gpl-3.0.html

import ephem
import datetime
 
class Sky(object):
    def __init__(self, lat, long, localtime=True):
        self.observer = ephem.Observer()
        self.observer.lat = lat
        self.observer.long = long
        self.sun = ephem.Sun()
        
        self.localtime = localtime
        self.night = self.getnight()
        self.day = self.getday()
    
    def setdate(self, date=None):
        if not date: date = datetime.datetime.now()
        self.date = date
        self.observer.date = date
    
    def sunrise(self, date=None):
        if date:
            previous = self.date
            self.setdate(date)
        
        sunrise = self.observer.next_rising(self.sun)
        if self.localtime:
            sunrise = ephem.localtime(sunrise)
        else: sunrise = sunrise.datetime()
        
        if date: self.setdate(previous)
        
        return sunrise
    
    def sunset(self, date=None):
        if date:
            previous = self.date
            self.setdate(date)
        
        sunset = self.observer.next_setting(self.sun)
        if self.localtime:
            sunset = ephem.localtime(sunset)
        else: sunset = sunset.datetime()
        
        if date: self.setdate(previous)
        
        return sunset
    
    def getnext(self):
        self.setdate()
        
        sunrise = self.sunrise()
        sunset = self.sunset()
        
        return sunrise, sunset
    
    def getday(self):
        sunrise, sunset = self.getnext()
        
        if sunrise > sunset:
            sunrise = self.sunrise(self.date - datetime.timedelta(days=1))
        return sunrise, sunset
    
    def getnight(self):
        sunrise, sunset = self.getnext()
        
        if sunset > sunrise:
            sunset = self.sunset(self.date - datetime.timedelta(days=1))
        return sunrise, sunset
    
    def isday(self):
        now = datetime.datetime.now()
        if now > self.day[1]:
            self.day = self.getday()
        return (now > self.day[0] and now < self.day[1])
    
    def isnight(self):
        now = datetime.datetime.now()
        if now > self.night[0]:
            self.night = self.getnight()
        return (now < self.night[0] and now > self.night[1])
