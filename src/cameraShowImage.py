#!/usr/bin/env python3

from pypylon import pylon
import rospy
import sys
from sensor_msgs.msg import Image
from notCvBridge import cv2_to_imgmsg

class CameraShowImage:
    def __init__(self):
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices()
        if len(devices) == 0:
            raise rospy.logerr("No camera present.")

        # Create an array of instant cameras for the found devices and avoid exceeding a maximum number of devices.
        cameras = pylon.InstantCameraArray(len(devices))
        cam_number = 1
        for i in range(len(cameras)):
            self.camera[i] = pylon.InstantCamera()
            self.camera[i].Attach(tl_factory.CreateDevice(devices[cam_number]))
            self.camera[i].Open()
            self.camera[i].BslScalingEnable.SetValue(True)
            self.camera[i].Width.SetValue(1280)
            self.camera[i].Height.SetValue(720)
            self.camera[i].StartGrabbing()            

            print("Opened camera %d" % cam_number)
            cam_number += 1
            #change camera image size

        
        self.converter = pylon.ImageFormatConverter()
        # converting to opencv bgr format
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        #self.bridge = CvBridge()
        self.ImagePublisher = rospy.Publisher(('/camera/image_raw_'+sys.argv[1]), Image, queue_size=1)
        #self.CompressedImagePublisher = rospy.Publisher('/camera/image_raw/compressed', CompressedImage, queue_size=1)

    def run(self):
        grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if grabResult.GrabSucceeded():
            #convert to opencv bgr format
            image = self.converter.Convert(grabResult)
            #convert to opencv bgr format
            image = image.GetArray()
            #
            #cv2.imshow('image', image)
            #cv2.waitKey(0)
            #publish image
            self.ImagePublisher.publish(cv2_to_imgmsg(image))
            
            #compress image
            #compressed_image = CompressedImage()
            #compressed_image.header.stamp = rospy.Time.now()
            #compressed_image.format = "jpeg"
            #compressed_image.data = cv2.imencode('.jpg', image)[1].tostring()
            #self.CompressedImagePublisher.publish(compressed_image)



        #cv2.waitKey()
        grabResult.Release()




if (__name__ == "__main__"):

    rospy.init_node(('camera_show_image'+sys.argv[1]), anonymous=True)
    camera = CameraShowImage()
    rate = rospy.Rate(120)
    while not rospy.is_shutdown():
        camera.run()
        rate.sleep()
