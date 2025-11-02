"""hand_tracker.py
Utility wrapper around MediaPipe Hands to get landmarks and finger states.

Provides:
- HandTracker: class to process frames and return landmarks in pixel coords
- finger_up: helper to check if a finger is raised (simple PIP-vs-TIP y comparison)

"""
import cv2
import mediapipe as mp
import numpy as np


class HandTracker:
    def __init__(self, max_num_hands=1, detection_conf=0.7, track_conf=0.7):
        self.max_num_hands = max_num_hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False,
                                         max_num_hands=max_num_hands,
                                         min_detection_confidence=detection_conf,
                                         min_tracking_confidence=track_conf)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame, draw=True):
        """Processes an RGB frame and returns the results object."""
        # MediaPipe expects RGB
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        if draw and self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, handLms, self.mp_hands.HAND_CONNECTIONS)
        return self.results

    def get_landmark_positions(self, frame, hand_index=0):
        """Returns list of (id, x, y) in pixel coords for specified hand. Empty list if none."""
        h, w, _ = frame.shape
        lm_list = []
        if not hasattr(self, 'results') or not self.results.multi_hand_landmarks:
            return lm_list
        if hand_index >= len(self.results.multi_hand_landmarks):
            return lm_list

        hand = self.results.multi_hand_landmarks[hand_index]
        for i, lm in enumerate(hand.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)
            lm_list.append((i, cx, cy))
        return lm_list

    @staticmethod
    def finger_up(lm_list, finger_tip_id, finger_pip_id):
        """Simple check: tip y is above (smaller) than pip y -> finger considered up.
        lm_list: list of (id, x, y)
        Returns False if landmark ids not found.
        """
        id_to_pos = {id_: (x, y) for id_, x, y in lm_list}
        if finger_tip_id not in id_to_pos or finger_pip_id not in id_to_pos:
            return False
        tip_y = id_to_pos[finger_tip_id][1]
        pip_y = id_to_pos[finger_pip_id][1]
        return tip_y < pip_y

    @staticmethod
    def distance(p1, p2):
        """Euclidean distance between two (x,y) points."""
        return np.linalg.norm(np.array(p1) - np.array(p2))
