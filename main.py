import wx
import cv2
import UI.image
from pyCv2 import HumanTracking

import functools


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Social Distancing Enforcer")
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        img_panel = UI.image.CV2ImagePanel(self, functools.partial(HumanTracking.display_frame, self.cap))
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, e):
        self.cap.release()
        e.Skip()


app = wx.App()
MainFrame().Show()
app.MainLoop()
