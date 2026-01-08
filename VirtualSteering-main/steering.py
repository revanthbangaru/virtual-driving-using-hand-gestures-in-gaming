import cv2
import mediapipe as mp
import keyinput

font = cv2.FONT_HERSHEY_SIMPLEX

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# ================== STRICT THUMBS UP ==================
def is_thumbs_up(hand_landmarks):
    lm = hand_landmarks.landmark

    thumb_tip = lm[4]
    thumb_ip = lm[3]
    wrist = lm[0]

    # STRICT CONDITIONS:
    # 1. Thumb tip must be clearly above thumb joint
    # 2. Thumb tip must be clearly above wrist
    thumb_up = (thumb_tip.y < thumb_ip.y - 0.04) and (thumb_tip.y < wrist.y - 0.08)

    return thumb_up

# ================== KEY STATE ==================
state = {"w": False, "a": False, "s": False, "d": False, "space": False}

def set_key(key, pressed):
    if pressed and not state[key]:
        keyinput.press_key(key)
        state[key] = True
    elif not pressed and state[key]:
        keyinput.release_key(key)
        state[key] = False

with mp_hands.Hands(
    max_num_hands=2,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:

    while True:
        success, image = cap.read()
        if not success:
            continue

        image = cv2.flip(image, 1)
        h, w, _ = image.shape

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        hand_points = []
        thumbs_up_count = 0

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                cx = int(hand_landmarks.landmark[9].x * w)
                cy = int(hand_landmarks.landmark[9].y * h)
                hand_points.append((cx, cy))

                if is_thumbs_up(hand_landmarks):
                    thumbs_up_count += 1

        # ================== TARGET STATE ==================
        target = {"w": False, "a": False, "s": False, "d": False, "space": False}

        # ================== BOOST ==================
        if thumbs_up_count == 2:
            target["space"] = True
            cv2.putText(image, "BOOST", (50, 140), font, 1.2, (0,0,255), 3)

        # ================== DRIVING ==================
        if len(hand_points) == 2:
            # Sort hands by X to avoid random flip
            hand_points.sort(key=lambda p: p[0])

            (lx, ly) = hand_points[0]
            (rx, ry) = hand_points[1]

            diff = ly - ry
            DEAD_ZONE = 50

            if abs(diff) < DEAD_ZONE:
                target["w"] = True
                cv2.putText(image, "FORWARD", (50, 50), font, 1, (0,255,0), 2)

            elif diff > 0:
                target["w"] = True
                target["a"] = True
                cv2.putText(image, "LEFT", (50, 50), font, 1, (0,255,0), 2)

            else:
                target["w"] = True
                target["d"] = True
                cv2.putText(image, "RIGHT", (50, 50), font, 1, (0,255,0), 2)

        elif len(hand_points) == 1:
            target["s"] = True
            cv2.putText(image, "BACKWARD", (50, 50), font, 1, (0,255,0), 2)

        else:
            cv2.putText(image, "NO HANDS", (50, 50), font, 1, (0,0,255), 2)

        # ================== APPLY KEYS ==================
        for k in target:
            set_key(k, target[k])

        cv2.putText(image, f"Hands: {len(hand_points)}", (50, 100), font, 1, (255,0,0), 2)

        cv2.imshow("Virtual Steering", image)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

# ================== CLEANUP ==================
for k in state:
    if state[k]:
        keyinput.release_key(k)

cap.release()
cv2.destroyAllWindows()
