#!/usr/bin/env python
from math import cos, pi, sin
import rospy
from std_msgs.msg import Float32

class Ojos:
    def __init__(self):
        self.rate = rospy.Rate(20)
        self.yawPub = rospy.Publisher('/eye_yaw', Float32, queue_size=1)
        self.pitchPub = rospy.Publisher('/eye_pitch', Float32, queue_size=1)
        self.yaw = Float32()
        self.pitch = Float32()
        self.yaw.data = 0
        self.pitch.data = 0
        self.yawPub.publish(self.yaw)
        self.pitchPub.publish(self.pitch)
        self.state = "start"
        self.multiplier = 1.3

    def run(self):
        if (self.state =="start"):
            self.startTime = rospy.Time.now()
            self.state = "circles"
        #move in circles
        elif (self.state=="circles"):
            timeDiff = (rospy.Time.now() - self.startTime).to_sec()
            timeDiff *= 1*self.multiplier
            if (timeDiff < 4):
                self.yaw.data = sin(timeDiff*pi/2)*45
                self.pitch.data = cos(timeDiff*pi/2)*45
            else:
                self.state = "plus"
                self.startTime = rospy.Time.now()
        #move in plus
        elif (self.state=="plus"):
            timeDiff = (rospy.Time.now() - self.startTime).to_sec()
            timeDiff *= 2*self.multiplier
            if (timeDiff < 4):
                self.yaw.data = sin(timeDiff*pi/2)*45
                self.pitch.data = 0
            elif(timeDiff < 8):
                self.yaw.data = 0
                self.pitch.data = sin(timeDiff*pi/2)*45
            else:
                self.state = "HEight"
                self.startTime = rospy.Time.now()
        #Horizontal eight
        elif (self.state=="HEight"):
            timeDiff = (rospy.Time.now() - self.startTime).to_sec()
            timeDiff *= 1*self.multiplier
            if (timeDiff < 4):
                self.yaw.data = sin(timeDiff*pi/2)*45
                self.pitch.data = sin(timeDiff*pi)*45
            else:
                self.state = "VEight"
                self.startTime = rospy.Time.now()
        #Vertical eight
        elif (self.state=="VEight"):
            timeDiff = (rospy.Time.now() - self.startTime).to_sec()
            timeDiff *= 1*self.multiplier
            if (timeDiff < 4):
                self.yaw.data = sin(timeDiff*pi)*45
                self.pitch.data = sin(timeDiff*pi/2)*45
            else:
                self.state = "points"
                self.startTime = rospy.Time.now()
        elif (self.state=="points"):
            timeDiff = (rospy.Time.now() - self.startTime).to_sec()
            time = 2.0 #tiempo en segundos para dar una vuelta completa
            if (timeDiff < time/4):
                self.yaw.data = 0
                self.pitch.data = 45
            elif (timeDiff < time/4*2):
                self.yaw.data = 45
                self.pitch.data = 0
            elif (timeDiff < time/4*3):
                self.yaw.data = 0
                self.pitch.data = -45
            elif (timeDiff < time):
                self.yaw.data = -45
                self.pitch.data = 0
            else:
                self.state = "start"

        self.yawPub.publish(self.yaw)
        self.pitchPub.publish(self.pitch)




def main():
    rospy.init_node('ojos_test')
    rate = rospy.Rate(20)
    ojos = Ojos()
    while not rospy.is_shutdown():
        ojos.run()
        rate.sleep()


if (__name__ == "__main__"):
    main()
