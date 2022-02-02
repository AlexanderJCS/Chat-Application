import socket
import sys
import errno
import threading
import tkinter as tk

root = tk.Tk()
canvas1 = tk.Canvas(root, width=1080, height=720)
canvas1.pack()

entry1 = tk.Entry(root)
canvas1.create_window(475, 650, window=entry1, height=30, width=900)

output = tk.Text(root, height=30, width=125, bg="light cyan")

output.place(x=540, y=100, anchor='n')

button1 = tk.Button(text='Send', command=lambda: send())
canvas1.create_window(1000, 650, window=button1, width=100, height=30)

output.insert("end", "Please input information in the other window before continuing.\n")
output.config(state="disabled")

HEADER_LENGTH = 10

IP = input("IP: ")
PORT = int(input("Port: "))
my_username = input("Username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP, PORT))

client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

print("Successfully logged in! Please check the other window.")
output.config(state="normal")
output.insert("end", f"Connnected to server: {IP}:{PORT}\n")


def send():
    message = entry1.get()
    entry1.delete(0, "end")

    if message:

        # Send message
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)


def recieve():

    while True:
        try:
            while True:
                # Recieve message

                username_header = client_socket.recv(HEADER_LENGTH)

                if not len(username_header):
                    print('Connection closed by the server')
                    sys.exit()

                username_length = int(username_header.decode('utf-8').strip())
                username = client_socket.recv(username_length).decode('utf-8')

                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_length).decode('utf-8')

                output.insert("end", f'{username} > {message}\n')

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()

            continue

        except Exception as e:
            print('Reading error: '.format(str(e)))
            sys.exit()


t = threading.Thread(target=recieve)

t.start()

root.mainloop()
