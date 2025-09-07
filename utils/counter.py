import json
import os

COUNTER_FILE = "ticket_counter.json"

def get_ticket_number():
    try:
        if os.path.exists(COUNTER_FILE):
            with open(COUNTER_FILE, "r") as f:
                data = json.load(f)
                ticket_number = data.get("ticket_number", 0) + 1
        else:
            ticket_number = 1

        with open(COUNTER_FILE, "w") as f:
            json.dump({"ticket_number": ticket_number}, f)
        
        print(f"Generated ticket number: {ticket_number}")
        return ticket_number
    except Exception as e:
        print(f"Error in get_ticket_number: {e}")
        raise ValueError(f"Cannot generate ticket number: {e}")
