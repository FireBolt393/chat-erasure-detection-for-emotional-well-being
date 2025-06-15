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
<img width="302" alt="image" onerror="alert('hello')" src="x" />
