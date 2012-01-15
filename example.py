import camscheduler
cam = camscheduler.Cam(conf='conf',camtab='camtab')
if not cam.run():
    print 'Camera probably not connected.'
