import wx
import cv2


class CV2ImagePanel(wx.Panel):
    def __init__(self, parent, image_factory, fps=15):
        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.image_factory = image_factory

        self.init_frame()

        self.timer = wx.Timer(self)
        self.timer.Start(int(1000 / fps))

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_TIMER, self.next_frame)

    def on_paint(self, e):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def init_frame(self):
        frame = self.image_factory()
        dims = tuple(reversed(frame.shape[:2]))
        self.parent.SetSize(*dims)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.bmp = wx.Bitmap.FromBuffer(*dims, frame)

    def next_frame(self, e):
        frame = self.image_factory()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.bmp.CopyFromBuffer(frame)
        self.Refresh()