import wx
import cv2
import UI.image
from pyCv2 import HumanTracking

import operator


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Social Distancing Enforcer")
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        self.img_panel = UI.image.CV2ImagePanel(self, HumanTracking.display_frame, self.cap, "resources/config_mode")

        self.slider = wx.Slider(self, maxValue=100)
        # self.slider.SetSizeHints(100,1000)
        bot_row = wx.BoxSizer(wx.HORIZONTAL)
        bot_row.Add(wx.StaticText(self, label="Overlap Threshold:"), 0, wx.ALIGN_CENTER, 5)
        bot_row.Add(self.slider)
        bot_row.AddSpacer(20)

        self.config_but = wx.Button(self, label="Configure")
        self.length_text = wx.TextCtrl(self, size=wx.Size(80, 22))
        self.width_text = wx.TextCtrl(self, size=wx.Size(80, 22))
        bot_row.Add(self.config_but)
        bot_row.AddSpacer(15)
        bot_row.Add(wx.StaticText(self, label="Length (m):"), 0, wx.ALIGN_CENTER, 5)
        bot_row.AddSpacer(10)
        bot_row.Add(self.length_text)
        bot_row.AddSpacer(10)
        bot_row.Add(wx.StaticText(self, label="Width (m):"), 0, wx.ALIGN_CENTER, 5)
        bot_row.AddSpacer(10)
        bot_row.Add(self.width_text)
        bot_row.SetMinSize(self.img_panel.GetMinWidth() - 20, 20)

        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.v_sizer.Add(self.img_panel)
        self.v_sizer.Add(bot_row, 0, wx.ALL, 10)
        self.v_sizer.SetSizeHints(self)
        self.SetSizer(self.v_sizer)

        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.slider.Bind(wx.EVT_SCROLL_CHANGED, self.on_slider_change)
        self.config_but.Bind(wx.EVT_BUTTON, self.on_config)

    def on_close(self, e):
        self.img_panel.timer.Stop()
        self.cap.release()
        self.img_panel.Close()
        e.Skip()

    def on_slider_change(self, e):
        self.img_panel.threshold = self.slider.GetValue() / 100

    def on_config(self, e):
        self.img_panel.dotting = True
        self.img_panel.configuring = True
        self.config_but.Enable(False)

    def on_click(self, e):
        if self.img_panel.configuring and len(dots := self.img_panel.get_dots()) == 4:
            wx.CallLater(500, self.after_dot_config)
            print(list(map(operator.methodcaller("Get"), dots)))  # use for dis estim
            print(self.length_text.GetLineText(0), self.width_text.GetLineText(0))  # l and w

    def after_dot_config(self):
        self.img_panel.dotting = False
        self.img_panel.configuring = False
        self.img_panel.clear_dots()
        self.config_but.Enable(True)


app = wx.App()
MainFrame().Show()
app.MainLoop()
