#!/usr/bin/env python3

"""Create a ros program that reads the left eye position from the EyeTracking.csv file and plots it on a graph."""
import ciso8601
from math import atan2, degrees, sqrt
import pandas as pd
import rospy
from std_msgs.msg import Float32
import time

class DataReader():
    def __init__(self):

        self.data = pd.read_csv(rospy.get_param('/data_test/csv'))
        self.yawPub = rospy.Publisher('/eye_yaw', Float32, queue_size=1)
        self.pitchPub = rospy.Publisher('/eye_pitch', Float32, queue_size=1)
        # get datetime format from a string like 22-06-30 12:56:03.902
        start = 0
        t =ciso8601.parse_datetime("20"+self.data['timestamp'][start])
        self.timestamp =  time.mktime(t.timetuple())*1e3 +t.microsecond/1e3
        self.timeStart = rospy.get_time()
        self.pitch =0
        self.yaw = 0
        self.index = start
    
    def run(self):
        t = ciso8601.parse_datetime("20"+self.data['timestamp'][self.index])
        now = time.mktime(t.timetuple())*1e3 +t.microsecond/1e3
        diff = (now-self.timestamp)/1000
        if (diff < (rospy.get_time()-self.timeStart)):
            x = self.data['gazeDirectionRight.x'][self.index]
            y = self.data['gazeDirectionRight.y'][self.index]
            z = self.data['gazeDirectionRight.z'][self.index]
            if(self.data['eOpenR'][self.index]<0.8):
                None
                #print('Ojo cerrado')
            else:
                #print('Ojo abierto')
                pitch = Float32()
                yaw = Float32()
                pitch.data, yaw.data =self.calculateAngle(x, y, z)
                self.yawPub.publish(yaw)
                self.pitchPub.publish(pitch)
            
            self.index+=1
            if(self.index>=len(self.data)):
                rospy.signal_shutdown("End of data")   
            


    #kalman filter
    def kalman(self, pitch, yaw ):
        kalmangain = .5
        #pitch
        self.pitch = self.pitch+kalmangain*(pitch-self.pitch)
        #yaw
        self.yaw = self.yaw + kalmangain*(yaw - self.yaw)
        #print(pitch, yaw, self.pitch, self.yaw)
        return self.pitch, self.yaw


    def calculateAngle(self, x, y, z):
        #print(x, y, z)
        yaw = degrees(atan2(x, -z))
        val = sqrt(z**2 + x**2)
        pitch = degrees(-atan2(y,val))
        
        return self.kalman(pitch, yaw)







def main():
    """Create a ros program that reads the left eye position from the EyeTracking.csv file and plots it on a graph."""
    # Create a ros node named 'data_test'
    rospy.init_node('data_test', anonymous=True)
    rate = rospy.Rate(120) 
    # Create a new instance of the data class
    data = DataReader()
    # Loop until the node is shutdown
    while (not rospy.is_shutdown()):
        data.run()
        rate.sleep()




if (__name__=="__main__"):
    main()
    