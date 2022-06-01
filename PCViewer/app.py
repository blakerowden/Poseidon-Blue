"""
Project - PC Viewer
Main File
CSSE4011 - Advanced Embedded Systems
Semester 1, 2022
"""

__author__ = "L. van Teijlingen"

import time
from threading import Thread
from queue import *
import logging
from data import *
from gui import *
from global_ import *


def main() -> None:
    """
    Main function for the application.
    """
    # Set logging level
    logging.basicConfig(level=logging.INFO)
    # Create a stop flag
    stop_flag = False
    data_active = False
    gui_active = True

    thread_data = None
    thread_gui = None

    j_data = Queue()  # Queue for Raw JSON data
    k_data = Queue()  # Queue for (k)lean data


    if data_active:
        # Create thread to process the data
        logging.debug("Starting Data Thread")
        thread_data = Thread(
            target=data_processing_thread,
            args=(j_data, k_data, lambda: stop_flag),
        )
        thread_data.start()

    if gui_active:
        # Create thread to run the GUI
        logging.debug("Starting GUI Thread")
        thread_gui = Thread(target=gui_thread, args=(k_data,))
        thread_gui.start()

    while not stop_flag:
        if (
            (gui_active and not thread_gui.is_alive())
            or (data_active and not thread_data.is_alive())
        ):
            logging.warning("One of the threads has stopped. Stopping the program...")
            stop_flag = True

        time.sleep(SHORT_SLEEP)

    if gui_active:
        thread_gui.join()
        logging.info("GUI Thread Closed")

    if data_active:
        thread_data.join()
        logging.info("Data Thread Closed")

    logging.info("program complete")


if __name__ == "__main__":
    """
    Only run the main function if this file is run directly.
    """
    main()
