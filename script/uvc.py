#! /usr/bin/env python

import rospy
import time
import os
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class uvc_image():
    def __init__(self):
        rospy.init_node('camera_save_node')
        rospy.on_shutdown(self.shutdown)
        # function of transform ROS_image to opencv_image
        self.bridge = CvBridge()

        # ROS callback function, receive /image_raw mesage
        rospy.Subscriber('/image_raw', Image, self.image_callback)

        # prevents overwriting for saved images in the past
        self.file_path = os.path.expanduser('~') + "/images/"
        file_list = os.listdir(self.file_path)
        numbers=[]

        if len(file_list) > 0:
            for i in file_list:
                numbers.append(int(i[:-10]))
            self.group_number = max(numbers)+1
        else:
            self.group_number = 1
        print("group number is", self.group_number)
        self.seq = 1
        
    def image_callback(self, msg):
        # transform ROS_image to opencv_image
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            print "Cv_Brdige_Error"

    def shutdown(self):
        print "shutdown"

    def loop(self):
        while not rospy.is_shutdown():
            try:
                self.cv_image
            except AttributeError:
                continue

            cv2.imshow("", self.cv_image)
            key = cv2.waitKey(1)

            # save images
            if key == ord("s"):
                rgb_name = self.file_path +"{0:05d}".format(self.group_number) +"_" \
                           +"{0:05d}".format(self.seq) +".jpg"
                cv2.imwrite(rgb_name, self.cv_image)
                print(rgb_name, "is saved")
                self.seq = self.seq +1

            # next group_number
            if key == ord("n"):
                self.group_number = self.group_number +1
                print("move to the next group_number", self.group_number)
                self.seq = 1

            if key == 27: #[esc] key
                break
    
if __name__ == '__main__':
    u = uvc_image()
    u.loop()
