import wx
import cv2
import functools
import UI.image
from pyCv2 import HumanTracking


app = wx.App()
main_frame = wx.Frame(None)
img_panel = UI.image.CV2ImagePanel(main_frame, functools.partial(HumanTracking.display_frame, cv2.VideoCapture(0)))
main_frame.Show()
app.MainLoop()