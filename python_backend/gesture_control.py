import cv2
import mediapipe as mp
import pyautogui
from python_backend.logger import log_info, log_error, log_warning

def start_gesture_control():
    """Start gesture control in a separate thread"""
    cam = None
    try:
        log_info("Starting gesture control...")
        
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

        cam = cv2.VideoCapture(0)
        
        if not cam.isOpened():
            log_warning("Camera not available for gesture control")
            return

        log_info("Gesture control active")
        gesture_cooldown = 0

        while True:
            ret, frame = cam.read()
            if not ret:
                log_error("Failed to read from camera")
                break
                
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            # Simple gesture: hand detected = volume up (with cooldown)
            if result.multi_hand_landmarks and gesture_cooldown == 0:
                pyautogui.press("volumeup")
                gesture_cooldown = 30  # Cooldown frames
            
            if gesture_cooldown > 0:
                gesture_cooldown -= 1

            cv2.imshow("VEDA AI Gesture", frame)
            
            # ESC to exit
            if cv2.waitKey(1) == 27:
                log_info("Gesture control stopped by user")
                break
                
    except AttributeError as e:
        log_warning(f"Gesture control disabled: MediaPipe version issue - {e}")
    except Exception as e:
        log_error(f"Gesture control error: {e}")
    finally:
        if cam is not None:
            try:
                cam.release()
            except:
                pass
        try:
            cv2.destroyAllWindows()
        except:
            pass
        log_info("Gesture control cleanup completed")