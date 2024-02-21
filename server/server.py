import datetime
import json
import socket
import threading

HOST = '127.0.0.1'
PORT = 413

# The maximum number of queued connections
LISTENER_LIMIT = 5

active_clients = []


def send_message_to_all(message):
	# This function will send a message to all clients
	for client in active_clients:
		client[1].send(message.encode('utf-8'))


def send_message_to_client(client, message):
	# This function will send a message to a specific client
	client.sendall(message.encode('utf-8'))


def listen_for_messages(client, username):
	# This function will listen for messages from the client
	while True:
		# Try to receive a message from the client and decode it from bytes to a string.
		# If the client has disconnected, print a message and remove the client from the list of active clients.
		try:
			message = client.recv(2048).decode('utf-8')
		except ConnectionResetError:
			print(f"Client <{username}> has disconnected")
			active_clients.remove((username, client))
			send_message_to_all(json.dumps({
				"username": "SERVER",
				"message": f"{username} has left the chat!",
				"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			}))
			break

		# If the message is not empty, create a JSON object with the username, message, and timestamp,
		# and write the JSON object to the chatlog file. Then send the JSON object to all clients.
		# If the message is empty, print a message.
		if message != '':
			final = json.dumps({
				"username": username,
				"message": message,
				"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			})
			f = open("./chatlog.txt", "a")
			f.write(f"{final}\n")
			f.close()
			send_message_to_all(final)
		else:
			print(f"Empty message from client {username}")


def handle_client(client):
	# This function will handle the client connection
	while True:
		username = client.recv(1024).decode('utf-8')

		# If the client has sent a username, add the client to the list of active clients
		# and send a message to all clients. If the client has not sent a username, terminate the connection.
		if username is not None and username.strip() != '':
			active_clients.append((username, client))
			send_message_to_all(json.dumps({
				"username": "SERVER",
				"message": f"{username} has joined the chat!",
				"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			}))
			break
		else:
			print(f"Connection from [UNNAMED CLIENT] has been terminated.")
			return

	# Start a new thread to listen for messages from the client
	threading.Thread(target=listen_for_messages, args=(client, username)).start()


def main():
	# Create a socket object
	# AF_INET is the address family for IPv4
	# SOCK_STREAM is the socket type for TCP
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the socket to the host and port.
	# In the case of an error, print a message and exit the program.
	try:
		server.bind((HOST, PORT))
	except socket.error:
		print(f"Unable to bind to host {HOST}:{PORT}")
	print(f"Server listening on {HOST}:{PORT}")

	# Listen for incoming connections
	# The argument is the maximum number of queued connections
	server.listen(LISTENER_LIMIT)

	while True:
		# Accept a connection
		# Returns a new socket object and the address of the client
		client, address = server.accept()
		print(f"Connection from {address[0]}:{address[1]} has been established!")

		# Create a new thread to handle the client
		threading.Thread(target=handle_client, args=(client,)).start()


if __name__ == '__main__':
	main()
