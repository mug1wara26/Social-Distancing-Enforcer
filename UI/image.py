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
        self.thresholds = [0, 0]
        self.dotting = False
        self.configuring = False

        # init the first frame
        frame = self.image_factory(self.cap, self.thresholds)
        dims = tuple(reversed(frame.shape[:2]))
        self.SetSizeHints(*dims)
        self.bmp = wx.Bitmap.FromBuffer(*dims, frame)

        # start timer to know when to update frame
        self.timer = wx.Timer(self)
        self.timer.Start(int(1000 / fps))

        # binding functions
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_TIMER, self.next_frame)

        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_click(self, e):
        """If in config mode, display dot and propagate event"""
        if self.dotting:
            self.dots.append(e.GetPosition())
            e.ResumePropagation(1)
            e.Skip()

    def on_close(self, e):
        """Handle cleanup"""
        self.timer.Stop()
        self.cap.release()
        self.Close()
        e.Skip()

    def on_resize(self, e):
        """Resize the image when window is resized"""
        self.bmp = wx.Bitmap(self.bmp.ConvertToImage().Scale(*self.GetSize()))

    def on_paint(self, e):
        """Paint the image"""
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
        """Periodically replace frame with the next one"""
        frame = self.image_factory(self.cap, self.thresholds)
        if frame is None:
            return
        self.bmp = wx.Bitmap.FromBuffer(*self.GetSize(), cv2.resize(frame, tuple(self.GetSize())))
        self.Refresh()

    def get_dots(self):
        return self.dots

    def clear_dots(self):
        self.dots = []


class SettingsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.slider1 = wx.Slider(self, maxValue=100)
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row1.Add(wx.StaticText(self, label="Confidence:"), 0, wx.ALIGN_CENTER, 5)
        row1.AddSpacer(27)
        row1.Add(self.slider1)

        self.slider2 = wx.Slider(self, maxValue=100)
        row2 = wx.BoxSizer(wx.HORIZONTAL)
        row2.Add(wx.StaticText(self, label="Minimum Points:"), 0, wx.ALIGN_CENTER, 5)
        row2.Add(self.slider2)

        self.length_text = wx.TextCtrl(self, size=wx.Size(80, 22), value="1")
        self.width_text = wx.TextCtrl(self, size=wx.Size(80, 22), value="1")
        row3 = wx.BoxSizer(wx.HORIZONTAL)
        row3.Add(wx.StaticText(self, label="Length (m):"), 0, wx.ALIGN_CENTER, 5)
        row3.AddSpacer(10)
        row3.AddStretchSpacer(10)
        row3.Add(self.length_text)

        row4 = wx.BoxSizer(wx.HORIZONTAL)
        row4.Add(wx.StaticText(self, label="Width (m):"), 0, wx.ALIGN_CENTER, 5)
        row4.AddSpacer(8 + self.GetCharWidth())
        row4.AddStretchSpacer(10)
        row4.Add(self.width_text)

        row5 = wx.BoxSizer(wx.HORIZONTAL)
    
        inp_choice = wx.RadioBox(self, choices=["Webcam", "Video File"], majorDimension=1)
        inp_choice.SetSelection(0)
        row5.Add(inp_choice)
        row5.AddSpacer(10)
        row5.AddStretchSpacer(30)
        self.file_picker = wx.FilePickerCtrl(self)
        self.file_picker.Enable(False)
        row5.Add(self.file_picker, 0, wx.EXPAND, 5)

        v_sizer = wx.BoxSizer(wx.VERTICAL)
        row1.SetSizeHints(self)
        row2.SetSizeHints(self)
        row3.SetSizeHints(self)
        row4.SetSizeHints(self)
        row5.SetSizeHints(self)

        v_sizer.Add(row1, 0, wx.ALL, 10)
        v_sizer.Add(row2, 0, wx.ALL, 10)
        v_sizer.Add(row3, 0, wx.ALL, 10)
        v_sizer.Add(row4, 0, wx.ALL, 10)
        v_sizer.Add(row5, 0, wx.ALL, 10)
        self.config_but = wx.Button(self, label="Configure")
        v_sizer.Add(self.config_but)
        v_sizer.SetSizeHints(self)

        self.SetSizerAndFit(v_sizer)
