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
 
class NightSky(object):
    def __init__(self, lat, long):
        self.observer = ephem.Observer()
        self.observer.lat = lat
        self.observer.long = long
        self.sun = ephem.Sun()
    
    def today(self, localtime=True):
        now = datetime.datetime.now()
        self.observer.date = now
        
        sunset = self.observer.next_setting(self.sun)
        sunrise = self.observer.next_rising(self.sun)
        if localtime:
            sunset = ephem.localtime(sunset)
            sunrise = ephem.localtime(sunrise)
        return sunset, sunrise
