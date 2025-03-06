"""
A collection of routines that enables you to do some basic XCP protocol
operations. Includes only a subset of the XCP protocol. Mainly intended
for C9 commands.

Eaton Power Quality

author: Anders Sjoberg
date: 2014-04-01

Relies on pyserial for serial communication.

Updated to python3 syntax on 2016-03-01. Uses lists to build packets which
are then before sending converted to bytes. Whole class could be re written
to use bytes.
"""

import serial
import time
import ctypes
import random

class pyxcp(serial.Serial):
    '''
    Class that encapsulates a subset of the XCP protocol.
    '''
    
    __version__ = 3

    # Constants
    
    # cpuId constants, accessed as MEMTYPE["93PM"]["all"]
    CPUID = {
        "93PM": {
            "all": 0,
            "CSB": 1,
            "MCU": 2,
            "UPM1": 3,
            "HMI": 5,
            "MCUPLD": 6,
            "MCUBootloader": 7,
            "CSBBootloader": 8,
            "UPM1PLD": 9,
            "UPM1Bootloader": 10,
            
            "UPM2": 11,
            "UPM2PLD": 12,
            "UPM2Bootloader": 13,
            
            "UPM3": 14,
            "UPM3PLD": 15,
            "UPM3Bootloader": 16,
            
            "UPM4": 17,
            "UPM4PLD": 18,
            "UPM4Bootloader": 19,
            
            "UPM5": 20,
            "UPM5PLD": 21,
            "UPM5Bootloader": 22,
            
            "UPM6": 23,
            "UPM6PLD": 24,
            "UPM6Bootloader": 25,

            "UPM7": 26,
            "UPM7PLD": 27,
            "UPM7Bootloader": 28,

            "UPM8": 29,
            "UPM8PLD": 30,
            "UPM8Bootloader": 31,

            "UPM9": 32,
            "UPM9PLD": 33,
            "UPM9Bootloader": 34,
            
            "UPM10": 35,
            "UPM10PLD": 36,
            "UPM10Bootloader": 37,
            
            "UPM11": 38,
            "UPM11PLD": 39,
            "UPM11Bootloader": 40,
            
            "UPM12": 41,
            "UPM12PLD": 42,
            "UPM12Bootloader": 43,
            
            "UPM13": 44,
            "UPM13PLD": 45,
            "UPM13Bootloader": 46,

            "UPM14": 47,
            "UPM14PLD": 48,
            "UPM14Bootloader": 49,
            
            "UPM15": 50,
            "UPM15PLD": 51,
            "UPM15Bootloader": 52,

            "UPM16": 53,
            "UPM16PLD": 54,
            "UPM16Bootloader": 55,

            "AllUPMs": 56,
            "AllUPMPLDs": 57,
            "AllUPMBootloaders": 58,
            },
        
        "9395P": {
            "CSB": 1,
            "MCU": 2,
            "UPMs": 3,
            "display": 5,
            "PLD": 6
            }
        }

    # memType constants, accessed as MEMTYPE["93PM"]["var"]
    MEMTYPE = {
        "93PM": {
            "none": 0,
            "extRAM": 1,
            "intRAM": 2,
            "ROM": 3,
            "EEPROM": 4,
            "variable": 5,
            "boot": 6,
            },
        
        "9395P": {
            "none": 0,
            "extRAM": 1,
            "intRAM": 2,
            "ROM": 3,
            "EEPROM": 4,
            "variable": 5,
            "boot": 6,
            }
        }
    '''
    It seems that the memtypes are the same throughout the UPSs,
    so the above MEMTYPE could be depricated. Kept for backward
    compatibility.
    '''
    MTYPE = {
        "none": 0,
        "extRAM": 1,
        "intRAM": 2,
        "ROM": 3,
        "EEPROM": 4,
        "variable": 5,
        "boot": 6
        }

    _XCP_SFD = 0xAB
    _C9_CMD = 0xC9
    _C9_NACK = 0x4E
  
    def __init__(self, port, baud, txByteWait = 0.0, xcpWait = 0.1, **kwargs):
        '''
        - txByteDelay sets how long to wait in between every sent byte.
        - xcpWait is the minimum time the code waits in between packets
          before sending the next packet.
          
        This is to overcome CSB receive speed limitations. If CSB for some
        reson seems to hang or not answer, make txByteWait longer (40ms is
        a good guess).
        '''
        serial.Serial.__init__(self, port=port, baudrate=baud, **kwargs)
        
        # Force serial module timeout to 50ms
        self.timeout = 0.05
        
        self._txByteWait = txByteWait
        self._xcpWait = xcpWait

        # This is for trying to be smart with giving CSB its required time
        self._lastWrite = time.time()

        self._lastFailure = "No failures has occured"
        return

    def setTxByteWait(self, delay):
        '''
        Sets the wait time between every sent byte.
        '''
        self._txByteWait = delay
        return
    
    def setXCPWait(self, delay):
        '''
        Sets the wait time between write to CSB.
        '''
        self._xcpWait = delay
        return

    def _calculateChecksum(self, data):
        '''
        Calculate the two's complement checksum used in the XCP protocol.
        '''
        checksum = 0
        for byte in data:
            checksum = (checksum + (~byte) + 1) & 0xFF
        return checksum

    def write(self, data):
        '''
        Write one packet over XCP. Encapsulates packet in XCP headers.

        Max payload is 255 bytes. Fails in _writeSerial if is bigger.
        '''
        # Don't write non-existant data
        if len(data) < 1:
            return

        # Wait the CSB processing time
        while (time.time() - self._lastWrite) < self._xcpWait:
            continue

        # Add encapsulation
        encapData = [self._XCP_SFD, len(data)] + data
        encapData.append( self._calculateChecksum(encapData) )

        # Send it
        self._writeSerial(encapData)
        
        # Store time when last written to
        self._lastWrite = time.time() 
        return

    def _writeSerial(self, data):
        '''
        Writes a list of bytes to the serial port.
        Slows down writes if _txByteWait is not zero since it seems
        that the CSB cannot process data sent at full speed.
        '''

        # Convert list to bytes
        data = bytes(data)
        
        for byte in data:
            serial.Serial.write(self, [byte])
            
            # It seems the CSB cannot receive data fast enough in some cases.
            if self._txByteWait != 0:
                time.sleep(self._txByteWait)
        return

    
    def _readSerial(self):
        '''
        Tries to read one byte from serial port.
        '''
        # Read one byte and convert to int
        byte = int.from_bytes( serial.Serial.read(self, 1), "big")

        return byte

    def _readXCPSequence(self, timeout = 2):
        '''
        Reads a raw XCP response, only one sequence. Checksum is checked.
        Returns none if checksum fails or start delimiter is not found.

        This routine can be used directly to read responses, but it is
        reccomended to use read() as it handles packet merging and
        response checking aswell.
        '''
        # Find SFD
        startTime = time.time()
        while True:
            if time.time() - startTime > timeout:
                self._lastFailure = "Timeout"
                return None

            if self._readSerial() == self._XCP_SFD:
                break # SFD found!
        
        # Read header information
        blockNum = self._readSerial()
        length   = self._readSerial()
        seqNum   = self._readSerial()

        # Receive payload
        recData = []
        for i in range(length):
            recData.append( self._readSerial() )

        # Receive checksum
        checksum = self._readSerial()

        # Checksum match?
        if self._calculateChecksum([self._XCP_SFD, blockNum, length, seqNum] + recData) != checksum:
            self._lastFailure = "Checksum Error"
            return None

        # Build a dictionary for easy parsing
        return {"blockNum":blockNum, "length":length, "seqNum": seqNum, "data":recData}

    def read(self, timeout = 2):
        '''
        Reads a XCP response, takes sequence numbers into acount and merges
        them into one big packet. Returns None in case of error. Error reason
        can be read with getFailureReason().

        Notes:

        93PM implementation doesn't seem to follow XCP spec very strictly. For
        example the C9 read memory request doesn't repeat the function code nor
        cpu id or other address and mem size data in every packet. So the function
        code cannot be used for detecting errors reliably in a mutli packet read.
        It seems that if a NACK occurs, it either occurs in the first packet or in
        the last packet. The first packet in normally checked for all responses,
        as that works in CSB.

        The last packet is not checked for NACK. I noticed that if the memort read
        fails, the amount of words received will not match the requested amount.
        That can be used to check for successful reads.
        '''
        lastSequenceFound = False

        # Wait the CSB processing time
        while (time.time() - self._lastWrite) < self._xcpWait:
            continue

        # Store received data here
        recData = []

        # Receive all data
        while not lastSequenceFound:
            seq = self._readXCPSequence(timeout = timeout)

            # No valid data received, something has gone wrong
            if seq == None:
                return None

            # Check for ok response in first packet.
            if len(recData) == 0:
                if not self._operationSuccessful( seq["data"][0] ):
                    self._lastFailure = self._response( seq["data"][0] )
                    return None

            # Check for last sequence number (highest bit set)
            if seq["seqNum"] & 0x80:
                lastSequenceFound = True

            # Add received data to other data
            recData += seq["data"]
        
        return recData

    def getFailureReason(self):
        '''
        Returns a human readable reason for the last failure.
        '''
        return self._lastFailure


    def _operationSuccessful(self, funcCode):
        '''
        Returns true if the response returned is a considered a success.
        "Unknown Response" can be either a failure or a success depending on the
        operation. Thus it is treated as an ok response, and the user must decide
        what it really was.

        response = the function code received in the first location of the
        payload returned by read().
        '''
        okResponses = [
            "Accepted",
            "Accepted With Adjusted Parameter",
            "Memory Data Read",
            "Ack",
            "Ack End Of Mem Reached",
            "Unknown Response"
            ]

        if funcCode == None:
            return False
        
        response = self._response(funcCode)

        if response in okResponses:
            return True
        return False


    def _response(self, funcCode):
        '''
        Returns a human readable response of the last XCP operation.
        Use only if read operation was successful (read() does not
        return None). 
        
        response = the received function code returned by read() in
        the the fist location of the data list.
        If None is not returned getFailureReason() should be used.

        This function works only if the XCP communications work and
        a valid response was returned. getFailureReason() works
        even if communication does not work and has more reasons.
        '''
        responses = {
            0x31: "Accepted",
            0x32: "Not Implemented",
            0x33: "Busy",
            0x34: "Unrecognized",
            0x35: "Parameter Out Of Range",
            0x36: "Parameter Invalid",
            0x37: "Accepted With Adjusted Parameter",
            0x4E: "Negative Ack",
            0x52: "Memory Data Read",
            0x57: "Ack",
            0x58: "Ack End Of Mem Reached"
            }

        if funcCode in responses:
            return responses[funcCode]
        
        return "Unknown Response"


    def requestCapabilities(self, cpuId):
        '''
        Requests capabilities and configuration of the UPS.
        93PM support for this seems to be very scetchy.
        You have to parse it yourself.
        '''
        C9_READCONF = 0x43
        
        c9op = [self._C9_CMD, C9_READCONF, cpuId & 0xFF]
        self.write(c9op)
        return

    def requestIdBlock(self):
        '''
        Requests ID block. This includes much information form the UPS.
        You have to parse it yourself.
        '''
        XCP_REQID = 0x31
        c9op = [XCP_REQID]
        self.write(c9op)
        return


    def writeMem(self, cpuId, memType, adr, data, timeout = 2):
        '''
        Writes the words in data to adr in order.
        
        cpuId defines what board is read (this seems to be depricated).
        memType defines what memory is to be read.
        See CPUID and MEMTYPE definitions at beginning of class.

        Returns True on success, False on failure

        TODO: Automate the maximum amount of words to send.
        93PM seems to accept at most 64 words.
        9395P limit seems to be 42? At least that is what the
        service tool uses to read meters.
        '''
        if len(data) == 0:
            return

        if len(data) > 64:
            self._lastFailure = "Maximum write size is 64."
            return False

        C9_WRITE = 0x57

        # Build header
        c9op = [self._C9_CMD, C9_WRITE, cpuId & 0xFF, memType & 0xFF]

        # Add address. Split it into bytes
        adr *= 2
        c9op.append(adr >> 0  & 0xFF)
        c9op.append(adr >> 8  & 0xFF)
        c9op.append(adr >> 16 & 0xFF)
        c9op.append(adr >> 24 & 0xFF)

        # Add the data 
        for word in data:
            word = int(word)
            c9op.append(word >> 0 & 0xFF)
            c9op.append(word >> 8 & 0xFF)

        # Write eeproms
        self.write(c9op)

        # Check result
        data = self.read(timeout)
        
        if data == None:
            return False
                
        return True


    def _readFromMemRequest(self, cpuId, memType, adr, length):
        '''
        Sends a read memory request over XCP.
        '''
        if length == 0:
            return

        C9_READ = 0x52

        # Build header
        c9op = [self._C9_CMD, C9_READ, cpuId & 0xFF, memType & 0xFF]

        # Add address
        adr *= 2
        c9op.append(adr >> 0  & 0xFF)
        c9op.append(adr >> 8  & 0xFF)
        c9op.append(adr >> 16 & 0xFF)
        c9op.append(adr >> 24 & 0xFF)

        # Add number of bytes
        length *= 2
        c9op.append(length >> 0  & 0xFF)
        c9op.append(length >> 8  & 0xFF)
        c9op.append(length >> 16 & 0xFF)
        c9op.append(length >> 24 & 0xFF)

        # Send packet
        self.write(c9op)
        return

    
    def _combineBytesToWords(self, bytesStr):
        '''
        Combines a list consisting of bytes pairwise to words.
        '''
        wordsStr = []
        for i in range(0, len(bytesStr)-1, 2):
            wordsStr.append(bytesStr[i] | (bytesStr[i+1] << 8) )
        return wordsStr


    def readMem(self, cpuId, memType, start, length, timeout = 2):
        '''
        Reads 'length' amount of memory startging from 'start'.
        Returns read words. Returns None on failure.
        '''
        # Send read request
        self._readFromMemRequest(cpuId, memType, start, length)
        
        # Read response
        data = self.read(timeout = timeout)

        if data == None:
            return None

        # Decode packet header, not used for anything (yet atleast)
        r_funcCode = data[0]
        r_cpuId = data[1]
        r_memType = data[2]

        r_adr    = ( (data[3] << 0) | (data[4] << 8) | (data[5] << 16) | (data[6]  << 24) ) / 2
        r_length = ( (data[7] << 0) | (data[8] << 8) | (data[9] << 16) | (data[10] << 24) ) / 2

        # Combine bytes into words
        words = self._combineBytesToWords( data[11:] )

        # Check if received words match the requested amount. Due C9 read memory request
        # shortcomings in 93PM the "NACK" answer cannot be used to reliably detect faults
        # in multi-packet answers from the UPS.
        if len(words) != length:
            # Probably got NACK late in the read
            self._lastFailure = "Received incorrect amount of words ({} of {})".format(len(words), length)
            return None
        
        return words

    def _getSecurityKey(self, randomData, version):
        '''
        Returns security key. Expects DLL to be in same directory.

        This is only for panda platform.
        '''
        keydll = ctypes.WinDLL("mm1167sp.dll")

        RandomDataStruct = ctypes.c_ushort * 16
        keydll.GetKey.argtypes = [ctypes.POINTER(RandomDataStruct), ctypes.c_ushort]
        keydll.GetKey.restype = ctypes.c_ushort

        dataFromCsb = RandomDataStruct()
        # Copy data to c-type list
        for i in range(len(randomData)):
            dataFromCsb[i] = randomData[i];

        return keydll.GetKey(ctypes.byref(dataFromCsb), version)

    def unlock(self):
        '''
        Tries to unlock the XCP protocol. Returns True on success, False otherwise.

        This is only for panda platform.
        '''
        # Sequence to request random data        
        self.write( [0xcf, 0x00, 0x00, 0x00] )
        data = self.read(timeout = 1)

        # Nothing received or error occured
        if data == None:
            return False
        
        # Payload should be 34 bytes
        if len(data) < 34:
            self._lastFailure = "Received incorrect amount of random data."
            return False

        words = self._combineBytesToWords(data)
        key = self._getSecurityKey(words[1:], words[0])

        # Build the completion answer
        c9op = [0xcf]
        
        # Add random amount of random response bytes
        # to confuse potential buss sniffers
        for data in range(random.randint(8,55)):
            c9op.append(random.randint(0,255) & 0xFF)

        # Add key in right place
        c9op[3] = (key >> 0) & 0xFF
        c9op[4] = (key >> 8) & 0xFF

        # And send answer
        self.write(c9op)
        response = self.read(timeout = 1)

        if response != None:
            if self._response( response[0] ) == "Accepted":
                return True
        
        return False
