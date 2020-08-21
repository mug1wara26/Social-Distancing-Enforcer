import wx


class CV2ImagePanel(wx.Panel):
    def __init__(self, parent, image_factory, cap, fps=15):
        super().__init__(parent)
        config_img_bitmap = wx.Bitmap(wx.Image("resources/config_mode.png", wx.BITMAP_TYPE_ANY).Scale(200, 30))
        self.config_img_dims = config_img_bitmap.GetSize()
        self.config_img_dc = wx.MemoryDC(config_img_bitmap)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.image_factory = image_factory
        self.dots = []
        self.cap = cap
        self.threshold = 0
        self.dotting = False
        self.configuring = False

        # init the first frame
        frame = self.image_factory(self.cap, self.threshold)
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
        if self.dotting:
            self.dots.append(e.GetPosition())
            e.ResumePropagation(1)
            e.Skip()

    def on_paint(self, e):
        dc = wx.BufferedPaintDC(self, self.bmp)
        dc.DrawBitmap(self.bmp, 0, 0)
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 255), 2))
        for pt in self.dots:
            dc.DrawCircle(pt, 2)
            dc.DrawLines(self.dots)
        if self.configuring:
            dc.Blit(0, 0, *self.config_img_dims, self.config_img_dc, 0, 0)
            if len(self.dots) == 4:
                dc.DrawLine(self.dots[0], self.dots[3])

    def next_frame(self, e):
        frame = self.image_factory(self.cap, self.threshold)
        self.bmp.CopyFromBuffer(frame)
        self.Refresh()

    def get_dots(self):
        return self.dots

    def clear_dots(self):
        self.dots = []
