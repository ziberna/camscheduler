#    camscheduler (scheduler for capturing images from camera)
#    Copyright (C) 2011 Jure Žiberna
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

import os
import time
import thread

def istype(var, name): return (type(var).__name__ == name)

def isdict(var): return istype(var, 'dict')

def dictmerge(*dicts):
    merge = {}
    for dict in dicts:
        for key in dict:
            if isdict(dict[key]) and key in merge and isdict(merge[key]):
                merge[key] = dictmerge(merge[key], dict[key])
            else:
                merge[key] = dict[key]
    return merge

def dir(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except error:
            return False
    return True