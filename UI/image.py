import wx


class CV2ImagePanel(wx.Panel):
    def __init__(self, parent, image_factory, fps=15):
        super().__init__(parent)

        self.parent = parent
        self.image_factory = image_factory

        # init the first frame
        frame = self.image_factory()
        dims = tuple(reversed(frame.shape[:2]))
        self.parent.SetSize(*dims)

        self.bmp = wx.Bitmap.FromBuffer(*dims, frame)

        # update frame regularly
        self.timer = wx.Timer(self)
        self.timer.Start(int(1000 / fps))

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_TIMER, self.next_frame)

    def on_paint(self, e):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def next_frame(self, e):
        frame = self.image_factory()
        self.bmp.CopyFromBuffer(frame)
        self.Refresh()


class PointSelectionPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)

    def on_click(self, e):
        print(e.getPosition())
