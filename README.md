# 🖐️ Virtual Gesture Calculator

An interactive, touchless calculator application built with Python, OpenCV, and MediaPipe. Control an on-screen virtual calculator using hand gestures and hover-based button selection detected directly through your webcam.

---

## ✨ Features

* **🎨 Animated Intro Screen:** Startup screen with glowing title effects, features list, and smooth transitions.
* **🖐️ AI-Powered Hand Tracking:** Leverages Google's **MediaPipe** framework for real-time index finger tip detection.
* **⏱️ Hover-to-Click Mechanism:** Hover your index finger over any button for a short delay to trigger key presses cleanly without physical contact.
* **🖥️ Custom On-Screen UI:** Includes a translucent overlay layout featuring standard numbers, basic arithmetic operators (`+`, `-`, `*`, `/`), Backspace (`<x>`), and All Clear (`AC`).
* **💾 History Export:** Option to save your full calculation history to a `.txt` file upon exiting the application.

---

## 📁 Project Structure

```text
.
├── main.py              # Main Virtual Gesture Calculator Python script
├── requirements.txt     # Required Python dependencies
└── README.md            # Project documentation
⚙️ Installation & Setup
1. Prerequisites
Python 3.8 - 3.11

A functioning webcam

2. Install Dependencies
Open your terminal or command prompt in the project folder and run:

Bash
pip install -r requirements.txt
🚀 How to Run
Execute the main Python script:

Bash
python main.py
Startup Screen:

Watch the splash screen animation or press any key to skip directly to the calculator.

In-App Usage:

Start Detection: Wait 5 seconds or press the s key to begin gesture tracking.

Interact: Point your index finger at the screen to move the landmark pointer over the calculator buttons.

Select Button: Hold your index finger steady over a button to trigger the click.

Quit Application: Press the q key on your keyboard to exit.

Save History: After pressing q, check your terminal prompt if you wish to export your calculation history as a text file.
