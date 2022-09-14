#!/usr/bin/env python3

from pypylon import pylon
import numpy as np
import cv2
import rospy
from sensor_msgs.msg import Image
from notCvBridge import imgmsg_to_cv2, cv2_to_imgmsg
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import sys
#from cv_bridge import CvBridge
class CameraShowImage:
    def __init__(self):
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices()
        info = pylon.DeviceInfo()
        info.SetSerialNumber("401460142")
        if len(devices) == 0:
            raise rospy.logerr("No camera present.")
            
            
        self.camera = pylon.InstantCamera(tl_factory.GetInstance().CreateFirstDevice(info))
        self.camera.Attach(tl_factory.CreateFirstDevice())
        self.camera.Open()
        self.camera.BslScalingEnable.SetValue(True)
        self.camera.Width.SetValue(1280)
        self.camera.Height.SetValue(720)
        #change camera image size
        self.camera.StartGrabbing(1)
        self.converter = pylon.ImageFormatConverter()
        # converting to opencv bgr format
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        #self.bridge = CvBridge()
        self.ImagePublisher = rospy.Publisher('/camera/image_raw'+sys.argv[1], Image, queue_size=1)

    def run(self):
        grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if grabResult.GrabSucceeded():
            #convert to opencv bgr format
            image = self.converter.Convert(grabResult)
            #convert to opencv bgr format
            image = image.GetArray()
            image = cv2.resize(image,(1048,780))

            #cv2.imshow('image', image)
            #cv2.waitKey(0)
            #publish image
            self.ImagePublisher.publish(cv2_to_imgmsg(image))
        #cv2.waitKey()
        grabResult.Release()
    
    #function to send images as a rtsp strem using gstreamer
    def send_image_stream(self):
        #create a video streaming server using g streamer and video from pypylon
        #!/usr/bin/env python3
        
        Gst.init(None)
        pipeline = Gst.Pipeline.new('rtsp-pipeline')
        rtspsrc = Gst.ElementFactory.make('rtspsrc', 'rtspsrc')
        rtspsrc.set_property('location', 'rtsp://admin:')




if (__name__ == "__main__"):
    rospy.init_node('camera_show_image', anonymous=True)
    camera = CameraShowImage()
    rate = rospy.Rate(120)
    while not rospy.is_shutdown():
        camera.run()
        rate.sleep()
