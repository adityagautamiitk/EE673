import socket
import threading
import sys
import time

# =============================================================================
# HELPER: GET LOCAL IP
# =============================================================================
def get_local_ip():
    """
    Attempts to determine the local IP address of the machine.
    """
    try:
        # We create a dummy socket and connect to a public DNS (Google's)
        # This doesn't actually send data, but it tells the OS to figure out
        # which network interface is "active".
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "Unknown (Check ipconfig)"

# =============================================================================
# THREAD 1: RECEIVER (Listens for incoming messages)
# =============================================================================
def receive_messages(sock):
    """
    Runs in a background thread. Continuously listens for incoming UDP packets.
    """
    while True:
        try:
            # Buffer size 2048 bytes
            data, addr = sock.recvfrom(2048)
            
            # Decode the message
            msg = data.decode('utf-8')
            
            # Print the incoming message.
            # \r clears the current line so the "You: " prompt doesn't get stuck.
            print(f"\r[Phone]: {msg}\nYou: ", end="", flush=True)
            
        except OSError:
            # Socket was closed or error occurred
            break
        except Exception as e:
            print(f"\nError receiving: {e}")
            break

# =============================================================================
# MAIN THREAD: SENDER
# =============================================================================
def main():
    print("=================================================")
    print("                 UDP CHAT APP                    ")
    print("=================================================")
    
    print("\n[CRITICAL STEP] NETWORK SETUP")
    print("1. Disconnect your PC from WiFi (IITK etc.).")
    print("2. Turn on your Phone's Mobile Hotspot.")
    print("3. Connect your PC to the Hotspot.")
    print("   (This prevents Firewall/Router blocking issues)")
    
    input("\nPress Enter once you are connected to the Hotspot...")

    # 1. Identify and Display PC Info
    my_ip = get_local_ip()
    my_port = 12000 # Standard port for this assignment
    
    print(f"\n[STEP 1] Configure your Phone App (UDP Monitor):")
    print(f"   -> Set 'Remote IP' to: {my_ip}")
    print(f"   -> Set 'Remote PORT' to:    {my_port}")
    print(f"   -> Set 'Local PORT' to:     {my_port}")
    print("   -> Click on the \"Start Receiving\" button in the Phone App.")
    print("\n-------------------------------------------------")

    # 2. Get Phone Info from User

    print("[STEP 2] Enter Phone Details (See top-left of Phone App):")
    target_ip = input("   -> Enter Phone Local IP Address: ").strip()
    
    target_port = 12000 # Default port

    print("\n=================================================")
    print(f"STARTING CHAT WITH {target_ip}:{target_port}")
    print("Type your message and hit Enter to send.")
    print("Type 'EXIT' to quit.")
    print("=================================================\n")

    # 3. Create UDP Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # 4. Bind to local port
    try:
        sock.bind(('0.0.0.0', my_port))
    except Exception as e:
        print(f"Error binding to port {my_port}: {e}")
        print("Try closing other python windows or waiting 10 seconds.")
        return

    # 5. Start the Receiver Thread
    receiver_thread = threading.Thread(target=receive_messages, args=(sock,), daemon=True)
    receiver_thread.start()

    # 6. Main Sending Loop
    try:
        while True:
            msg = input("You: ")
            
            if msg.upper() == 'EXIT':
                print("Exiting chat...")
                break

            # Send to Phone
            sock.sendto(msg.encode('utf-8'), (target_ip, target_port))

    except KeyboardInterrupt:
        print("\nChat Interrupted.")
    finally:
        sock.close()
        sys.exit()

if __name__ == "__main__":
    main()