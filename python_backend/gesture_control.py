import cv2
import mediapipe as mp
import pyautogui
import math
from python_backend.logger import log_info, log_error, log_warning

class GestureRecognizer:
    """Recognizes hand gestures using MediaPipe landmarks"""
    
    def __init__(self):
        self.gesture_names = {
            'OPEN_PALM': 'Open Palm',
            'FIST': 'Fist',
            'PEACE': 'Peace Sign',
            'THUMBS_UP': 'Thumbs Up',
            'THUMBS_DOWN': 'Thumbs Down',
            'OK_SIGN': 'OK Sign',
            'POINTING': 'Pointing'
        }
    
    def count_fingers(self, landmarks):
        """Count extended fingers"""
        fingers = []
        
        # Thumb (check if tip is right of IP joint for right hand)
        if landmarks[4].x < landmarks[3].x:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # Other fingers (check if tip is above PIP joint)
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]
        
        for tip, pip in zip(finger_tips, finger_pips):
            if landmarks[tip].y < landmarks[pip].y:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers
    
    def get_distance(self, p1, p2):
        """Calculate distance between two points"""
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
    
    def recognize_gesture(self, landmarks):
        """Recognize gesture from hand landmarks"""
        fingers = self.count_fingers(landmarks)
        finger_count = sum(fingers)
        
        # Fist - no fingers extended
        if finger_count == 0:
            return 'FIST'
        
        # Open palm - all fingers extended
        if finger_count == 5:
            return 'OPEN_PALM'
        
        # Peace sign - index and middle finger up
        if finger_count == 2 and fingers[1] == 1 and fingers[2] == 1:
            return 'PEACE'
        
        # Pointing - only index finger up
        if finger_count == 1 and fingers[1] == 1:
            return 'POINTING'
        
        # OK sign - thumb and index forming circle
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        distance = self.get_distance(thumb_tip, index_tip)
        
        if distance < 0.05 and finger_count >= 3:
            return 'OK_SIGN'
        
        # Thumbs up - thumb up, other fingers closed
        if fingers[0] == 1 and sum(fingers[1:]) <= 1:
            # Check if thumb is pointing up
            if landmarks[4].y < landmarks[2].y:
                return 'THUMBS_UP'
        
        # Thumbs down - thumb down, other fingers closed
        if fingers[0] == 1 and sum(fingers[1:]) <= 1:
            if landmarks[4].y > landmarks[2].y:
                return 'THUMBS_DOWN'
        
        return None

def execute_gesture_action(gesture, last_gesture):
    """Execute action based on recognized gesture"""
    if gesture == last_gesture:
        return  # Avoid repeated actions
    
    try:
        if gesture == 'OPEN_PALM':
            pyautogui.press('playpause')
            log_info("Gesture: Play/Pause")
        
        elif gesture == 'PEACE':
            pyautogui.press('volumeup')
            log_info("Gesture: Volume Up")
        
        elif gesture == 'OK_SIGN':
            pyautogui.press('volumedown')
            log_info("Gesture: Volume Down")
        
        elif gesture == 'THUMBS_UP':
            pyautogui.press('nexttrack')
            log_info("Gesture: Next Track")
        
        elif gesture == 'THUMBS_DOWN':
            pyautogui.press('prevtrack')
            log_info("Gesture: Previous Track")
        
        elif gesture == 'FIST':
            pyautogui.press('volumemute')
            log_info("Gesture: Mute/Unmute")
        
        elif gesture == 'POINTING':
            log_info("Gesture: Pointing (no action)")
    
    except Exception as e:
        log_error(f"Error executing gesture action: {e}")

def start_gesture_control():
    """Start gesture control with real-time hand tracking"""
    cam = None
    try:
        log_info("Starting gesture control...")
        
        mp_hands = mp.solutions.hands
        mp_drawing = mp.solutions.drawing_utils
        
        hands = mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        recognizer = GestureRecognizer()
        cam = cv2.VideoCapture(0)
        
        if not cam.isOpened():
            log_warning("Camera not available for gesture control")
            return

        log_info("Gesture control active - Press ESC to exit")
        
        gesture_cooldown = 0
        last_gesture = None
        current_gesture = None

        while True:
            ret, frame = cam.read()
            if not ret:
                log_error("Failed to read from camera")
                break
            
            # Flip frame for mirror effect
            frame = cv2.flip(frame, 1)
            h, w, c = frame.shape
            
            # Convert to RGB for MediaPipe
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            # Process hand landmarks
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    # Draw hand landmarks
                    mp_drawing.draw_landmarks(
                        frame, 
                        hand_landmarks, 
                        mp_hands.HAND_CONNECTIONS
                    )
                    
                    # Recognize gesture
                    if gesture_cooldown == 0:
                        current_gesture = recognizer.recognize_gesture(hand_landmarks.landmark)
                        
                        if current_gesture:
                            execute_gesture_action(current_gesture, last_gesture)
                            last_gesture = current_gesture
                            gesture_cooldown = 30  # 30 frames cooldown
                    
                    # Display gesture name
                    if current_gesture:
                        gesture_name = recognizer.gesture_names.get(current_gesture, current_gesture)
                        cv2.putText(frame, f"Gesture: {gesture_name}", 
                                  (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                                  1, (0, 255, 0), 2)
            else:
                current_gesture = None
                last_gesture = None
            
            # Cooldown counter
            if gesture_cooldown > 0:
                gesture_cooldown -= 1
                cv2.putText(frame, f"Cooldown: {gesture_cooldown}", 
                          (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 
                          0.6, (0, 165, 255), 2)
            
            # Instructions
            cv2.putText(frame, "Press ESC to exit", 
                      (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                      0.5, (255, 255, 255), 1)
            
            cv2.imshow("VEDA AI Gesture Control", frame)
            
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