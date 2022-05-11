"""
CSSE4011 - Advanced Embedded Systems
Semester 1, 2022
"""

__author__ = "B.Rowden, B.O'Neill and L.Van Teijlingen"

import time
from threading import Thread
from queue import *
import logging
from serial_interface import serial_interface_thread
from global_ import *


def main() -> None:
    """
    Main function for the application.
    """
    # Set logging level
    logging.basicConfig(level=logging.INFO)
    # Create a stop flag
    stop_flag = False

    serial_active = True
    thread_serial = None

    j_data = Queue()  # Queue for Raw JSON data
    
    if serial_active:
        # Create thread to read from the serial port
        logging.debug("Starting Serial Thread")
        thread_serial = Thread(
            target=serial_interface_thread, args=(j_data, lambda: stop_flag)
        )
        thread_serial.start()

    if serial_active:
        thread_serial.join()
        logging.info("Serial Thread Closed")

    logging.info("program complete")


if __name__ == "__main__":
    """
    Only run the main function if this file is run directly.
    """
    main()