"""main.py

Run this script on Windows to control master volume using two-finger gestures.

How it works:
- Uses MediaPipe to find hand landmarks.
- Detects if index and middle fingers are both up.
- Measures distance between index-tip and middle-tip and maps it to volume (0-1).
- Uses pycaw to set system master volume in real-time.

Usage: python main.py

"""
import time
import argparse
import cv2
import numpy as np
from hand_tracker import HandTracker

try:
    from audio_controller import AudioController
    AUDIO_AVAILABLE = True
except Exception:
    AUDIO_AVAILABLE = False


def draw_volume_bar(img, vol_scalar, x=50, y=100, w=30, h=300):
    """Draw a vertical volume bar on img at (x, y) with height h."""
    # background
    cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 50), -1)
    # filled
    filled_h = int(h * vol_scalar)
    cv2.rectangle(img, (x, y + h - filled_h), (x + w, y + h), (0, 200, 0), -1)
    # border
    cv2.rectangle(img, (x, y), (x + w, y + h), (200, 200, 200), 2)
    # text
    cv2.putText(img, f'{int(vol_scalar*100)}%', (x - 10, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)


def main(camera_index=0, no_audio=False):
    cap = cv2.VideoCapture(camera_index)
    tracker = HandTracker(max_num_hands=1)

    audio = None
    if not no_audio:
        if not AUDIO_AVAILABLE:
            print('Audio control dependencies not available. Run with --no-audio for demo-only mode.')
            no_audio = True
        else:
            try:
                audio = AudioController()
            except Exception as e:
                print('Failed to initialize AudioController:', e)
                no_audio = True

    prev_time = 0
    smooth_vol = 0.0
    alpha = 0.2  # smoothing factor

    # calibration values (these may be adjusted if your hand appears small/large)
    MIN_DIST = 20   # px -> corresponds to volume ~0
    MAX_DIST = 200  # px -> corresponds to volume ~1

    print('Press ESC to quit')
    while True:
        ret, frame = cap.read()
        if not ret:
            print('Failed to grab frame')
            break

        frame = cv2.flip(frame, 1)
        tracker.find_hands(frame, draw=True)
        lm_list = tracker.get_landmark_positions(frame)

        if lm_list:
            # landmark ids: index tip=8, index pip=6, middle tip=12, middle pip=10
            index_up = tracker.finger_up(lm_list, 8, 6)
            middle_up = tracker.finger_up(lm_list, 12, 10)

            # get coordinates for tips
            id_to_pos = {id_: (x, y) for id_, x, y in lm_list}
            if 8 in id_to_pos and 12 in id_to_pos and index_up and middle_up:
                p1 = id_to_pos[8]
                p2 = id_to_pos[12]
                # draw connection
                cx, cy = (int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2))
                cv2.circle(frame, p1, 8, (0, 255, 0), -1)
                cv2.circle(frame, p2, 8, (0, 255, 0), -1)
                cv2.line(frame, p1, p2, (255, 0, 0), 2)
                cv2.circle(frame, (cx, cy), 10, (255, 0, 255), -1)

                # distance
                dist = tracker.distance(p1, p2)
                # map to 0-1
                vol = np.interp(dist, [MIN_DIST, MAX_DIST], [0.0, 1.0])
                vol = float(min(max(vol, 0.0), 1.0))
                # smooth
                smooth_vol = smooth_vol * (1 - alpha) + vol * alpha

                if not no_audio and audio is not None:
                    audio.set_volume(smooth_vol)

                # draw volume circle
                cv2.putText(frame, f'Vol: {int(smooth_vol*100)}%', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2)
            else:
                # when gesture not detected, show hint
                cv2.putText(frame, 'Show index+middle fingers (both up) to control volume', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200,200,200), 2)

        # draw volume bar on right
        try:
            vol_to_draw = smooth_vol
        except NameError:
            vol_to_draw = 0.0
        h, w, _ = frame.shape
        draw_volume_bar(frame, vol_to_draw, x=w-80, y=80, w=40, h=300)

        # FPS
        cur_time = time.time()
        fps = 1 / (cur_time - prev_time) if prev_time else 0.0
        prev_time = cur_time
        cv2.putText(frame, f'FPS: {int(fps)}', (10, frame.shape[0]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        cv2.imshow('Volume Control (press ESC to quit)', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--camera', type=int, default=0, help='camera index')
    parser.add_argument('--no-audio', action='store_true', help='run without changing system audio (demo mode)')
    args = parser.parse_args()
    main(camera_index=args.camera, no_audio=args.no_audio)
