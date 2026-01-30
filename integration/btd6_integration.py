"""
BTD6 Game Integration Layer
Captures screen and controls the real BTD6 game
"""

import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab
import time
from typing import Tuple, Optional, List


class BTD6Integration:
    """Integration with real BTD6 game"""

    def __init__(self, game_window_region: Optional[Tuple[int, int, int, int]] = None):
        """
        Initialize BTD6 integration

        Args:
            game_window_region: (x, y, width, height) of game window.
                               If None, will try to auto-detect
        """
        self.game_region = game_window_region
        pyautogui.PAUSE = 0.01  # Small pause between actions
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort

    def capture_screen(self) -> np.ndarray:
        """
        Capture game screen

        Returns:
            numpy array of screen (BGR format)
        """
        if self.game_region:
            screenshot = ImageGrab.grab(bbox=self.game_region)
        else:
            screenshot = ImageGrab.grab()

        # Convert PIL Image to numpy array
        img = np.array(screenshot)
        # Convert RGB to BGR for OpenCV
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img

    def click_at_position(self, x: int, y: int):
        """
        Click at game position

        Args:
            x, y: Pixel coordinates to click
        """
        if self.game_region:
            # Offset by window position
            x += self.game_region[0]
            y += self.game_region[1]

        pyautogui.click(x, y)

    def place_tower(self, tower_type: str, x: int, y: int):
        """
        Place tower at position

        Args:
            tower_type: Type of tower (e.g., "dart_monkey")
            x, y: Position to place tower
        """
        # Open tower menu (for Dart Monkey, press 'Z' or click icon)
        if tower_type == "dart_monkey":
            pyautogui.press('z')
        else:
            pyautogui.press('z')
        time.sleep(0.1)

        # Click position to place
        self.click_at_position(x, y)
        time.sleep(0.1)

    def start_round(self):
        """Start the next round (fallback to space)"""
        pyautogui.press('space')

    def start_round_auto(self, screen: Optional[np.ndarray] = None) -> bool:
        """
        Try to start the round by clicking the Start button on screen.
        Falls back to Space if not found.

        Returns:
            True if a click action was executed, False if fallback used.
        """
        if screen is None:
            screen = self.capture_screen()

        button_pos = self.detect_start_round_button(screen)
        if button_pos is not None:
            self.click_at_position(button_pos[0], button_pos[1])
            return True

        self.start_round()
        return False

    def detect_start_round_button(self, screen: np.ndarray) -> Optional[Tuple[int, int]]:
        """
        Detect the green Start Round button.

        Returns:
            (x, y) position of the button center relative to the game region, or None.
        """
        hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)

        # Green button range (tuned for typical BTD6 start button)
        lower_green = np.array([40, 80, 80])
        upper_green = np.array([85, 255, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)
        mask = cv2.medianBlur(mask, 5)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None

        # Choose largest green region near bottom-right
        h, w = screen.shape[:2]
        best = None
        best_score = -1
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 200:
                continue
            x, y, cw, ch = cv2.boundingRect(cnt)
            cx = x + cw // 2
            cy = y + ch // 2

            # Score: larger area + closer to bottom-right
            score = area + (cx / w) * 1000 + (cy / h) * 1000
            if score > best_score:
                best_score = score
                best = (cx, cy)

        return best

    def detect_game_window(self) -> Tuple[int, int, int, int]:
        """
        Detect (or assume) the game window region. For MVP we capture the full primary screen
        and set that as the game region. Returns (x, y, width, height).
        """
        # Capture full screen via PIL
        screenshot = ImageGrab.grab()
        width, height = screenshot.size
        # Use origin (0,0) for full-screen region
        self.game_region = (0, 0, width, height)
        return self.game_region

    def place_towers_hotkeys(self, actions: List[dict]):
        """
        Place towers in the real game using hotkeys and clicks.

        Args:
            actions: List of dicts {'type': str, 'x': int, 'y': int} where x,y are
                     pixel coordinates relative to the top-left of the game region.
        """
        for act in actions:
            tower_type = act.get("type", "dart_monkey")
            x = act.get("x")
            y = act.get("y")
            if x is None or y is None:
                continue

            # Press tower hotkey (MVP: dart monkey -> 'z')
            if tower_type == "dart_monkey":
                pyautogui.press("z")
            else:
                pyautogui.press("z")

            # Wait for tower selection menu to appear (0.2s delay as specified)
            time.sleep(0.2)

            # Click at the target position (convert to absolute screen coords)
            if self.game_region:
                abs_x = int(self.game_region[0] + x)
                abs_y = int(self.game_region[1] + y)
            else:
                abs_x = int(x)
                abs_y = int(y)

            self.click_at_position(abs_x, abs_y)
            time.sleep(0.15)

    def detect_track_path(self, screen: np.ndarray) -> List[Tuple[int, int]]:
        """
        Detect track path from screenshot and return ordered polyline.

        Returns:
            List of (x, y) points along the path.
        """
        mask = self._get_track_mask(screen)
        skeleton = self._skeletonize(mask)
        path = self._trace_skeleton_path(skeleton)
        return path

    def _get_track_mask(self, screen: np.ndarray) -> np.ndarray:
        """Create a mask for the track based on color heuristics."""
        hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)

        # Brown-ish path
        lower_brown = np.array([10, 40, 50])
        upper_brown = np.array([30, 180, 220])

        # Gray-ish path (low saturation)
        lower_gray = np.array([0, 0, 60])
        upper_gray = np.array([180, 40, 200])

        mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
        mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)

        mask = cv2.bitwise_or(mask_brown, mask_gray)

        # Clean up
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        return mask

    def _skeletonize(self, mask: np.ndarray) -> np.ndarray:
        """Skeletonize a binary mask using morphological thinning."""
        skel = np.zeros(mask.shape, np.uint8)
        element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        temp_mask = mask.copy()

        while True:
            eroded = cv2.erode(temp_mask, element)
            temp = cv2.dilate(eroded, element)
            temp = cv2.subtract(temp_mask, temp)
            skel = cv2.bitwise_or(skel, temp)
            temp_mask = eroded.copy()

            if cv2.countNonZero(temp_mask) == 0:
                break

        return skel

    def _trace_skeleton_path(self, skeleton: np.ndarray) -> List[Tuple[int, int]]:
        """Trace an ordered path through skeleton pixels."""
        coords = np.column_stack(np.where(skeleton > 0))
        if coords.size == 0:
            return []

        # Build a set for quick lookup
        points = {(int(x), int(y)) for y, x in coords}

        # Find endpoints (pixels with 1 neighbor)
        endpoints = []
        for (px, py) in points:
            neighbors = 0
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    if (px + dx, py + dy) in points:
                        neighbors += 1
            if neighbors == 1:
                endpoints.append((px, py))

        # Fallback: choose extreme points
        if len(endpoints) < 2:
            pts_list = list(points)
            pts_list.sort(key=lambda p: (p[0], p[1]))
            endpoints = [pts_list[0], pts_list[-1]]

        start = endpoints[0]
        visited = set()
        path = []
        current = start

        while current is not None:
            path.append(current)
            visited.add(current)
            next_point = None

            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    candidate = (current[0] + dx, current[1] + dy)
                    if candidate in points and candidate not in visited:
                        next_point = candidate
                        break
                if next_point is not None:
                    break

            current = next_point

        # Downsample path for usability
        if len(path) > 0:
            path = path[::10]

        # Convert back to (x, y)
        return [(p[0], p[1]) for p in path]

    def detect_balloons(self, screen: np.ndarray) -> list:
        """
        Detect balloons from screen capture using computer vision

        Args:
            screen: Screen capture as numpy array

        Returns:
            List of detected balloon positions and types
        """
        # TODO: Implement balloon detection using color segmentation
        # For MVP, this is a placeholder
        balloons = []

        # RED balloon detection (simple color threshold)
        hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)

        # Define red color range
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 + mask2

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:  # Filter small noise
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    balloons.append({"x": cx, "y": cy, "type": "red"})

        return balloons

    def detect_lives(self, screen: np.ndarray) -> int:
        """
        Detect remaining lives from screen (OCR or template matching)

        Args:
            screen: Screen capture

        Returns:
            Number of lives remaining
        """
        # TODO: Implement OCR for lives display
        # For MVP, return placeholder
        return 100

    def is_game_over(self, screen: np.ndarray) -> bool:
        """
        Check if game is over

        Args:
            screen: Screen capture

        Returns:
            True if game over screen detected
        """
        # TODO: Implement game over detection
        # For MVP, return False
        return False


# Example usage
if __name__ == "__main__":
    integration = BTD6Integration()

    print("Starting BTD6 integration test...")
    print("Make sure BTD6 is open and on the game screen!")
    print("Test will start in 3 seconds...")
    time.sleep(3)

    # Capture screen
    screen = integration.capture_screen()
    print(f"Screen captured: {screen.shape}")

    # Detect balloons
    balloons = integration.detect_balloons(screen)
    print(f"Detected {len(balloons)} balloons")

    # Save captured screen
    cv2.imwrite("btd6_screen_capture.png", screen)
    print("Screen saved to btd6_screen_capture.png")
