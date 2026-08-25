import socket
import ssl
import base64
import getpass
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class InteractiveSMTPClient:
    def __init__(self):
        self.sock = None
        self.server = ""
        self.port = 0
        self.email_address = ""
        self.is_connected = False

    def connect_and_login(self):
        print("\n--- SMTP LOGIN SETUP ---")
        default_server = "mmtp.iitk.ac.in"
        default_port = "465" # Port 465 is for Implicit SSL
        print("\nWe will ask for your Email Server and Port. If you are using mmtp.iitk.ac.in, just press Enter to skip typing them and use the default values for both of them. \n")
        self.server = input(f"SMTP Server [default: {default_server}]: ").strip() or default_server
        port_str = input(f"SMTP Port [default: {default_port}]: ").strip() or default_port
        self.port = int(port_str)
        print("\nNow, enter your email address and password. The password will not be displayed as you type for security reasons.\n")
        self.email_address = input("Your Email Address: ").strip()
        password = getpass.getpass("Your Password: ")

        try:
            print(f"\nConnecting to {self.server}:{self.port}...")

            # LOGIC SPLIT: Port 465 (Implicit SSL) vs 587/25 (STARTTLS)
            if self.port == 465:
                # OPTION A: Implicit SSL (Connect directly with SSL wrapper)
                # This is what mmtp.iitk.ac.in uses
                raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                raw_socket.settimeout(20)
                
                context = ssl.create_default_context()
                self.sock = context.wrap_socket(raw_socket, server_hostname=self.server)
                self.sock.connect((self.server, self.port))
                
                # Receive initial greeting (encrypted from start)
                self._recv_response()
                
                # Handshake
                self._send_command(f'EHLO {self.email_address}')
                
            else:
                # OPTION B: STARTTLS (Connect plain -> Upgrade)
                # Used for ports 587 or 25
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(20)
                self.sock.connect((self.server, self.port))
                self._recv_response() # Greeting
                
                self._send_command(f'EHLO {self.email_address}')
                self._send_command('STARTTLS')
                
                context = ssl.create_default_context()
                self.sock = context.wrap_socket(self.sock, server_hostname=self.server)
                self._send_command(f'EHLO {self.email_address}') # Resend EHLO

            print("Successfully connected securely.")

            # AUTHENTICATION
            print("Authenticating...")
            username_b64 = base64.b64encode(self.email_address.encode()).decode()
            password_b64 = base64.b64encode(password.encode()).decode()

            self._send_command('AUTH LOGIN')
            self._send_command(username_b64)
            response = self._send_command(password_b64, silent=True)

            if "235" in response or "2.7.0" in response:
                print("\nLogin Successful!")
                self.is_connected = True
                return True
            else:
                print(f"\nLogin Failed. Server said: {response}")
                self.sock.close()
                return False

        except Exception as e:
            print(f"\nConnection Error: {e}")
            return False

    def compose_mail(self):
        if not self.is_connected:
            print("Error: You are not connected.")
            return

        print("\n--- COMPOSE NEW MAIL ---")
        to_addr = input("To (separate multiple with commas): ").strip()
        cc_addr = input("Cc: ").strip()
        bcc_addr = input("Bcc: ").strip()
        subject = input("Subject: ").strip()

        print("Body (To Finish typing the body, Type '.' on a new empty line and press Enter):")
        body_lines = []
        while True:
            line = input()
            if line == '.':
                break
            body_lines.append(line)
        body = "\n".join(body_lines)

        attachment_path = input("Attachment Filename (leave blank for none): ").strip()

        # Build MIME Message
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = to_addr
        if cc_addr: msg['Cc'] = cc_addr
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Handle Attachment
        if attachment_path:
            if os.path.exists(attachment_path):
                try:
                    with open(attachment_path, "rb") as f:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header("Content-Disposition", f"attachment; filename={attachment_path}")
                        msg.attach(part)
                    print(f"Attached: {attachment_path}")
                except Exception as e:
                    print(f"Could not attach file: {e}")
            else:
                print(f"Warning: File '{attachment_path}' not found. Sending without attachment.")

        # Send Logic
        try:
            self._send_command(f'MAIL FROM: <{self.email_address}>')

            # Aggregate recipients for RCPT TO command
            all_recipients = []
            if to_addr: all_recipients.extend(to_addr.split(','))
            if cc_addr: all_recipients.extend(cc_addr.split(','))
            if bcc_addr: all_recipients.extend(bcc_addr.split(','))

            for recipient in all_recipients:
                recipient = recipient.strip()
                if recipient:
                    self._send_command(f'RCPT TO: <{recipient}>')

            self._send_command('DATA')
            
            print("Sending data...")
            self.sock.sendall(msg.as_string().encode())
            self._send_command('\r\n.') # End of Data
            print("\n>>> Mail Sent Successfully! <<<")

        except Exception as e:
            print(f"Failed to send email: {e}")
            self.is_connected = False

    def logout(self):
        if self.sock:
            try:
                self._send_command('QUIT')
                self.sock.close()
            except:
                pass
        self.is_connected = False
        print("Logged out. Goodbye.")

    def _send_command(self, cmd, silent=False):
        if not self.sock: return ""
        cmd_str = cmd + '\r\n'
        self.sock.send(cmd_str.encode())
        return self._recv_response(silent_cmd=silent)

    def _recv_response(self, silent_cmd=False):
        if not self.sock: return ""
        try:
            response = self.sock.recv(4096).decode()
            # print(f"DEBUG S: {response.strip()}") # Uncomment to debug
            return response
        except socket.timeout:
            print("Server timed out.")
            return ""

def main():
    client = InteractiveSMTPClient()
    if not client.connect_and_login():
        return

    while True:
        print("\n--- MENU ---")
        print("1. Compose New Mail")
        print("2. Logout")
        
        choice = input("Select Option Number: ").strip()
        
        if choice == '1':
            client.compose_mail()
        elif choice == '2':
            client.logout()
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted.")