import json
import socket
import threading
import tkinter as tk

from client_gui import login_gui, chat_gui

HOST = '127.0.0.1'
PORT = 413


def send_to_server(client, message, chat_box: tk.Entry = None):
	# This function will send a message to the server.
	# Try to send the message to the server. If the server has disconnected, print a message and return.
	try:
		client.send(message.encode('utf-8'))
	except (ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError, ConnectionError):
		print(f"Server has disconnected")
		return
	if chat_box is not None:
		chat_box.delete(0, tk.END)


def listen_for_messages(client, chatbox: list[tk.Entry]):
	# This function will listen for messages from the client.
	while True:
		# Try to receive a message from the server and decode it from bytes to a string.
		# If the server has disconnected, print a message and break out of the loop.
		try:
			message = client.recv(2048).decode('utf-8')
		except (ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError, ConnectionError):
			print(f"Disconnected")
			break
		if message != '':
			message = json.loads(message)

			# Shift the chatbox entries up by one. Enabling and disabling the chatbox entries is necessary to allow
			# the entries to be modified.
			# The first entry is discarded, and the last entry is updated with the new message.
			for x in range(0, len(chatbox) - 1):
				chatbox[x].configure(state=tk.NORMAL)
				chatbox[x].delete(0, tk.END)
				chatbox[x].insert(0, chatbox[x + 1].get())
				chatbox[x].configure(state=tk.DISABLED)
			chatbox[len(chatbox) - 1].configure(state=tk.NORMAL)
			chatbox[len(chatbox) - 1].delete(0, tk.END)

			# If the message is from the server, display the message without the username and timestamp,
			# otherwise display the message with the username and timestamp.
			if message["username"] == 'SERVER':
				chatbox[len(chatbox) - 1].insert(0, f"{message['message']}")
			else:
				chatbox[len(chatbox) - 1].insert(0, f"[{message['timestamp']}] <{message['username']}>: "
													f"{message['message']}")
			chatbox[len(chatbox) - 1].configure(state=tk.DISABLED)
		else:
			print("Empty message from server")
			break


def login(text_input: tk.Entry, error_label: tk.Label, window: tk, client):
	username = text_input.get().strip()
	# If the username is not empty, send the username to the server and close the login window.
	# Else, display an error message.
	if username != '':
		# Send the username to the server and close the login window.
		# In case the server has disconnected, print a message and close the window.
		try:
			client.send(username.encode('utf-8'))
		except (ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError, ConnectionError):
			print(f"Server has disconnected")
			window.destroy()
			return
		window.destroy()
	else:
		error_label.config(text="Username cannot be empty.")


def main():
	# Create a socket object.
	# AF_INET is the address family for IPv4.
	# SOCK_STREAM is the socket type for TCP.
	try:
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except ConnectionRefusedError:
		print("Server is not running. Please start the server and try again.")
		# Return 1 to indicate an error.
		return 1

	# Connect to the server.
	try:
		client.connect((HOST, PORT))
	except ConnectionRefusedError:
		print("Unable to connect to the server. Please try again later.")
		# Return 1 to indicate an error.
		return 1

	login_gui(client, login)

	try:
		client.send("".encode('utf-8'))
	except (ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError, ConnectionError):
		# If the server has disconnected, close the client connection.
		client.close()
		# Return 1 to indicate an error.
		return 1

	window, chat_boxes = chat_gui(client, send_to_server)

	# Start a new thread to listen for messages from the server.
	thread = threading.Thread(target=listen_for_messages, args=(client, chat_boxes))
	thread.start()

	# Run the chat GUI.
	window.mainloop()

	# Close the client connection.
	client.close()

	# Wait for the thread to finish.
	thread.join()

	# Return 0 to indicate successful execution.
	return 0


if __name__ == '__main__':
	main()
