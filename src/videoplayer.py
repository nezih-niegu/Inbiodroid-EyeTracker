#!/usr/bin/env python

"""open cv video player"""
import rospy
import cv2


def main():
    rospy.init_node('videoplayer', anonymous=True)
    cap = cv2.VideoCapture(rospy.get_param('/video/mp4'))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)
    rate =rospy.Rate(fps)
    start = (int)(fps*6.3)
    print(start)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start)
    
    while(not rospy.is_shutdown()):
        ret, frame = cap.read()
        if ret==True:
            cv2.imshow('frame',frame)
        
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
        rate.sleep()
 
    
if (__name__ == "__main__"):
    main()