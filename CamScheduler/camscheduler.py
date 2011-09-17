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

# Camera modules
import pygame
import pygame.camera
from pygame.locals import *

# Other
import datetime
import time
import conf
import scheduler
import tools
import nightsky

class Cam(object):
    conf = conf.defaults
    camera = None
    datetime = None
    
    def __init__(self, conf='conf', camtab='camtab'):
        self.conf_init(conf)
        self.scheduler_init(camtab)
        self.dir_init()
        self.camera_init()
        if self.conf['nightsky']:
            self.nightsky_init()
    
    def conf_init(self, path='conf'):
        self.conf = conf.get(path)
    
    def scheduler_init(self, path='camtab'):
        self.jobs = scheduler.jobs(path=path)
        for job in self.jobs:
            if job.function == None:
                job.function = self.image
            elif job.function == 'video':
                job.function = self.video
            elif job.function == 'nightsky' and self.conf['nightsky']:
                job.function = self.image_nightsky
    
    def dir_init(self):
        tools.dir(self.conf['basedir'])
    
    def camera_init(self):
        pygame.init()
        pygame.camera.init()
        if self.conf['device'] == None:
            cameras = pygame.camera.list_cameras()
            if len(cameras) == 0:
                return False
            else:
                self.conf['device'] = cameras[0]
        
        self.camera = pygame.camera.Camera(
            self.conf['device'],
            self.conf['resolution'],
            self.conf['format']
        )
    
    def nightsky_init(self):
        self.nightsky = nightsky.NightSky(self.conf['lat'],self.conf['long'])
        self.sunset, self.sunrise = self.nightsky.today()
        self.sunset_delay = datetime.timedelta(minutes=self.conf['sunset_delay'])
        self.sunrise_delay = datetime.timedelta(minutes=self.conf['sunrise_delay'])
        self.datetime = datetime.datetime.now()
    
    def nightsky_update(self):
        now = datetime.datetime.now()
        if now > self.sunrise:
            self.sunset, self.sunrise = self.nightsky.today()
            self.sunset, self.sunrise = self.nightsky.today()
    
    def nightsky_isnow(self):
        now = datetime.datetime.now()
        return (now >= self.sunset + self.sunset_delay and now <= self.sunrise + self.sunrise_delay)
    
    def run(self):
        try:
            self.camera.start()
        except SystemError:
            return False
        scheduler.start(self.jobs, daemon=True)
        
        try:
            open('cam.lck','w').close()
            while True:
                time.sleep(1)
                try:
                    open('cam.lck').close()
                except IOError:
                    raise KeyboardInterrupt
        except KeyboardInterrupt:
            print 'CamScheduler terminated.'
            self.camera.stop()
        finally:
            return True
    
    def image(self, basedir=None, dirname=None, filename=None, filetype=None):
        self.datetime = datetime.datetime.now()
        image = self.capture_image()
        if image == None:
            return False
        path = self.filepath(basedir, dirname, filename, filetype, create_dir=True)
        self.save_image(image, path)
    
    def image_nightsky(self, basedir=None, dirname=None, filename=None, filetype=None):
        self.nightsky_update()
        if self.nightsky_isnow():
            self.image(basedir, dirname, filename, filetype)
    
    def video(self, seconds=5):
        pass # not implemented
    
    def capture_image(self):
        for n in range(self.conf['takes']):
            image = self.camera.get_image()
        return image
    
    def capture_video(self, seconds=5):
        pass # not implemented
    
    def save_image(self, image, file):
        print file
        pygame.image.save(image, file)
    
    def save_video(self, video, file):
        pass # not implemented
    
    def filepath(self, basedir=None, dirname=None, filename=None, filetype=None, create_dir=False):
        if basedir == None: basedir = self.conf['basedir']
        if dirname == None: dirname = self.conf['dirname']
        if filename == None: filename = self.conf['filename']
        if filetype == None: filetype = self.conf['filetype']
        
        dirname = self.datetime.strftime(dirname)
        filename = self.datetime.strftime(filename)
        path = basedir + '/' + dirname
        if create_dir:
            tools.dir(path)
        self.file = path + '/' + filename + '.' + filetype
        return self.file
