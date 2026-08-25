=============================================================================
EE673A: Digital Communication Networks - Assignment 1
Student Name: Aditya Gautam
Roll Number:  220064
Date:         February 8, 2026
=============================================================================

-----------------------------------------------------------------------------
1. OVERVIEW & REQUIREMENTS
-----------------------------------------------------------------------------
This submission contains Python implementations for three network programming 
tasks. The code is organized into three folders:

- Q1: TCP and UDP Client-Server implementations (Echo Service).
- Q2: UDP Peer-to-Peer Chat Application (using Threading).
- Q3: SMTP Mail Client (Interactive, supports SSL/TLS & Attachments).

SYSTEM REQUIREMENTS:
- Python 3.x installed.
- Standard Python Libraries only (socket, threading, ssl, email, sys, os).
- No external 'pip install' is required.

-----------------------------------------------------------------------------
2. HOW TO RUN AND TEST
-----------------------------------------------------------------------------

--- QUESTION 1: Basics of Socket Programming ---
Location: /Q1/

Part A: TCP Implementation (Connection-Oriented)
1. Open a terminal and navigate to the Q1 folder.
2. Start the Server:
   $ python tcp_server.py
   (Output: "TCP Server is ready to receive...")
3. Open a SECOND terminal and start the Client:
   $ python tcp_client.py
4. Enter a sentence when prompted. The server will capitalize it and return it.

Part B: UDP Implementation (Connectionless)
1. Start the Server:
   $ python udp_server.py
   (Output: "UDP Server is up and listening...")
2. Open a SECOND terminal and start the Client:
   $ python udp_client.py
3. Enter a sentence. The server receives the packet, processes it, and 
   sends it back to the client's specific address.

--- QUESTION 2: UDP Chat Application ---
Location: /Q2/
File: q2_chat.py

** CRITICAL NETWORK SETUP **
To ensure the PC and Phone can communicate without Firewall or IITK 
Router blocking, please use a Mobile Hotspot:
1. Disconnect PC from WiFi.
2. Turn on Mobile Hotspot on your Android phone.
3. Connect PC to the Hotspot.

Steps to Run:
1. Open the "UDP Monitor" app on your Android phone.
2. Run the script on your PC:
   $ python q2_chat.py
3. Follow the on-screen prompts:
   - The script will display your PC's IP. Enter this in the Phone App 
     under "Remote Address", along with the PORT numbers.
   - Enter the Phone's IP (displayed in the App) into the Python console.
   - Click on the "Start Receiving" button in the Phone App.
4. Chatting:
   - Type a message on PC -> Appears on Phone.
   - Type a message on Phone -> Appears on PC.

--- QUESTION 3: Mail Client ---
Location: /Q3/
File: mail_client.py

Description:
This client establishes a raw TCP connection with an SMTP server. It handles 
handshakes (EHLO), Encryption (SSL/TLS), Authentication (AUTH LOGIN), and 
MIME formatting for attachments.

Steps to Run:
1. Ensure 'test_attachment.txt' exists in the folder (included).
2. Run the script:
   $ python mail_client.py
3. Login Configuration:
   - Server: Press Enter to use default 'mmtp.iitk.ac.in' (or type another).
   - Port: Press Enter to use default '465' (Implicit SSL).
   - Enter your Email Address and Password (input is hidden for security).
4. Composing Mail:
   - Select Option 1.
   - Enter To/Cc/Subject.
   - BODY: Type your message. To finish, press Enter, type a single dot '.',
     and press Enter again.
   - ATTACHMENT: Type 'test_attachment.txt' (or leave blank).
5. Verification:
   - The script will display "Mail Sent Successfully!".
   - Check the recipient's inbox.
