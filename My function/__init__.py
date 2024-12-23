import logging
from .ChangesSeguros import main as process_changes  # Avoid naming conflict

def main(mytimer) -> None:
    logging.info("Timer function started.")
    try:
        # Call your main logic here
        process_changes()  # Use the renamed function
        logging.info("Function executed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
