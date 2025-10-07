#!/usr/bin/env python3
"""
Nail Biting Detector - macOS Menu Bar App
Detects when hands are near mouth/face and shows visual alerts
"""

# Suppress warnings
import os
import warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

import rumps
import cv2
import mediapipe as mp
import threading
import time
import math
from AppKit import NSScreen, NSWindow, NSColor, NSApplication


class NailBitingDetector(rumps.App):
    def __init__(self):
        super(NailBitingDetector, self).__init__(
            "👋",
            quit_button=rumps.MenuItem('Quit', key='q')
        )

        # State management
        self.is_monitoring = False
        self.monitoring_thread = None
        self.cap = None
        self.last_alert_time = 0
        self.alert_cooldown = 2  # seconds between alerts
        self.show_alert_flag = False

        # Detection settings
        self.sensitivity = 0.15  # Distance threshold (lower = more sensitive)

        # MediaPipe setup
        self.mp_hands = mp.solutions.hands
        self.mp_face_mesh = mp.solutions.face_mesh
        self.hands = None
        self.face_mesh = None

        # Timer to check for alerts on main thread
        self.alert_timer = rumps.Timer(self.check_alert_flag, 0.1)
        self.alert_timer.start()

    @rumps.clicked("Start Monitoring")
    def toggle_monitoring(self, sender):
        """Toggle monitoring on/off"""
        if self.is_monitoring:
            self.stop_monitoring()
        else:
            self.start_monitoring()

    @rumps.clicked("Sensitivity: High")
    def set_high(self, _):
        self.set_sensitivity(0.10, "High (Very Sensitive)")

    @rumps.clicked("Sensitivity: Medium")
    def set_medium(self, _):
        self.set_sensitivity(0.15, "Medium (Default)")

    @rumps.clicked("Sensitivity: Low")
    def set_low(self, _):
        self.set_sensitivity(0.20, "Low (Less Sensitive)")

    def set_sensitivity(self, value, name):
        """Set detection sensitivity"""
        self.sensitivity = value
        rumps.notification(
            title="Nail Guard",
            subtitle="Sensitivity Updated",
            message=f"Set to {name}"
        )

    def start_monitoring(self):
        """Start the camera monitoring"""
        self.is_monitoring = True

        # Update menu item
        menu_items = {item.title: item for item in self.menu.values() if hasattr(item, 'title')}
        if 'Start Monitoring' in menu_items:
            menu_items['Start Monitoring'].title = 'Stop Monitoring'

        self.title = "👁️"

        # Start monitoring in a separate thread
        self.monitoring_thread = threading.Thread(target=self.monitor_camera, daemon=True)
        self.monitoring_thread.start()

        rumps.notification(
            title="Nail Guard",
            subtitle="Monitoring Started",
            message="Camera is now watching for nail-biting behavior"
        )

    def stop_monitoring(self):
        """Stop the camera monitoring"""
        self.is_monitoring = False

        # Update menu item
        menu_items = {item.title: item for item in self.menu.values() if hasattr(item, 'title')}
        if 'Stop Monitoring' in menu_items:
            menu_items['Stop Monitoring'].title = 'Start Monitoring'

        self.title = "👋"

        # Release camera
        if self.cap:
            self.cap.release()
            self.cap = None

        # Close MediaPipe
        if self.hands:
            self.hands.close()
            self.hands = None
        if self.face_mesh:
            self.face_mesh.close()
            self.face_mesh = None

        rumps.notification(
            title="Nail Guard",
            subtitle="Monitoring Stopped",
            message="Camera monitoring has been disabled"
        )

    def monitor_camera(self):
        """Main monitoring loop - runs in separate thread"""
        try:
            # Initialize camera
            self.cap = cv2.VideoCapture(0)

            if not self.cap.isOpened():
                rumps.alert(
                    title="Camera Error",
                    message="Could not access camera. Please check permissions in System Settings > Privacy & Security > Camera"
                )
                self.stop_monitoring()
                return

            # Initialize MediaPipe
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )

            self.face_mesh = self.mp_face_mesh.FaceMesh(
                static_image_mode=False,
                max_num_faces=1,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )

            while self.is_monitoring:
                ret, frame = self.cap.read()

                if not ret:
                    continue

                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Detect hands
                hand_results = self.hands.process(rgb_frame)

                # Detect face
                face_results = self.face_mesh.process(rgb_frame)

                # Check if nail-biting detected
                if hand_results.multi_hand_landmarks and face_results.multi_face_landmarks:
                    if self.detect_nail_biting(hand_results, face_results, frame.shape):
                        self.trigger_alert()

                # Small delay to reduce CPU usage
                time.sleep(0.1)

        except Exception as e:
            print(f"Monitoring error: {e}")
            import traceback
            traceback.print_exc()

    def detect_nail_biting(self, hand_results, face_results, frame_shape):
        """
        Detect if hands are near mouth area
        Returns True if nail-biting behavior detected
        """
        height, width, _ = frame_shape

        # Get mouth landmarks (lips area)
        face_landmarks = face_results.multi_face_landmarks[0]

        # Mouth landmarks in MediaPipe Face Mesh
        mouth_landmarks = [13, 14, 61, 291, 0, 17]

        mouth_points = []
        for idx in mouth_landmarks:
            landmark = face_landmarks.landmark[idx]
            mouth_points.append((landmark.x, landmark.y))

        # Calculate average mouth position
        mouth_x = sum(p[0] for p in mouth_points) / len(mouth_points)
        mouth_y = sum(p[1] for p in mouth_points) / len(mouth_points)

        # Check each hand
        for hand_landmarks in hand_results.multi_hand_landmarks:
            # Check fingertips (landmarks 4, 8, 12, 16, 20)
            fingertips = [4, 8, 12, 16, 20]

            for tip_idx in fingertips:
                tip = hand_landmarks.landmark[tip_idx]

                # Calculate distance between fingertip and mouth
                distance = math.sqrt(
                    (tip.x - mouth_x) ** 2 +
                    (tip.y - mouth_y) ** 2
                )

                # If any fingertip is close to mouth, trigger alert
                if distance < self.sensitivity:
                    return True

        return False

    def trigger_alert(self):
        """Trigger visual alert if cooldown period has passed"""
        current_time = time.time()

        if current_time - self.last_alert_time < self.alert_cooldown:
            return

        self.last_alert_time = current_time
        self.show_alert_flag = True

    def check_alert_flag(self, _):
        """Check if we need to show an alert (runs on main thread)"""
        if self.show_alert_flag:
            self.show_alert_flag = False
            self.show_visual_alert()

    def show_visual_alert(self):
        """Show a visual popup alert using PyObjC"""
        try:
            # Get the main screen
            screen = NSScreen.mainScreen()
            screen_frame = screen.frame()

            # Create a full-screen window
            window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                screen_frame,
                0,  # No style mask = borderless
                2,  # NSBackingStoreBuffered
                False
            )

            # Configure window
            window.setBackgroundColor_(NSColor.colorWithCalibratedRed_green_blue_alpha_(1.0, 0.0, 0.0, 0.7))
            window.setOpaque_(False)
            window.setLevel_(NSApplication.sharedApplication().orderedWindows()[0].level() + 1)  # Above everything
            window.setIgnoresMouseEvents_(True)
            window.makeKeyAndOrderFront_(None)

            # Close after 0.5 seconds
            def close_window():
                window.close()

            threading.Timer(0.5, close_window).start()

        except Exception as e:
            print(f"Alert error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    app = NailBitingDetector()
    app.run()
