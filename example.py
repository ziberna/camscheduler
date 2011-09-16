import camscheduler
cam = camscheduler.Cam()
if not cam.run():
    print 'Check your camera.'