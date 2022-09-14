#!/usr/bin/env python3

"""Create a ros program that reads the left eye position from the EyeTracking.csv file and plots it on a graph."""
from tokenize import String
import ciso8601
from math import atan2, degrees, sqrt
import pandas as pd
import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Vector3
import time

def callback(self,data):
    rospy.logwarn(rospy.get_caller_id() + "I heard %s", data.x)
    


class eyecontrol():
    def __init__(self):
        self.vector = Vector3()
        self.yawPub = rospy.Publisher('/eye_yaw', Float32, queue_size=1)
        self.pitchPub = rospy.Publisher('/eye_pitch', Float32, queue_size=1)
        self.vectorSub = rospy.Subscriber('/ojo_derecho', Vector3, self.callback )
        # get datetime format from a string like 22-06-30 12:56:03.902
        self.timeStart = rospy.get_time()
        self.pitch =0
        self.yaw = 0
    
    def callback(self, data):
        self.vector.x = data.x
        self.vector.y = data.y
        self.vector.z = data.z

    
    
    def run(self):
        
        while True:
            #print('Ojo abierto')
            pitch = Float32()
            yaw = Float32()
            pitch.data, yaw.data =self.calculateAngle(self.vector.x, self.vector.y, self.vector.z)
            offset_yaw = Float32(90)
            offset_yaw.data = 90
            self.yawPub.publish(yaw)
            self.pitchPub.publish(pitch)
            
            


    #kalman filter
    def kalman(self, pitch, yaw ):
        kalmangain = .5
        #pitch
        self.pitch = self.pitch+kalmangain*(pitch-self.pitch)
        #yaw
        self.yaw = self.yaw + kalmangain*(yaw - self.yaw)
        print(pitch, yaw, self.pitch, self.yaw)
        return self.pitch, self.yaw


    def calculateAngle(self, x, y, z):
        #print(x, y, z)
        yaw = -(degrees(atan2(x, -z)) - 90) # 90 is because it was looking up, the - is because when the eyes lokked up the mechanism was going down
        val = sqrt(z**2 + x**2) + 0
        pitch = degrees(-atan2(y,val))
        
        return self.kalman(pitch, yaw)







def main():
    """Create a ros program that reads the left eye position from the EyeTracking.csv file and plots it on a graph."""
    # Create a ros node named 'data_test'
    rospy.init_node('data_test', anonymous=True)
    rate = rospy.Rate(120) 
    # Create a new instance of the data class
    data = eyecontrol()
    # Loop until the node is shutdown
    while (not rospy.is_shutdown()):
        data.run()
        rate.sleep()




if (__name__=="__main__"):
    main()
    