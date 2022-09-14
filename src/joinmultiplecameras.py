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
maxCamerasToUse = 2

#from cv_bridge import CvBridge
class CameraShowImage:
    def __init__(self):
        # Get the transport layer factory.
        tlFactory = pylon.TlFactory.GetInstance()

        # Get all attached devices and exit application if no device is found.
        devices = tlFactory.EnumerateDevices()
        if len(devices) == 0:
            raise pylon.RuntimeException("No camera present.")
            

        # Create an array of instant cameras for the found devices and avoid exceeding a maximum number of devices.
        self.cameras = pylon.InstantCameraArray(min(len(devices), maxCamerasToUse))
        l = self.cameras.GetSize()

        # Create and attach all Pylon Devices.
        for i, cam in enumerate(self.cameras):
            cam.Attach(tlFactory.CreateDevice(devices[i]))

            # Print the model name of the camera.
            print("Using device ", cam.GetDeviceInfo().GetModelName())

        # Starts grabbing for all cameras starting with index 0. The grabbing
        # is started for one camera after the other. That's why the images of all
        # cameras are not taken at the same time.
        # However, a hardware trigger setup can be used to cause all cameras to grab images synchronously.
        # According to their default configuration, the cameras are
        # set up for free-running continuous acquisition.
        rospy.logwarn(self.cameras)
        self.cameras.StartGrabbing()


        self.converter = pylon.ImageFormatConverter()
        # converting to opencv bgr format
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        #self.bridge = CvBridge()
        self.ImagePublisher = rospy.Publisher('/camera/joined_image', Image, queue_size=1)


    def run(self):
        grabResult = self.cameras[0].RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        grabResult2 = self.cameras[1].RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grabResult.GrabSucceeded() and grabResult2.GrabSucceeded():
            #convert to opencv bgr format
            image = self.converter.Convert(grabResult) 
            image2 = self.converter.Convert(grabResult2)

            #convert to opencv bgr format
            image = image.GetArray()
            image2 = image2.GetArray()
            
            #image = cv2.resize(image,(2096,1560))
            #image2 = cv2.resize(image2,(2096,1560))
            image = cv2.resize(image,(1048,780))
            image2 = cv2.resize(image2,(1048,780))
            # image = imutils.rotate_bound(image,-90)
            # image2 = imutils.rotate_bound(image2,90)
            # resimg = np.concatenate((image,image2),axis=1)image2 = cv2.resize(image2,(image2.shape/4,image2.size()/4))
            resimg = np.concatenate((image2,image),axis=1)
            resimg2 = cv2.Canny(resimg,100,200)
            #
            #cv2.imshow('image', image)
            #cv2.waitKey(0)
            #publish image
            self.ImagePublisher.publish(cv2_to_imgmsg())
        #cv2.waitKey()
        grabResult.Release()
        # if grabResult2.GrabSucceeded():
        #     #convert to opencv bgr format
        #     image = self.converter.Convert(grabResult2)
        #     #convert to opencv bgr format
        #     image = image.GetArray()
        #     #
        #     #cv2.imshow('image', image)
        #     #cv2.waitKey(0)
        #     #publish image
        #     self.ImagePublisher2.publish(cv2_to_imgmsg(image))
        # #cv2.waitKey()
        # grabResult2.Release()
    
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
