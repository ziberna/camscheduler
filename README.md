camscheduler
============

Features
--------
- cron-like schedule table of image captures
- capturing images based on sunrises and sunsets with custom delays and intervals
- settings for latitude and longitude (sunrises and sunsets are based on your location)
- custom filetype, image format and image size
- custom number of camera takes (increasing image quality)
- custom directory tree formats based on date of capturing

See `conf` file for an example configuration.

Dependencies
------------

camscheduler uses py-scheduler (https://github.com/jzib/py-scheduler).

Other dependencies:

- pygame (for capturing images from camera)
- pyephem (for calculating sunrises and sunsets)
