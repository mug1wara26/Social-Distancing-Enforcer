def display_frame(cap):
    ret, frame = cap.read()
    if ret:
        return frame

