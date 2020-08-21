import wx
import cv2
import UI.image
from pyCv2 import HumanTracking

import functools


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Social Distancing Enforcer")
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        #img_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, "")
        self.img_panel = UI.image.CV2ImagePanel(self, HumanTracking.display_frame, self.cap)
        #img_sizer.Add(self.img_panel)

        self.slider = wx.Slider(self, maxValue=100)
        # self.slider.SetSizeHints(100,1000)
        bot_row = wx.BoxSizer(wx.HORIZONTAL)
        bot_row.Add(wx.StaticText(self, wx.ID_ANY, "Overlap Threshold:"))
        bot_row.Add(self.slider)
        bot_row.SetMinSize(self.img_panel.GetMinWidth() - 20, 20)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.img_panel)
        sizer.Add(bot_row, 0, wx.ALL, 10)
        sizer.SetSizeHints(self)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.slider.Bind(wx.EVT_SCROLL_CHANGED, self.on_slider_change)

    def on_close(self, e):
        self.img_panel.timer.Stop()
        self.cap.release()
        self.img_panel.Close()
        e.Skip()

    def on_slider_change(self, e):
        self.img_panel.set_threshold(self.slider.GetValue()/100)


app = wx.App()
MainFrame().Show()
app.MainLoop()
