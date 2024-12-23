import logging
from .ChangesSeguros import main  # Import your main function

def main(mytimer) -> None:
    logging.info("Timer function started.")
    try:
        # Call your main logic here
        main()
        logging.info("Function executed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")