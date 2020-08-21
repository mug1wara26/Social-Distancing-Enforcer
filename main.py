import os

import wx
import cv2
import UI.image
from pyCv2 import HumanTracking

import operator


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Social Distancing Enforcer")

        nb = wx.Notebook(self)

        self.vid_pane = VideoPanel(nb)
        settings_pane = SettingsPanel(nb)

        nb.AddPage(self.vid_pane, "Video")
        nb.AddPage(settings_pane, "Settings")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nb)
        self.SetSizerAndFit(sizer)

        #os.getcwd() + r"\resources\WalkByShop1cor.mpg"

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, e):
        self.vid_pane.on_close(e)


class VideoPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.img_panel = UI.image.CV2ImagePanel(self, HumanTracking.display_frame, cv2.VideoCapture(0, cv2.CAP_DSHOW),
                                                r"resources/config_mode")

        self.slider = wx.Slider(self, maxValue=100)
        bot_row = wx.BoxSizer(wx.HORIZONTAL)
        bot_row.Add(wx.StaticText(self, label="Confidence:"), 0, wx.ALIGN_CENTER, 5)
        bot_row.Add(self.slider)
        bot_row.AddStretchSpacer(20)

        self.config_but = wx.Button(self, label="Configure")
        self.length_text = wx.TextCtrl(self, size=wx.Size(80, 22))
        self.width_text = wx.TextCtrl(self, size=wx.Size(80, 22))
        bot_row.Add(self.config_but)
        bot_row.AddStretchSpacer(15)
        bot_row.Add(wx.StaticText(self, label="Length (m):"), 0, wx.ALIGN_CENTER, 5)
        bot_row.AddStretchSpacer(10)
        bot_row.Add(self.length_text)
        bot_row.AddStretchSpacer(10)
        bot_row.Add(wx.StaticText(self, label="Width (m):"), 0, wx.ALIGN_CENTER, 5)
        bot_row.AddStretchSpacer(10)
        bot_row.Add(self.width_text)
        bot_row.SetMinSize(self.img_panel.GetMinWidth() - 20, 20)

        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.v_sizer.Add(self.img_panel)
        self.v_sizer.Add(bot_row, 0, wx.ALL, 10)
        self.SetSizerAndFit(self.v_sizer)

        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.slider.Bind(wx.EVT_SCROLL_CHANGED, self.on_slider_change)
        self.config_but.Bind(wx.EVT_BUTTON, self.on_config)

    def on_slider_change(self, e):
        self.img_panel.threshold = self.slider.GetValue() / 100

    def on_config(self, e):
        self.img_panel.dotting = True
        self.img_panel.configuring = True
        self.config_but.Enable(False)

    def on_click(self):
        if self.img_panel.configuring and len(dots := self.img_panel.get_dots()) == 4:
            wx.CallLater(500, self.after_dot_config)
            print(list(map(operator.methodcaller("Get"), dots)))  # use for dis estim
            print(self.length_text.GetLineText(0), self.width_text.GetLineText(0))  # l and w

    def after_dot_config(self):
        self.img_panel.dotting = False
        self.img_panel.configuring = False
        self.img_panel.clear_dots()
        self.config_but.Enable(True)

    def change_inp(self, e):
        self.img_panel.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        print(dir(e))

    def on_close(self, e):
        self.img_panel.timer.Stop()
        self.cap.release()
        self.img_panel.Close()
        e.Skip()


class SettingsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        sizer = wx.GridSizer(4, wx.Size(10, 10))

        inp_choice = wx.RadioBox(self, choices=["Webcam", "Video File"], majorDimension=1)
        inp_choice.SetSelection(0)
        # inp_choice.Bind(wx.EVT_RADIOBOX, VideoPanel.change_inp)

        sizer.Add(inp_choice)

        self.SetSizerAndFit(sizer)


app = wx.App()
MainFrame().Show()
app.MainLoop()
