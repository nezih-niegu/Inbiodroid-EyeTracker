#!/usr/bin/python3
import sys, time
import cv2
import numpy as np
from threading import Thread
from pypylon import pylon

class EncoderStream:
  def __init__(self):
    self.current_frame = None
    self.cap = None
    self.ENCODE_PARAM = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
  
  def start(self, src = 0):
    tl_factory = pylon.TlFactory.GetInstance()
    self.camera = pylon.InstantCamera()
    self.camera.Attach(tl_factory.CreateFirstDevice())
    self.camera.Open()
    self.camera.BslScalingEnable.SetValue(True)
    self.camera.Width.SetValue(1920)
    self.camera.Height.SetValue(1080)
    #change camera image size
    self.camera.StartGrabbing(1)
    self.converter = pylon.ImageFormatConverter()
    # converting to opencv bgr format
    self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
    t = Thread(target = self.update_frame, args=())
    t.daemon = True
    t.start()
    return self

  def update_frame(self):
    while self.running():
      grab = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
      if(not grab.GrabSucceeded()):
        self.stop()
        return
      frame = self.converter.Convert(grab)
      frame = frame.GetArray()
      #frame = self.crop_aoi_img(frame)
      frame = self.resize_img(frame)
      _, imgencode = cv2.imencode('.jpg', frame, self.ENCODE_PARAM)
      data = np.array(imgencode)
      self.current_frame = data.tobytes()
      grab.Release()

  def stop(self):
    self.camera.Close()
  
  def running(self):
    return self.camera.IsOpen()

  def crop_aoi_img(self, frame):
    h = frame.shape[0]
    frame = frame[h//3:]
    fr = (frame.shape[0] // 2)
    frame = np.concatenate((frame[:,:fr], frame[:,-fr:]), axis = 1)
    return frame

  def resize_img(self, frame):
    frame = cv2.resize(frame, (1920, 1080))
    return frame