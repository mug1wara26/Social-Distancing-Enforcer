import os

import wx
import cv2
import numpy as np

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
        self.BackgroundColour = wx.WHITE

        # os.getcwd() + r"\resources\WalkByShop1cor.mpg"

        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_resize(self, e):
        self.nb.SetSize(self.GetSize())

    def on_close(self, e):
        self.nb.Close()
        e.Skip()


class MainNotebook(wx.Notebook):
    def __init__(self, parent):
        super().__init__(parent)
        self.dots = np.array((np.array((0, 0)), np.array((20, 0)), np.array((0, 20)), np.array((20, 20))))

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        self.settings = UI.image.SettingsPanel(self)
        self.img_pane = UI.image.CV2ImagePanel(self, self.img_factory, r"resources/config_mode", cap)

        self.AddPage(self.img_pane, "Video")
        self.AddPage(self.settings, "Settings")

        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_BUTTON, self.on_button)
        self.Bind(wx.EVT_SCROLL_CHANGED, self.on_slider_change)
        self.Bind(wx.EVT_RADIOBOX, self.on_inp_change)
        self.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_file_change)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_click(self, e):
        if self.img_pane.configuring and len(dots := self.img_pane.get_dots()) == 4:
            wx.CallLater(500, self.after_dot_config)
            self.dots = np.array(list(map(np.array, map(operator.methodcaller("Get"), dots))))
        e.Skip()

    def after_dot_config(self):
        self.img_pane.dotting = False
        self.img_pane.configuring = False
        self.img_pane.clear_dots()
        self.settings.config_but.Enable(True)

    def on_slider_change(self, e):
        self.img_pane.thresholds[0] = self.settings.slider1.GetValue() / 100
        self.img_pane.thresholds[1] = 2 + self.settings.slider1.GetValue() / 10

    def on_button(self, e: wx.EVT_BUTTON):
        self.img_pane.dotting = True
        self.img_pane.configuring = True
        self.settings.config_but.Enable(False)
        self.SetSelection(0)

    def on_close(self, e):
        self.img_pane.on_close(e)
        e.Skip()

    def on_inp_change(self, e):
        if e.GetSelection():
            self.settings.file_picker.Enable(True)
        else:
            self.settings.file_picker.Enable(False)

    def on_file_change(self, e):
        cap = cv2.VideoCapture(self.settings.file_picker.GetPath())
        self.img_pane.cap = cap

    def img_factory(self, cap, thresholds):
        try:
            args = HumanTracking.get_boundaries(cap, thresholds[0])
        except cv2.error:
            if self.GetSelection() == 0:
                raise
            args = None

        if args is None:
            return None

        return HumanTracking.display_frame(*args, self.dots,
                                           float(self.settings.length_text.GetLineText(0)),
                                           float(self.settings.width_text.GetLineText(0)),
                                           thresholds[1], 1, 5)


app = wx.App()
MainFrame().Show()
app.MainLoop()
