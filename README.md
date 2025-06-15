# Chat Erasure Detection for Emotional Well-being
- This project is a real-time emotional well-being monitoring system that detects and analyzes unsent emotional messages in chat applications. It was developed as a final year engineering capstone project.

## Publication
- This project has been published in the International Journal of Scientific Research and Engineering Development (IJSREM). You can access the paper here:
[Chat Erasure Detection for Emotional Well-being](https://ijsrem.com/download/chat-erasure-detection-for-emotional-well-being/)

## Overview
- In the digital age, a lot of emotional expression happens in typed messages. Often, people type out messages reflecting emotional vulnerability or distress and then delete them. These "chat erasures" are important emotional cues that usually go unnoticed. This project introduces a system to capture these moments to provide timely support.

- The system works by monitoring keystrokes in chat applications (specifically WhatsApp in this implementation). When a significant amount of text is deleted, the system analyzes the erased text for its emotional content using a Natural Language Processing (NLP) model. If it detects emotions like sadness or depression, it securely sends an alert to a designated guardian or caregiver. This allows for a timely and compassionate response in sensitive situations.

## Features

- Real-time Chat Monitoring: Monitors chat applications for user input.
- Chat Erasure Detection: Identifies when a user erases a significant portion of a typed message.
- Emotional Analysis: Uses an NLP model to determine the emotional context of the erased text.
- Real-time Alerts: Sends an alert to a designated receiver if emotional distress is detected.
- Secure Data Transmission: Uses sockets for sending alerts from the user's machine to the receiver's.
- Guardian Interface: A simple GUI for a guardian or caregiver to view incoming alerts.
- Data Persistence: Received alerts are stored in a local SQLite database for future reference.

## How It Works
- The system has a client-server architecture:

- Client.py: This is the application that runs on the user's computer. It runs in the background, and when it detects that the user is on WhatsApp, it starts monitoring keystrokes. If it detects a chat erasure with a negative emotional context, it sends the erased text, the sender's username, and a timestamp to the server.

- Server.py: This application is for the guardian or caregiver. It's a GUI application that listens for incoming connections from the client. When it receives an alert, it displays the information in a window and saves it to a local database.

## Flow Diagram
<img width="302" alt="image" src="https://github.com/user-attachments/assets/0195020a-6505-4583-8d7e-08689ef8c7db" />

## Tech Stack

- Python: The core programming language for the project.
- PyQt5: For the graphical user interface of the receiver application.
- Hugging Face Transformers: For the NLP model used for emotion detection. The specific model is j-hartmann/emotion-english-distilroberta-base.
- Keyboard: For cross-platform keystroke monitoring.
- Pillow (PIL): For capturing screenshots.
- Pytesseract: For performing Optical Character Recognition (OCR) on screenshots to identify the username.
- Sockets: For real-time communication between the client and server.
- SQLite: For the local database to store received messages.
- win32gui: For interacting with the Windows GUI to get window titles and dimensions.

## Installation Steps
- Clone the repository
  `git clone https://github.com/your-username/your-repository-name.git
  cd your-repository-name`

- Install the dependencies:
`pip install -r requirements.txt`

## Usage
- Start the receiver application:
- Run the server.py file on the machine that will be receiving the alerts.
`python server.py`

- Start the client applicaton:
- Run the client.py file on the you want to monitor.
`python client.py`

- The script will run in the background and automatically start monitoring when it detects that WhatsApp is the active window.

## Future Improvements
- Cross-Platform Support: The current implementation uses win32gui, which is specific to Windows. This could be extended to work on macOS and Linux.

- Support for More Chat Apps: The current version is tailored for WhatsApp. It could be adapted to work with other messaging applications like Telegram, Discord, or Facebook Messenger.

- Enhanced NLP Model: A more sophisticated NLP model could be used for more nuanced emotional analysis.

- Data Encryption: The data sent between the client and server could be encrypted for enhanced privacy and security.

- Acknowledgement Mechanism: Implement an acknowledgment mechanism to ensure no data is lost if the receiver is offline.

- Local Caching: The sender can save messages locally if the receiver is offline and send them when the connection is re-established.

## Contribution: 
- Feel free to provide your contributions.
