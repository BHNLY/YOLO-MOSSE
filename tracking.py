import cv2
import time

cap = cv2.VideoCapture('videos/videovideo.mp4')


class Dogfight:
    def __init__(self):
        self.mosse_tracker = None
        self.tracking_active = False
        self.bbox = None
        self.frame = None
        self.mouse_x = 0
        self.mouse_y = 0
        self.square_size = 100  # Fixed frame size at startup
        self.min_square_size = 50 # Minimum size for frame
        self.max_square_size = 300 # Maximum size for frame
        self.yolo() # Leave the function with this name

    def yolo(self):
        self.prev_time = time.time()
        self.frame_count = 0
        self.fps_display = 0

        cv2.namedWindow("YOLOv5 with MOSSE")
        cv2.setMouseCallback("YOLOv5 with MOSSE", self.mouse_move)

        while cap.isOpened():
            self.ret, self.frame = cap.read()
            if not self.ret:
                break

           # self.frame = cv2.resize(self.frame, (640, 640))

            self.kareciz() # Create a shape where the mouse is hovering
            self.draw_center_square()  # Draw a fixed square in the middle of the screen
            
            if self.tracking_active and self.mosse_tracker is not None:
                self.mosse()

            self.fps()

            # Add tracker coordinates to the top left corner
            self.show_tracker_coordinates()

            cv2.imshow('YOLOv5 with MOSSE', self.frame)

            key = cv2.waitKey(30) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.reset_tracking()
            elif key == 81:  # Left arrow key
                self.square_size -= 10 # Reduce frame size
            elif key == 83:  # Right arrow key
                self.square_size += 10  # Increase frame size

            # Keep frame size within minimum and maximum limits
            self.square_size = max(self.min_square_size, min(self.square_size, self.max_square_size))

    def kareciz(self):
       # Draw the square in the center according to the mouse movement
        top_left_x = self.mouse_x - self.square_size // 2
        top_left_y = self.mouse_y - self.square_size // 2
        bottom_right_x = self.mouse_x + self.square_size // 2
        bottom_right_y = self.mouse_y + self.square_size // 2

       # Draw corner lines on the screen
        corner_size = 20  # Length of corner lines

        # Upper left corner lines
        cv2.line(self.frame, (top_left_x - corner_size, top_left_y - corner_size),
                 (top_left_x + corner_size, top_left_y - corner_size), (0, 255, 0), 2)
        cv2.line(self.frame, (top_left_x - corner_size, top_left_y - corner_size),
                 (top_left_x - corner_size, top_left_y + corner_size), (0, 255, 0), 2)

       # Top right corner lines
        cv2.line(self.frame, (bottom_right_x - corner_size, top_left_y - corner_size),
                 (bottom_right_x + corner_size, top_left_y - corner_size), (0, 255, 0), 2)
        cv2.line(self.frame, (bottom_right_x + corner_size, top_left_y - corner_size),
                 (bottom_right_x + corner_size, top_left_y + corner_size), (0, 255, 0), 2)

        # Bottom left corner lines
        cv2.line(self.frame, (top_left_x - corner_size, bottom_right_y + corner_size),
                 (top_left_x + corner_size, bottom_right_y + corner_size), (0, 255, 0), 2)
        cv2.line(self.frame, (top_left_x - corner_size, bottom_right_y + corner_size),
                 (top_left_x - corner_size, bottom_right_y - corner_size), (0, 255, 0), 2)

       # Bottom right corner lines
        cv2.line(self.frame, (bottom_right_x - corner_size, bottom_right_y + corner_size),
                 (bottom_right_x + corner_size, bottom_right_y + corner_size), (0, 255, 0), 2)
        cv2.line(self.frame, (bottom_right_x + corner_size, bottom_right_y - corner_size),
                 (bottom_right_x + corner_size, bottom_right_y + corner_size), (0, 255, 0), 2)

    def draw_center_square(self):
        # Draw a fixed square in the middle of the screen
        height, width, _ = self.frame.shape
        center_x, center_y = width // 2, height // 2

        # Dimension for fixed corner square
        fixed_square_size = 300
        top_left_x = center_x - fixed_square_size // 2
        top_left_y = center_y - fixed_square_size // 2
        bottom_right_x = center_x + fixed_square_size // 2
        bottom_right_y = center_y + fixed_square_size // 2

        # Draw corners
        corner_size = 20  # Length of corner lines

        # Upper left corner lines
        cv2.line(self.frame, (top_left_x - corner_size, top_left_y - corner_size),
                 (top_left_x + corner_size, top_left_y - corner_size), (255, 0, 0), 2)
        cv2.line(self.frame, (top_left_x - corner_size, top_left_y - corner_size),
                 (top_left_x - corner_size, top_left_y + corner_size), (255, 0, 0), 2)

       # Top right corner lines
        cv2.line(self.frame, (bottom_right_x - corner_size, top_left_y - corner_size),
                 (bottom_right_x + corner_size, top_left_y - corner_size), (255, 0, 0), 2)
        cv2.line(self.frame, (bottom_right_x + corner_size, top_left_y - corner_size),
                 (bottom_right_x + corner_size, top_left_y + corner_size), (255, 0, 0), 2)

        # Bottom left corner lines
        cv2.line(self.frame, (top_left_x - corner_size, bottom_right_y + corner_size),
                 (top_left_x + corner_size, bottom_right_y + corner_size), (255, 0, 0), 2)
        cv2.line(self.frame, (top_left_x - corner_size, bottom_right_y + corner_size),
                 (top_left_x - corner_size, bottom_right_y - corner_size), (255, 0, 0), 2)

       # Bottom right corner lines
        cv2.line(self.frame, (bottom_right_x - corner_size, bottom_right_y + corner_size),
                 (bottom_right_x + corner_size, bottom_right_y + corner_size), (255, 0, 0), 2)
        cv2.line(self.frame, (bottom_right_x + corner_size, bottom_right_y - corner_size),
                 (bottom_right_x + corner_size, bottom_right_y + corner_size), (255, 0, 0), 2)

    def mouse_move(self, event, x, y, flags, param):
       # Update position as mouse moves
        self.mouse_x = x
        self.mouse_y = y

        if event == cv2.EVENT_LBUTTONDOWN:
            # Left click to grab the current frame and start following
            self.bbox = (self.mouse_x - self.square_size // 2, self.mouse_y - self.square_size // 2, self.square_size,
                         self.square_size)
            self.activate_mosse()

    def activate_mosse(self):
        if self.bbox is not None:
            self.mosse_tracker = cv2.legacy.TrackerMOSSE_create()
            self.mosse_tracker.init(self.frame, self.bbox)
            self.tracking_active = True

    def mosse(self):
        if self.mosse_tracker is not None:
            success, bbox = self.mosse_tracker.update(self.frame)
            if success:
                x, y, w, h = [int(v) for v in bbox]
                cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                self.reset_tracking()

    def fps(self):
        self.frame_count += 1
        current_time = time.time()
        elapsed_time = current_time - self.prev_time

        # Faster FPS calculation
        if elapsed_time >= 0.1:  # Calculate every 0.1 seconds
            self.fps_display = self.frame_count / elapsed_time
            self.frame_count = 0
            self.prev_time = current_time

        cv2.putText(self.frame, f'FPS: {int(self.fps_display)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0),
                    2)

    def show_tracker_coordinates(self):
        if self.tracking_active and self.mosse_tracker is not None:
            success, bbox = self.mosse_tracker.update(self.frame)
            if success:
                x, y, w, h = [int(v) for v in bbox]
                coordinates_text = f'Tracker X: {x}, Y: {y}'

                # Creating text background and border
                text_size, _ = cv2.getTextSize(coordinates_text, cv2.FONT_HERSHEY_COMPLEX, 0.7, 2)
                text_width, text_height = text_size
                box_coords = (10, 200)
                cv2.rectangle(self.frame, (box_coords[0] - 5, box_coords[1] - text_height - 10),
                              (box_coords[0] + text_width + 5, box_coords[1] + 10), (0, 0, 0), -1)

                cv2.putText(self.frame, coordinates_text, box_coords, cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)

    def reset_tracking(self):
        self.mosse_tracker = None
        self.tracking_active = False


Dogfight()
