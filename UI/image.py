import wx
from . import utils


class CV2ImagePanel(wx.Panel):
    def __init__(self, parent, image_factory, fps=15):
        super().__init__(parent)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.image_factory = image_factory
        self.circles = []

        # init the first frame
        frame = self.image_factory()
        dims = tuple(reversed(frame.shape[:2]))
        self.SetSize(*dims)
        self.SetSizeHints(*dims)

        self.bmp = wx.Bitmap.FromBuffer(*dims, frame)

        # update frame regularly
        self.timer = wx.Timer(self)
        self.timer.Start(int(1000 / fps))

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_TIMER, self.next_frame)

        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)

    def on_click(self, e):
        self.circles.append(e.GetPosition())

    def on_paint(self, e):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def next_frame(self, e):
        frame = self.image_factory()
        for pt in self.circles:
            utils.create_circle(frame, *pt)
        self.bmp.CopyFromBuffer(frame)
        self.Refresh()
