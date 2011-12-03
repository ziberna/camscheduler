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

from tools import dictmerge

defaults = {
    # camera settings
    'device':None, # make SchedCam ask for device
    'resolution':(640,480),
    'format':'RGB',
    'takes':10,
    # nightsky settins
    'lat':'46.55',
    'long':'15.64',
    # file & directory settings
    'basedir':'images',
    'dirname':'%Y-m/%d',
    'filename':'%Y-%m-%d_%H-%M-%S',
    'filetype':'jpg'
}

def file(path='conf'):
    conf = {}
    try:
        with open(path, 'r') as file:
            lines = [line.strip() for line in file.read().split('\n')]
            lines = [line for line in lines if line != '' and not line.startswith('#')]
            for line in lines:
                line = line.partition('=')
                if line[1] == '=':
                    conf[line[0].strip()] = line[2].strip()
                elif line[0] == '=':
                    conf[line[1].strip()] = True
    except IOError:
        pass
    return conf

def parse(conf):
    conf = dictmerge(conf)
    
    # resolution
    try:
        res = tuple([int(num.strip()) for num in conf['resolution'].split('x')])
        if len(res) < 2:
            res = (res[0], int(float(res[0])/4*3))
        elif len(res) > 2:
            res = tuple([res[0],res[1]])
    except ValueError, KeyError:
        res = defaults['resolution']
    finally:
        conf['resolution'] = res
    
    # takes
    try:
        takes = int(conf['takes'])
    except ValueError, KeyError:
        takes = defaults['takes']
    finally:
        conf['takes'] = takes
    
    # dir paths
    conf['basedir'] = conf['basedir'].rstrip('/')
    conf['dirname']= conf['dirname'].strip('/')
    
    return conf

def get(path='conf'):
    conf = file(path)
    conf = parse(conf)
    return conf
