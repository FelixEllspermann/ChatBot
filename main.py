import tkinter as tk
from tkinter import scrolledtext
import requests
from threading import Thread

def send_message_to_api(message):
	url = "https://chatgpt-42.p.rapidapi.com/conversationgpt4"
	payload = {
		"messages": [
			{
				"role": "user",
				"content": message
			}
		],
		"system_prompt": "",
		"temperature": 0.9,
		"top_k": 5,
		"top_p": 0.9,
		"max_tokens": 256,
		"web_access": False
	}
	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": "Your API Toke",
		"X-RapidAPI-Host": "chatgpt-42.p.rapidapi.com"
	}

	response = requests.post(url, json=payload, headers=headers)
	response_data = response.json()
	if "result" in response_data:
		return response_data["result"]
	else:
		return "Keine Antwort gefunden oder falsche Antwortstruktur."


def send():
	user_input = entry.get()
	if user_input:
		response_thread = Thread(target=update_response, args=(user_input,))
		response_thread.start()
		entry.delete(0, tk.END)


def update_response(message):
	response_text = send_message_to_api(message)
	response_area.config(state=tk.NORMAL)
	response_area.insert(tk.END, "Du: " + message + "\n")
	response_area.insert(tk.END, "API-Antwort: " + response_text + "\n\n")
	response_area.config(state=tk.DISABLED)
	response_area.see(tk.END)


root = tk.Tk()
root.title("Chat mit API")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

entry = tk.Entry(frame, width=50)
entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
entry.bind("<Return>", lambda event: send())

send_button = tk.Button(frame, text="Senden", command=send)
send_button.pack(side=tk.RIGHT)

response_area = scrolledtext.ScrolledText(root, state='disabled', height=15, width=50)
response_area.pack(padx=10, pady=10)

root.mainloop()