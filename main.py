import wx
import UI.image
from pyCv2 import HumanTracking

app = wx.App()
main_frame = wx.Frame(None)
img_panel = UI.image.CV2ImagePanel(main_frame, HumanTracking.display_frame)  # lambda is placeholder for the img factory
main_frame.Show()
app.MainLoop()

