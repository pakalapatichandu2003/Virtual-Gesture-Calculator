import cv2
import mediapipe as mp
import numpy as np
import time

# ---------- Animated & Attractive Project Info Screen ----------
def show_project_info():
    w, h = 1280, 720
    info_img = np.zeros((h, w, 3), dtype=np.uint8)

    # Create smooth gradient background (purple to blue)
    for i in range(h):
        color = (int(100 + (i / h) * 100), int(0 + (i / h) * 120), int(255 - (i / h) * 80))
        info_img[i, :] = color

    title = "VIRTUAL GESTURE CALCULATOR"
    subtitle = "Control a Calculator Using Hand Gestures!"
    author = "Developed by: Chandu"
    features = [
    "* Perform calculations without touching the keyboard!",
    "* Uses AI hand tracking with MediaPipe.",
    "* Real-time gesture-based input detection.",
    "* Modern UI with hover-based virtual buttons.",
    "* Option to save your calculation history."
]

    note = "Press any key to start..."

    # Fade-in animation for title
    for alpha in np.linspace(0, 1, 50):
        frame = info_img.copy()

        # Glowing effect for title
        for thickness in range(10, 2, -2):
            cv2.putText(frame, title, (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 2.3,
                        (255, 255, 255), thickness, cv2.LINE_AA)

        cv2.putText(frame, subtitle, (210, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.3,
                    (255, 255, 255), 3, cv2.LINE_AA)
        cv2.putText(frame, author, (340, 400), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 0), 2, cv2.LINE_AA)

        blended = cv2.addWeighted(info_img, 1 - alpha, frame, alpha, 0)
        cv2.imshow("Project Information", blended)
        if cv2.waitKey(30) & 0xFF != 255:
            cv2.destroyWindow("Project Information")
            return

    # Show features with soft fade-in scrolling style
    start_time = time.time()
    scroll_y = 460
    while True:
        frame = info_img.copy()
        cv2.putText(frame, title, (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 2.3, (255, 255, 255), 6, cv2.LINE_AA)
        cv2.putText(frame, subtitle, (210, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.putText(frame, author, (340, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

        # Display each feature line by line
        for i, line in enumerate(features):
            y = scroll_y + i * 40
            cv2.putText(frame, line, (150, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2, cv2.LINE_AA)

        # Pulsing "Press any key to start"
        brightness = int((np.sin(time.time() * 3) + 1) * 127.5)
        cv2.putText(frame, note, (420, 660), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, brightness, 0), 3, cv2.LINE_AA)

        cv2.imshow("Project Information", frame)
        key = cv2.waitKey(20) & 0xFF
        if key != 255 or time.time() - start_time > 10:
            break

if cv2.getWindowProperty("Project Information", cv2.WND_PROP_VISIBLE) >= 1:
    cv2.destroyWindow("Project Information")

show_project_info()


# ---------- Button Class ----------
class Button:
    def __init__(self, pos, width, height, text, color=(255, 255, 255)):
        self.pos = pos
        self.width = width
        self.height = height
        self.text = text
        self.hover_counter = 0
        self.pressed = False
        self.color = color

    def draw(self, img):
        x, y = self.pos
        overlay = img.copy()
        cv2.rectangle(overlay, (x, y), (x + self.width, y + self.height), (0, 0, 0), -1)
        alpha = 0.3
        img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
        cv2.rectangle(img, (x, y), (x + self.width, y + self.height), self.color, 2)

        # Center text
        text_size = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_PLAIN, 3, 3)[0]
        text_x = x + (self.width - text_size[0]) // 2
        text_y = y + (self.height + text_size[1]) // 2
        cv2.putText(img, self.text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 3, self.color, 3)
        return img

    def is_hover(self, x, y):
        return self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height


# ---------- Setup ----------
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Base layout (4x4)
button_values = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', '=', '+']
]

buttons = []

# Create regular 4x4 buttons
for y_idx, row in enumerate(button_values):
    for x_idx, val in enumerate(row):
        x = 100 + x_idx * 120
        y = 120 + y_idx * 120
        buttons.append(Button((x, y), 100, 100, val))

# Add merged Backspace "<x>" beside / and * (double height)
backspace_x = 100 + 4 * 120
backspace_y = 120
buttons.append(Button((backspace_x, backspace_y), 100, 220, "<x>", (0, 200, 255)))

# Add merged All Clear "AC" beside - and + (double height)
clear_x = 100 + 4 * 120
clear_y = 120 + 2 * 120
buttons.append(Button((clear_x, clear_y), 100, 220, "AC", (0, 100, 255)))

expression = ""
last_result = ""
history = []


def get_index_tip(hand_landmarks):
    if hand_landmarks:
        lm = hand_landmarks[0].landmark[8]
        return int(lm.x * 1280), int(lm.y * 720)
    return None


HOVER_TRIGGER_FRAMES = 15

print("🕐 Waiting 5 seconds or press 's' to start...")
start_time = time.time()
started = False

# ---------- Main Loop ----------
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    if not started:
        cv2.putText(img, "Waiting to Start... (Press 's' or wait 5 sec)", (150, 360),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        cv2.imshow("Virtual Calculator", img)

        key = cv2.waitKey(1) & 0xFF
        if time.time() - start_time > 5 or key == ord('s'):
            print("✅ Starting gesture detection...")
            started = True
        elif key == ord('q'):
            break
        continue

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    index_tip = None
    if results.multi_hand_landmarks:
        index_tip = get_index_tip(results.multi_hand_landmarks)
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    # Expression bar
    overlay = img.copy()
    cv2.rectangle(overlay, (90, 30), (1010, 100), (0, 0, 0), -1)
    img = cv2.addWeighted(overlay, 0.4, img, 0.6, 0)
    cv2.rectangle(img, (90, 30), (1010, 100), (255, 255, 255), 2)
    cv2.putText(img, expression, (110, 85), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)

    # Draw & handle buttons
    for button in buttons:
        img = button.draw(img)

        if index_tip and button.is_hover(*index_tip):
            button.hover_counter += 1
            cv2.rectangle(img, button.pos,
                          (button.pos[0] + button.width, button.pos[1] + button.height),
                          (0, 255, 0), 3)

            if button.hover_counter == HOVER_TRIGGER_FRAMES:
                val = button.text
                button.pressed = True

                if val == "=":
                    try:
                        result = str(eval(expression))
                        last_result = result
                        history.append(expression + " = " + result)
                        expression = result
                    except:
                        expression = "ERROR"
                elif val in ["CLR", "AC"]:
                    expression = ""
                elif val in ["BCK", "<x>"]:
                    expression = expression[:-1]
                else:
                    expression += val
        else:
            button.hover_counter = 0

    for button in buttons:
        if button.pressed:
            button.pressed = False
            button.hover_counter = 0

    cv2.imshow("Virtual Calculator", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        save_choice = input("Do you want to save calculation history as a text file? (y/n): ").strip().lower()
        if save_choice == 'y':
            filename = input("Enter file name (without extension): ").strip()
            with open(f"{filename}.txt", 'w') as f:
                f.write("\n".join(history))
            print(f"✅ History saved as {filename}.txt")
        else:
            print("❌ History not saved.")
        break

cap.release()
cv2.destroyAllWindows()





