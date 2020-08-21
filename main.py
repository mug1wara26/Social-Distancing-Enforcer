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
        bot_row.Add(wx.StaticText(self, label="Overlap Threshold:"))
        bot_row.Add(self.slider)
        bot_row.AddSpacer(30)
        calib_but = wx.Button(self, label="&Calibrate")
        bot_row.Add(calib_but)
        bot_row.SetMinSize(self.img_panel.GetMinWidth() - 20, 20)

        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.v_sizer.Add(self.img_panel)
        self.v_sizer.Add(bot_row, 0, wx.ALL, 10)
        self.calib_text = wx.StaticText(self, label="CALIBRATION MODE")
        self.v_sizer.Add(self.calib_text, 1)
        self.calib_text.Hide()
        self.v_sizer.SetSizeHints(self)
        self.SetSizer(self.v_sizer)
        # self.v_sizer.Detach(self.calib_text)

        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.slider.Bind(wx.EVT_SCROLL_CHANGED, self.on_slider_change)
        calib_but.Bind(wx.EVT_BUTTON, self.on_calib)

    def on_close(self, e):
        self.img_panel.timer.Stop()
        self.cap.release()
        self.img_panel.Close()
        e.Skip()

    def on_slider_change(self, e):
        self.img_panel.set_threshold(self.slider.GetValue()/100)

    def on_calib(self, e):
        self.calib_text.Show()
        self.calib_text
        # self.v_sizer.Add(self.calib_text)


app = wx.App()
MainFrame().Show()
app.MainLoop()
