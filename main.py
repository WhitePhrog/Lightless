import cv2
import mediapipe as mp
import time

mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
pose = mp_pose.Pose()
hands = mp_hands.Hands(max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

def is_fist(hand_landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    fingers_folded = 0
    for tip_id in tips_ids[1:]:
        if hand_landmarks.landmark[tip_id].y > hand_landmarks.landmark[tip_id - 2].y:
            fingers_folded += 1
    return fingers_folded >= 3

def are_both_arms_up(landmarks, img_h):
    l_sh = landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * img_h
    l_wr = landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y * img_h
    r_sh = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * img_h
    r_wr = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y * img_h
    return l_wr < l_sh and r_wr < r_sh

cap = cv2.VideoCapture(0)

gesture_triggered = {
    "open_hand": False,
    "fist": False,
    "both_arms": False
}
gesture_time = {
    "open_hand": 0,
    "fist": 0,
    "both_arms": 0
}
DISPLAY_DURATION = 3  # seconds

while True:
    success, img = cap.read()
    if not success:
        break
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = img.shape
    current_time = time.time()

    pose_result = pose.process(img_rgb)
    hands_result = hands.process(img_rgb)

    if pose_result.pose_landmarks:
        mp_draw.draw_landmarks(img, pose_result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    if hands_result.multi_hand_landmarks:
        for hand_landmarks in hands_result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            wrist_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * h

            if wrist_y < h * 0.5:
                if is_fist(hand_landmarks):
                    if not gesture_triggered["fist"]:
                        print("Punho fechado detectado")
                    gesture_triggered["fist"] = True
                    gesture_time["fist"] = current_time
                else:
                    if not gesture_triggered["open_hand"]:
                        print("Mao aberta detectada")
                    gesture_triggered["open_hand"] = True
                    gesture_time["open_hand"] = current_time

    if pose_result.pose_landmarks:
        if are_both_arms_up(pose_result.pose_landmarks, h):
            if not gesture_triggered["both_arms"]:
                print("Dois bracos erguidos detectado")
            gesture_triggered["both_arms"] = True
            gesture_time["both_arms"] = current_time
        else:
            gesture_triggered["both_arms"] = False

    # Draw messages if within display time
    if current_time - gesture_time["open_hand"] <= DISPLAY_DURATION:
        cv2.putText(img, "Mao aberta detectada!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if current_time - gesture_time["fist"] <= DISPLAY_DURATION:
        cv2.putText(img, "Punho fechado detectado!", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    if current_time - gesture_time["both_arms"] <= DISPLAY_DURATION:
        cv2.putText(img, "Dois bracos erguidos!", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Lightless - Gesture Detection", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
