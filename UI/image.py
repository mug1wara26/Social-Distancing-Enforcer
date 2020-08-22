import wx
import cv2

import operator


class CV2ImagePanel(wx.Panel):
    def __init__(self, parent, image_factory, config_png_name, cap, fps=15):
        super().__init__(parent)
        config_img_bitmap = wx.Bitmap(wx.Image(config_png_name + ".png", wx.BITMAP_TYPE_ANY).Scale(200, 30))
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
        self.SetSizeHints(*dims)
        self.bmp = wx.Bitmap.FromBuffer(*dims, frame)

        # update frame regularly
        self.timer = wx.Timer(self)
        self.timer.Start(int(1000 / fps))

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_TIMER, self.next_frame)

        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.settings = None

    def on_click(self, e):
        if self.dotting:
            self.dots.append(e.GetPosition())
            e.ResumePropagation(1)
            e.Skip()

    def on_close(self, e):
        self.timer.Stop()
        self.cap.release()
        self.Close()
        e.Skip()


    def on_resize(self, e):
        self.bmp = wx.Bitmap(self.bmp.ConvertToImage().Scale(*self.GetSize()))

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
        self.bmp = wx.Bitmap.FromBuffer(640, 360, cv2.resize(frame, (640, 360)))
        self.Refresh()

    def get_dots(self):
        return self.dots

    def clear_dots(self):
        self.dots = []


class SettingsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.slider = wx.Slider(self, maxValue=100)
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row1.Add(wx.StaticText(self, label="Confidence:"), 0, wx.ALIGN_CENTER, 5)
        row1.Add(self.slider)
        row1.AddStretchSpacer(20)

        self.config_but = wx.Button(self, label="Configure")
        self.length_text = wx.TextCtrl(self, size=wx.Size(80, 22))
        self.width_text = wx.TextCtrl(self, size=wx.Size(80, 22))
        row1.Add(self.config_but)
        row1.AddStretchSpacer(15)
        row1.Add(wx.StaticText(self, label="Length (m):"), 0, wx.ALIGN_CENTER, 5)
        row1.AddStretchSpacer(10)
        row1.Add(self.length_text)
        row1.AddStretchSpacer(10)
        row1.Add(wx.StaticText(self, label="Width (m):"), 0, wx.ALIGN_CENTER, 5)
        row1.AddStretchSpacer(10)
        row1.Add(self.width_text)

        row2 = wx.BoxSizer(wx.HORIZONTAL)
        inp_choice = wx.RadioBox(self, choices=["Webcam", "Video File"], majorDimension=1)
        inp_choice.SetSelection(0)
        row2.Add(inp_choice)

        v_sizer = wx.BoxSizer(wx.VERTICAL)
        v_sizer.Add(row1)
        v_sizer.Add(row2)

        self.SetSizerAndFit(v_sizer)
