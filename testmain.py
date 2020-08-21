import wx
import UI.image

app = wx.App()
main_frame = wx.Frame(None)
click_frame = UI.image.PointSelectionPanel(main_frame)
main_frame.Show()
print(dir(wx.MouseEvent))
app.MainLoop()