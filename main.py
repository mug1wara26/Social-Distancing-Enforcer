import os

import wx
import cv2
import UI.image
from pyCv2 import HumanTracking

import operator


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Social Distancing Enforcer")

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.nb = MainNotebook(self)
        sizer.Add(self.nb)
        self.SetSizerAndFit(sizer)

        # os.getcwd() + r"\resources\WalkByShop1cor.mpg"

        self.Bind(wx.EVT_SIZE, self.on_resize)

    def on_resize(self, e):
        self.nb.SetSize(self.GetSize())


class MainNotebook(wx.Notebook):
    def __init__(self, parent):
        super().__init__(parent)

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        self.img_pane = self.create_img_pane(self, cap)
        self.settings = UI.image.SettingsPanel(self)

        self.AddPage(self.img_pane, "Video")
        self.AddPage(self.settings, "Settings")

        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_BUTTON, self.on_config)
        self.Bind(wx.EVT_SCROLL_CHANGED, self.on_slider_change)
        self.Bind(wx.EVT_RADIOBOX, self.on_inp_change)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_click(self, e):
        if self.img_pane.configuring and len(dots := self.img_pane.get_dots()) == 4:
            wx.CallLater(500, self.after_dot_config)
            print(list(map(operator.methodcaller("Get"), dots)))  # use for dis estim
            print(self.settings.length_text.GetLineText(0), self.settings.width_text.GetLineText(0))
            print(self.img_pane.get_dots())
        e.Skip()

    def after_dot_config(self):
        self.img_pane.dotting = False
        self.img_pane.configuring = False
        self.img_paneclear_dots()
        self.settings.config_but.Enable(True)

    def on_slider_change(self, e):
        self.img_pane.threshold = self.settings.slider.GetValue() / 100

    def on_config(self, e):
        self.img_pane.dotting = True
        self.img_pane.configuring = True
        self.settings.config_but.Enable(False)

    def on_close(self, e):
        self.img_pane.on_close(e)

    def on_inp_change(self, e):
        self.img_pane.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        print(e.GetSelection())

    @staticmethod
    def create_img_pane(parent, cap):
        return UI.image.CV2ImagePanel(parent, lambda a, b: HumanTracking.display_frame(
            *HumanTracking.get_boundaries(a, b)), r"resources/config_mode", cap)


app = wx.App()
MainFrame().Show()
app.MainLoop()
