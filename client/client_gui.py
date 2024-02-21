import tkinter as tk


def login_gui(client, login: callable):
	# This function will create a login window.
	# Create a new window with the title "Login" and the dimensions 300x100 and make it non-resizable.
	window = tk.Tk()
	window.title("Login")
	window.geometry("300x100")
	window.resizable(False, False)

	# Create a label with the text "Enter your username:" and pack it into the window.
	label = tk.Label(window, text="Enter your username:")
	label.pack()

	# Create an entry widget for the username and pack it into the window.
	username = tk.Entry(window)
	username.pack()

	# Create a label for error messages and pack it into the window, but do not display it.
	error_label = tk.Label(window, text="")

	# Create a button with the text "Login" and the command to call the login function with the username, error label,
	# window, and client as arguments. Then pack the button into the window.
	login_button = tk.Button(window, text="Login", command=lambda: login(username, error_label, window, client))
	login_button.pack()
	error_label.pack()

	# Bind the Enter key to the login function with the username, error label, window, and client as arguments.
	window.bind('<Return>', lambda event: login(username, error_label, window, client))

	window.mainloop()


def chat_gui(client, send: callable):
	# This function will create a chat window.
	# Create a new window with the title "Chat" and the dimensions 600x750 and make it non-resizable.
	window = tk.Tk()
	window.geometry("600x750")
	window.title("Chat")
	window.configure(bg="#FFFFFF")

	# Create a canvas with the dimensions 600x750 and pack it into the window.
	canvas = tk.Canvas(
		window,
		bg="#FFFFFF",
		height=750,
		width=600,
		bd=0,
		highlightthickness=0,
		relief="ridge"
	)
	canvas.place(x=0, y=0)

	# Create 28 chat boxes and pack them into the window.
	# The chat boxes are used to display the chat log.
	# The chat boxes are disabled to prevent the user from editing the chat log.
	# The chat boxes are packed into the window in a vertical stack.
	# Each of the chat boxes will hold one line of the chat log.
	chat_boxes = []
	for x in range(0, 28):
		chat_boxes.append(tk.Entry(
			bd=0,
			bg="#000000",
			disabledbackground="#000000",
			fg="#FFFFFF",
			disabledforeground="#FFFFFF",
			highlightthickness=0,
		))
		chat_boxes[x].place(
			x=0.0,
			y=x * 25.0,
			width=600.0,
			height=25.0
		)

	# Create an entry widget for the user to input messages and pack it into the window.
	message_box = tk.Entry(
		bd=0,
		bg="#D9D9D9",
		fg="#000716",
		highlightthickness=0
	)
	message_box.place(
		x=0.0,
		y=700.0,
		width=550.0,
		height=48.0
	)

	# Create a button with the text "Send" and the command to call the send function with the client, message, and
	# message box as arguments. Then pack the button into the window.
	send_button = tk.Button(
		text="Send",
		borderwidth=0,
		highlightthickness=0,
		command=lambda: send(client, message_box.get(), message_box),
		relief="flat"
	)
	send_button.place(
		x=550.0,
		y=700.0,
		width=50.0,
		height=50.0
	)

	# Bind the Enter key to the send function with the client, message, and message box as arguments.
	window.bind('<Return>', lambda event: send(client, message_box.get(), message_box))

	# Return the window and chat boxes.
	return window, chat_boxes
