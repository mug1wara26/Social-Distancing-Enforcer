import wx
from .image import CV2ImagePanel

app = wx.App()
main_frame = wx.Frame(None)
cap = CV2ImagePanel(main_frame, lambda: 1)  # lambda is placeholder for the img factory
main_frame.Show()
app.MainLoop()
