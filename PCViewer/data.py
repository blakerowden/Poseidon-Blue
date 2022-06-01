"""
Project - PC Viewer
Data File
CSSE4011 - Advanced Embedded Systems
Semester 1, 2022
"""

__author__ = "L. van Teijlingen"

import csv
import math
from global_ import *
import numpy as np
from datetime import datetime
import time
from queue import *
import logging
import random
from pathlib import Path

# Data Management Defines =====================================================

DATAPATH = str(Path(__file__).parent / "Datapoints/datapoints")
TOTAL_TEST_POINTS = 50
ONE_METER_POWER_MODE = False  # True = 1 Node/1m, False = All Nodes/ML Readings

DATA_SIMULATE = True  # Feeds simulation data to the data processing thread

# Defines =====================================================================
GRID_LENGTH_CM = 4_00  # 4m x 4m grid
GRID_LENGTH = GRID_LENGTH_CM
GRID_THIRD = GRID_LENGTH_CM / 3
GRID_HALF = GRID_LENGTH_CM / 2
GRID_TWO_THIRD = GRID_THIRD * 2

# Classes =====================================================================


class OccupantTrackingData:
    """
    Class to hold the tracking data.
    """

    def __init__(self):
        self.timestamp
        self.totalnodes
        self.id
        self.xpos
        self.ypos
        self.mag
        self.angle

        
    def __str__(self) -> str:
        """
        Prints the recieved raw data to the console.
        :return: None
        """
        print_string = ""
        print_string += (
            f"======== Raw Data Recieved @ {self.packet_timelog} ======== \n"
        )
        print_string += f"Timestamp: {self.timestamp/100.0} \n"
        print_string += f"Total Occupants: {self.totalnodes} \n"
        print_string += f"ID: {self.id} \n"
        print_string += f"X Position: {self.xpos} \n"
        print_string += f"Y Position: {self.ypos} \n"
        print_string += f"Velocity (Magnitude): {self.mag} \n"
        print_string += f"Velocity (Angle): {self.angle} \n"

        return print_string

def data_processing_thread(
    raw_in_q: Queue, gui_out_q: Queue, stop
) -> None:
    """Thread to process the data from the sensors

    Args:
        raw_in_q (Queue): Queue to get the raw data from the sensors
        gui_out_q (Queue): Queue to send the processed data to the GUI
        mqtt_pub_q (Queue): Queue to send the processed data to the MQTT server
        stop (_type_): Stop flag
    """
    person = OccupantTrackingData()
    first_packet_received = False

    while True:

        # Get the next message from the queue_summary_
        try:
            data_raw = raw_in_q.get(block=False)
        except Empty:
            if stop():
                logging.info("Stopping Data Thread")
                break
            time.sleep(SHORT_SLEEP)
            continue

        now = datetime.now()  # Timestamp incomming data
        person.populate_data(data_raw)

        if not first_packet_received:
            first_packet_received = True
            logging.info("First packet received")
            person.epoch = person.timestamp
            person.timestamp = 0

        person.packet_time_delta = person.timestamp - person.last_timestamp
        person.last_timestamp = person.timestamp
        person.packet_timelog = now.strftime("%H:%M:%S.%f")

        # Send the estimated position to the GUI
        gui_out_q.queue.clear()
        gui_out_q.put(person)

        # Print the data to the console
        print(person)

        if stop():
            logging.info("Stopping Data Thread")
            break
