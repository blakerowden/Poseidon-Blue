from tkinter import ON
import serial
import time
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import os
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import Point
from dataclasses import dataclass

from sklearn import cluster
from grouper import *
from velocity import *

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "AWR1843config.cfg")

INFLUXDB_TOKEN = "oG8va_7annhvLMe3uSkHTE3pUrxhYO5tGUUUyCOmBqkhX_Lu0ySBA_aDR-pQa2dpkiCBiDk0AX29VgQAHLBlVA=="

# Change the configuration file name
configFileName = filename

CLIport = {}
Dataport = {}
byteBuffer = np.zeros(2**15, dtype="uint8")
byteBufferLength = 0

configParameters = (
    {}
)  # Initialize an empty dictionary to store the configuration parameters

centreX = []
centreY = []
xPoints = []
yPoints = []
velList = []
angList = []
timeStamps = []
iteration = 0
last_num = 1


@dataclass
class DetectedObject:
    """
    Holds all the information about a detected object
    """

    uid: int = 0
    x: float = 0
    y: float = 0
    v: float = 0
    angle: float = 0


class OnlineDashboard:
    """
    Class to hold the data and functions related to dashboard publishing
    """

    def __init__(self):
        self._token = INFLUXDB_TOKEN
        self._org = "lianavant@gmail.com"
        self._url = "https://ap-southeast-2-1.aws.cloud2.influxdata.com"
        self._bucket = "People"
        self._client = influxdb_client.InfluxDBClient(
            url=self._url, token=self._token, org=self._org
        )
        self._write_api = self._client.write_api(write_options=SYNCHRONOUS)
        self.total_nodes = 0
        self.objects = []

    def add_object(self, x: float, y: float, v: float, angle: float) -> None:
        """
        Add an object to the dashboard
        """
        self.total_nodes += 1
        self.objects.append(DetectedObject(self.total_nodes, x, y, v, angle))

    def clear_objects(self) -> None:
        """
        Clear all objects from the dashboard
        """
        self.total_nodes = 0
        self.objects.clear()

    def send_data(self) -> None:
        """
        Send the data to the online dashboard
        """

        # Send data for each identified object
        for index, person in enumerate(self.objects):
            print(f"Sending person {index} to dashboard")
            self._write_api.write(
                bucket=self._bucket,
                record=person,
                record_measurement_key="uid",
                record_field_keys=["x", "y", "v", "angle"],
            )

        # Senf the total number of people to the dashboard
        total_occ = influxdb_client.Point("room_occupancy").field(
            "current_occupancy", self.total_nodes
        )
        print(f"Sending occupancy of {total_occ} to dashboard")
        self._write_api.write(bucket=self._bucket, record=total_occ)


def serialConfig(configFileName: str) -> tuple:
    """
    Function to configure the serial ports and send the data from
    the configuration file to the radar

    Args:
        configFileName (str): Filenae of the configuration file

    Returns:
        tuple: Tuple containing the CLI and data serial ports
    """

    global CLIport
    global Dataport
    # Open the serial ports for the configuration and the data ports

    # Linux
    CLIport = serial.Serial("/dev/ttyACM0", 115200)
    Dataport = serial.Serial("/dev/ttyACM1", 921600)

    # Windows
    # CLIport = serial.Serial('COM8', 115200)
    # Dataport = serial.Serial('COM9', 921600)

    # Read the configuration file and send it to the board
    config = [line.rstrip("\r\n") for line in open(configFileName)]
    for i in config:
        CLIport.write((i + "\n").encode())
        print(i)
        time.sleep(0.01)

    return CLIport, Dataport


def parseConfigFile(configFileName: str) -> dict:
    """Function to parse the data inside the configuration file

    Args:
        configFileName (str): Filename of the configuration file

    Returns:
        dict: Dictionary containing the configuration parameters
    """

    # Read the configuration file and send it to the board
    config = [line.rstrip("\r\n") for line in open(configFileName)]
    for i in config:

        # Split the line
        splitWords = i.split(" ")

        # Hard code the number of antennas
        numRxAnt = 4
        numTxAnt = 3

        # Get the information about the profile configuration
        if "profileCfg" in splitWords[0]:
            startFreq = int(float(splitWords[2]))
            idleTime = int(splitWords[3])
            rampEndTime = float(splitWords[5])
            freqSlopeConst = float(splitWords[8])
            numAdcSamples = int(splitWords[10])
            numAdcSamplesRoundTo2 = 1

            while numAdcSamples > numAdcSamplesRoundTo2:
                numAdcSamplesRoundTo2 = numAdcSamplesRoundTo2 * 2

            digOutSampleRate = int(splitWords[11])

        # Get the information about the frame configuration
        elif "frameCfg" in splitWords[0]:

            chirpStartIdx = int(splitWords[1])
            chirpEndIdx = int(splitWords[2])
            numLoops = int(splitWords[3])
            numFrames = int(splitWords[4])
            framePeriodicity = float(splitWords[5])

    # Combine the read data to obtain the configuration parameters
    numChirpsPerFrame = (chirpEndIdx - chirpStartIdx + 1) * numLoops
    configParameters["numDopplerBins"] = numChirpsPerFrame / numTxAnt
    configParameters["numRangeBins"] = numAdcSamplesRoundTo2
    configParameters["rangeResolutionMeters"] = (3e8 * digOutSampleRate * 1e3) / (
        2 * freqSlopeConst * 1e12 * numAdcSamples
    )
    configParameters["rangeIdxToMeters"] = (3e8 * digOutSampleRate * 1e3) / (
        2 * freqSlopeConst * 1e12 * configParameters["numRangeBins"]
    )
    configParameters["dopplerResolutionMps"] = 3e8 / (
        2
        * startFreq
        * 1e9
        * (idleTime + rampEndTime)
        * 1e-6
        * configParameters["numDopplerBins"]
        * numTxAnt
    )
    configParameters["maxRange"] = (300 * 0.9 * digOutSampleRate) / (
        2 * freqSlopeConst * 1e3
    )
    configParameters["maxVelocity"] = 3e8 / (
        4 * startFreq * 1e9 * (idleTime + rampEndTime) * 1e-6 * numTxAnt
    )

    return configParameters


def readAndParseData18xx(Dataport: int, configParameters: dict) -> tuple:
    """Funtion to read and parse the incoming data

    Args:
        Dataport (int): Serial port to read the data from
        configParameters (dict): Dictionary containing the conf parameters

    Returns:
        tuple: Tuple containing the data
    """
    global byteBuffer, byteBufferLength

    # Constants
    OBJ_STRUCT_SIZE_BYTES = 12
    BYTE_VEC_ACC_MAX_SIZE = 2**15
    MMWDEMO_UART_MSG_DETECTED_POINTS = 1
    MMWDEMO_UART_MSG_RANGE_PROFILE = 2
    maxBufferSize = 2**15
    tlvHeaderLengthInBytes = 8
    pointLengthInBytes = 16
    magicWord = [2, 1, 4, 3, 6, 5, 8, 7]

    # Initialize variables
    magicOK = 0  # Checks if magic number has been read
    dataOK = 0  # Checks if the data has been read correctly
    frameNumber = 0
    detObj = {}

    readBuffer = Dataport.read(Dataport.in_waiting)
    byteVec = np.frombuffer(readBuffer, dtype="uint8")
    byteCount = len(byteVec)

    # Check that the buffer is not full, and then add the data to the buffer
    if (byteBufferLength + byteCount) < maxBufferSize:
        byteBuffer[byteBufferLength : byteBufferLength + byteCount] = byteVec[
            :byteCount
        ]
        byteBufferLength = byteBufferLength + byteCount

    # Check that the buffer has some data
    if byteBufferLength > 16:

        # Check for all possible locations of the magic word
        possibleLocs = np.where(byteBuffer == magicWord[0])[0]

        # Confirm that is the beginning of the magic word and store the index in startIdx
        startIdx = []
        for loc in possibleLocs:
            check = byteBuffer[loc : loc + 8]
            if np.all(check == magicWord):
                startIdx.append(loc)

        # Check that startIdx is not empty
        if startIdx:

            # Remove the data before the first start index
            if startIdx[0] > 0 and startIdx[0] < byteBufferLength:
                byteBuffer[: byteBufferLength - startIdx[0]] = byteBuffer[
                    startIdx[0] : byteBufferLength
                ]
                byteBuffer[byteBufferLength - startIdx[0] :] = np.zeros(
                    len(byteBuffer[byteBufferLength - startIdx[0] :]),
                    dtype="uint8",
                )
                byteBufferLength = byteBufferLength - startIdx[0]

            # Check that there have no errors with the byte buffer length
            if byteBufferLength < 0:
                byteBufferLength = 0

            # word array to convert 4 bytes to a 32 bit number
            word = [1, 2**8, 2**16, 2**24]

            # Read the total packet length
            totalPacketLen = np.matmul(byteBuffer[12 : 12 + 4], word)

            # Check that all the packet has been read
            if (byteBufferLength >= totalPacketLen) and (byteBufferLength != 0):
                magicOK = 1

    # If magicOK is equal to 1 then process the message
    if magicOK:
        # word array to convert 4 bytes to a 32 bit number
        word = [1, 2**8, 2**16, 2**24]

        # Initialize the pointer index
        idX = 0

        # Read the header
        magicNumber = byteBuffer[idX : idX + 8]
        idX += 8
        version = format(np.matmul(byteBuffer[idX : idX + 4], word), "x")
        idX += 4
        totalPacketLen = np.matmul(byteBuffer[idX : idX + 4], word)
        idX += 4
        platform = format(np.matmul(byteBuffer[idX : idX + 4], word), "x")
        idX += 4
        frameNumber = np.matmul(byteBuffer[idX : idX + 4], word)
        idX += 4
        timeCpuCycles = np.matmul(byteBuffer[idX : idX + 4], word)
        idX += 4
        numDetectedObj = np.matmul(byteBuffer[idX : idX + 4], word)
        idX += 4
        numTLVs = np.matmul(byteBuffer[idX : idX + 4], word)
        idX += 4
        subFrameNumber = np.matmul(byteBuffer[idX : idX + 4], word)
        idX += 4

        # Read the TLV messages
        for tlvIdx in range(numTLVs):

            # word array to convert 4 bytes to a 32 bit number
            word = [1, 2**8, 2**16, 2**24]

            # Check the header of the TLV message
            try:
                tlv_type = np.matmul(byteBuffer[idX : idX + 4], word)
                idX += 4
                tlv_length = np.matmul(byteBuffer[idX : idX + 4], word)
                idX += 4
            except ValueError:
                print("Error reading TLV header, restarting...")
                time.sleep(0.1)
                main()

            # Read the data depending on the TLV message
            if tlv_type == MMWDEMO_UART_MSG_DETECTED_POINTS:

                # Initialize the arrays
                x = np.zeros(numDetectedObj, dtype=np.float32)
                y = np.zeros(numDetectedObj, dtype=np.float32)
                z = np.zeros(numDetectedObj, dtype=np.float32)
                velocity = np.zeros(numDetectedObj, dtype=np.float32)
                try:
                    for objectNum in range(numDetectedObj):

                        # Read the data for each object
                        x[objectNum] = byteBuffer[idX : idX + 4].view(dtype=np.float32)
                        idX += 4
                        y[objectNum] = byteBuffer[idX : idX + 4].view(dtype=np.float32)
                        idX += 4
                        z[objectNum] = byteBuffer[idX : idX + 4].view(dtype=np.float32)
                        idX += 4
                        velocity[objectNum] = byteBuffer[idX : idX + 4].view(
                            dtype=np.float32
                        )
                        idX += 4

                    # Store the data in the detObj dictionary
                    detObj = {
                        "numObj": numDetectedObj,
                        "x": x,
                        "y": y,
                        "z": z,
                        "velocity": velocity,
                    }
                except:
                    dataOK = 0
                    return dataOK, frameNumber, detObj
                dataOK = 1

        # Remove already processed data
        if idX > 0 and byteBufferLength > idX:
            shiftSize = totalPacketLen

            byteBuffer[: byteBufferLength - shiftSize] = byteBuffer[
                shiftSize:byteBufferLength
            ]
            byteBuffer[byteBufferLength - shiftSize :] = np.zeros(
                len(byteBuffer[byteBufferLength - shiftSize :]), dtype="uint8"
            )
            byteBufferLength = byteBufferLength - shiftSize

            # Check that there are no errors with the buffer length
            if byteBufferLength < 0:
                byteBufferLength = 0

    return dataOK, frameNumber, detObj


def update(
    window: pg.GraphicsLayoutWidget,
    plot: pg.graphicsItems.PlotItem,
    onlineDash: OnlineDashboard,
) -> int:
    """Funtion to update the data and display in the plot

    Args:
        window (pg.GraphicsLayoutWidget): The window to display the plot
        plot (pg.graphicsItems.PlotItem): The plot to display the data
        onlineDash (OnlineDashboard): The online dashboard to update the data

    Returns:
        int: eroor code
    """

    dataOk = 0
    global detObj
    global iteration
    global centreX
    global centreY
    global velList
    global angList
    global last_num
    num_clusters = 0
    velSum = []
    angSum = []
    x = []
    y = []

    # Read and parse the received data
    dataOk, frameNumber, detObj = readAndParseData18xx(Dataport, configParameters)

    if dataOk and len(detObj["x"]) > 0:
        # print(detObj)
        x = -detObj["x"]
        y = detObj["y"]

        for i in range(len(x)):

            xPoints.append(x[i])
            yPoints.append(y[i])

        iteration += 1

        if iteration % 5 == 0:
            # Pass Machine Learning DBSCAN from Grouper.py:
            (
                groupCentreX,
                groupCentreY,
                num_clusters,
            ) = scanner(window, xPoints, yPoints, last_num, plot)
            velSum.clear()
            angSum.clear()
            xPoints.clear()
            yPoints.clear()
            last_num = num_clusters
            centreX.append(groupCentreX)
            centreY.append(groupCentreY)

        #
        try:
            if iteration % 30 == 0 and num_clusters > 0:
                # print(centreX, centreY)
                for i in range(num_clusters):
                    velSum.clear()
                    angSum.clear()
                    velSum = [0 for i in range(num_clusters)]
                    angSum = [0 for i in range(num_clusters)]

                vel, ang = velocity_calc(centreX, centreY)
                velList.append(vel)
                angList.append(ang)
                print("Number of people is: " + str(num_clusters))
                for i in range(len(velList)):
                    for j in range(num_clusters):
                        velSum[j] = sum(velList[i])
                        angSum[j] = sum(angList[i])
                for i in range(len(velSum)):
                    onlineDash.add_object(centreX[i], centreY[i], velSum[i], angSum[i])
                    print(
                        "Average velocity of cluster "
                        + str(i + 1)
                        + " is: "
                        + str(velSum[i])
                    )
                    print(
                        "Average angle of cluster "
                        + str(i + 1)
                        + " is: "
                        + str(angSum[i])
                        + "\n"
                    )
                centreX.clear()
                centreY.clear()
                velList.clear()
                angList.clear()
        except:
            centreX.clear()
            centreY.clear()
            velList.clear()
            angList.clear()

        for i in range(num_clusters):

            out = (
                "("
                + str(round(groupCentreX[i] * 4) / 4)
                + ", "
                + str(round(groupCentreY[i] * 4) / 4)
                + ")"
            )

            plot.addItem(pg.TextItem(out, (0, 0, 0, 255), anchor=(-1, -i + 14)))
            plot.plot(
                [1.1],
                [-i + 13.15],
                pen=None,
                symbol="o",
                symbolPen=None,
                symbolBrush=(255 / (i + 5), 200 / (i + 3), 255 / (i + 1)),
            )

        QtGui.QApplication.processEvents()

    return dataOk


def main() -> None:
    """
    Main function to run the program
    """

    # Configurate the serial port
    CLIport, Dataport = serialConfig(configFileName)

    # Get the configuration parameters from the configuration file
    parseConfigFile(configFileName)

    # START QtAPPfor the plot
    QtGui.QApplication([])

    # Set the plot
    pg.setConfigOption("background", tuple((255, 255, 255, 255)))
    window = pg.GraphicsLayoutWidget(title="Posideon Blue People Tracking")
    plot = window.addPlot()
    plot.setXRange(-5, 5)
    plot.setYRange(0, 15)
    plot.setLabel("left", text="Y position", units="m")
    plot.setLabel("bottom", text="X position", units="m")
    plot.plot(
        [],
        [],
        pen=None,
        symbolBrush=(200, 0, 0),
        symbolSize=5,
        symbol="o",
        color="w",
    )

    window.show()

    # Main loop
    detObj = {}
    frameData = {}
    currentIndex = 0
    onlineDash = OnlineDashboard()
    while True:
        try:
            # Update the data and check if the data is okay
            dataOk = update(window, plot, onlineDash)

            if dataOk:
                # Store the current frame into frameData
                frameData[currentIndex] = detObj
                currentIndex += 1
                onlineDash.send_data()
                onlineDash.clear_objects()

            # time.sleep(1/30)  # Sampling frequency of 30 Hz

        # Stop the program and close everything if Ctrl + c is pressed
        except KeyboardInterrupt:
            CLIport.write(("sensorStop\n").encode())
            CLIport.close()
            Dataport.close()
            window.close()
            break


if __name__ == "__main__":
    """
    Only run the main function if this file is run directly.
    """
    main()
