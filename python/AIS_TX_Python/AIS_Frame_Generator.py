#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Simon Acker.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
import time
from gnuradio import gr

class AIS_Frame_Generator(gr.sync_block):
    """
    AIS Frame Generator Block
    
    Generates AIS frames from comma-separated 168-bit binary payloads.
    """
    def __init__(self, binary_payloads=""):
        gr.sync_block.__init__(
            self,
            name="AIS_Frame_Generator",
            in_sig=None,
            out_sig=[np.uint8])
        
        self.payload_list = self.process_payloads(binary_payloads)
        self.current_payload_index = 0
        self.last_tx_time = 0  # Track last transmission time
        
        # Constants
        self.PREAMBLE = np.array([1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0], dtype=np.uint8)
        self.START_FLAG = np.array([0,1,1,1,1,1,1,0], dtype=np.uint8)
        self.END_FLAG = self.START_FLAG

    def process_payloads(self, payloads_str):
        """Process and validate comma-separated 168-char binary payloads"""
        payloads = [p.strip() for p in payloads_str.split(',') if p.strip()]
        
        if not payloads:
            raise ValueError("No payloads provided")
        
        processed_payloads = []
        for payload in payloads:
            # Validate length
            if len(payload) != 168:
                raise ValueError(f"Invalid payload length: {len(payload)}. Must be 168 characters")
            
            processed_payloads.append(np.array([int(b) for b in payload], dtype=np.uint8)) # Convert to binary array
                
        return processed_payloads

    def nrz_to_nrzi(self, data):
        """Convert NRZ to NRZI encoding"""
        nrzi = np.zeros_like(data)
        last_bit = 0
        for i in range(len(data)):
            if data[i] == 0:
                nrzi[i] = 1 - last_bit
            else:
                nrzi[i] = last_bit
            last_bit = nrzi[i]
        return nrzi
        
    def bit_stuff(self, data):
        """Perform bit stuffing - add 0 after five consecutive 1s"""
        result = []
        consecutives = 0
        
        for bit in data:
            result.append(bit)
            if bit == 1:
                consecutives += 1
                if consecutives == 5:
                    result.append(0)
                    consecutives = 0
            else:
                consecutives = 0
                
        return np.array(result, dtype=np.uint8)
        
    def calculate_crc(self, data):
        """Calculate CRC-16 using ITU-T polynomial with table lookup"""
        # CRC-CCITT (ITU-T) lookup table
        crc_table = [
            0x0000, 0x1189, 0x2312, 0x329B, 0x4624, 0x57AD, 0x6536, 0x74BF,
            0x8C48, 0x9DC1, 0xAF5A, 0xBED3, 0xCA6C, 0xDBE5, 0xE97E, 0xF8F7,
            0x1081, 0x0108, 0x3393, 0x221A, 0x56A5, 0x472C, 0x75B7, 0x643E,
            0x9CC9, 0x8D40, 0xBFDB, 0xAE52, 0xDAED, 0xCB64, 0xF9FF, 0xE876,
            0x2102, 0x308B, 0x0210, 0x1399, 0x6726, 0x76AF, 0x4434, 0x55BD,
            0xAD4A, 0xBCC3, 0x8E58, 0x9FD1, 0xEB6E, 0xFAE7, 0xC87C, 0xD9F5,
            0x3183, 0x200A, 0x1291, 0x0318, 0x77A7, 0x662E, 0x54B5, 0x453C,
            0xBDCB, 0xAC42, 0x9ED9, 0x8F50, 0xFBEF, 0xEA66, 0xD8FD, 0xC974,
            0x4204, 0x538D, 0x6116, 0x709F, 0x0420, 0x15A9, 0x2732, 0x36BB,
            0xCE4C, 0xDFC5, 0xED5E, 0xFCD7, 0x8868, 0x99E1, 0xAB7A, 0xBAF3,
            0x5285, 0x430C, 0x7197, 0x601E, 0x14A1, 0x0528, 0x37B3, 0x263A,
            0xDECD, 0xCF44, 0xFDDF, 0xEC56, 0x98E9, 0x8960, 0xBBFB, 0xAA72,
            0x6306, 0x728F, 0x4014, 0x519D, 0x2522, 0x34AB, 0x0630, 0x17B9,
            0xEF4E, 0xFEC7, 0xCC5C, 0xDDD5, 0xA96A, 0xB8E3, 0x8A78, 0x9BF1,
            0x7387, 0x620E, 0x5095, 0x411C, 0x35A3, 0x242A, 0x16B1, 0x0738,
            0xFFCF, 0xEE46, 0xDCDD, 0xCD54, 0xB9EB, 0xA862, 0x9AF9, 0x8B70,
            0x8408, 0x9581, 0xA71A, 0xB693, 0xC22C, 0xD3A5, 0xE13E, 0xF0B7,
            0x0840, 0x19C9, 0x2B52, 0x3ADB, 0x4E64, 0x5FED, 0x6D76, 0x7CFF,
            0x9489, 0x8500, 0xB79B, 0xA612, 0xD2AD, 0xC324, 0xF1BF, 0xE036,
            0x18C1, 0x0948, 0x3BD3, 0x2A5A, 0x5EE5, 0x4F6C, 0x7DF7, 0x6C7E,
            0xA50A, 0xB483, 0x8618, 0x9791, 0xE32E, 0xF2A7, 0xC03C, 0xD1B5,
            0x2942, 0x38CB, 0x0A50, 0x1BD9, 0x6F66, 0x7EEF, 0x4C74, 0x5DFD,
            0xB58B, 0xA402, 0x9699, 0x8710, 0xF3AF, 0xE226, 0xD0BD, 0xC134,
            0x39C3, 0x284A, 0x1AD1, 0x0B58, 0x7FE7, 0x6E6E, 0x5CF5, 0x4D7C,
            0xC60C, 0xD785, 0xE51E, 0xF497, 0x8028, 0x91A1, 0xA33A, 0xB2B3,
            0x4A44, 0x5BCD, 0x6956, 0x78DF, 0x0C60, 0x1DE9, 0x2F72, 0x3EFB,
            0xD68D, 0xC704, 0xF59F, 0xE416, 0x90A9, 0x8120, 0xB3BB, 0xA232,
            0x5AC5, 0x4B4C, 0x79D7, 0x685E, 0x1CE1, 0x0D68, 0x3FF3, 0x2E7A,
            0xE70E, 0xF687, 0xC41C, 0xD595, 0xA12A, 0xB0A3, 0x8238, 0x93B1,
            0x6B46, 0x7ACF, 0x4854, 0x59DD, 0x2D62, 0x3CEB, 0x0E70, 0x1FF9,
            0xF78F, 0xE606, 0xD49D, 0xC514, 0xB1AB, 0xA022, 0x92B9, 0x8330,
            0x7BC7, 0x6A4E, 0x58D5, 0x495C, 0x3DE3, 0x2C6A, 0x1EF1, 0x0F78
        ]
        
        # Initialize CRC
        crc = 0xFFFF
        
        # Group bits into bytes first (like unpack() in C++)
        bytes_data = []
        for i in range(0, len(data), 8):
            byte = 0
            for j in range(8):
                if i+j < len(data):
                    byte = (byte << 1) | data[i+j]
            bytes_data.append(byte)
        
        # Process each byte using table lookup (like C++ version)
        for byte in bytes_data:
            crc = ((crc >> 8) ^ crc_table[(crc ^ byte) & 0xFF]) & 0xFFFF
            
        # Final operations matching C++:
        crc = (crc & 0xFFFF) ^ 0xFFFF  # Invert
        
        # Convert to bits and handle byte swapping
        bits = [int(b) for b in format(crc, '016b')]
        # Swap bytes (8-bit chunks)
        bits = bits[8:] + bits[:8]
        
        return np.array(bits, dtype=np.uint8)
        
    def reverse_bits(self, data):
        """Reverse bits within each byte of data"""
        reversed_data = np.zeros_like(data)
        for i in range(0, len(data), 8):
            byte = data[i:i+8]
            if len(byte) == 8:  # Only process complete bytes
                reversed_data[i:i+8] = byte[::-1]  # Reverse the bits
        return reversed_data

    def work(self, input_items, output_items):
        """ Called by GNURadio to request the next output bytes.
        Used to generate a single AIS frame. If multiple payloads
        were provided on initialization, then the transmitted
        payloads will cycle through the list.
        
        Args:
            input_items: Not used (no input ports)
            output_items: List containing output numpy arrays (one per output port)
            
        Returns:
            int: Number of output items (ie bytes) produced
        """

        # Transmission rate 5 Hz
        if time.time() - self.last_tx_time < 0.2:
            return 0

        # Check if payloads are available
        if not self.payload_list:
            return 0
            
        # Get next binary payload
        payload_bits = self.payload_list[self.current_payload_index]
        self.current_payload_index = (self.current_payload_index + 1) % len(self.payload_list)
        
        # Add CRC
        crc = self.calculate_crc(payload_bits)
        payload_with_crc = np.concatenate([payload_bits, crc])
        
        # Reverse bits in payload
        rev_payload_with_crc = self.reverse_bits(payload_with_crc)

        # Bit stuff the payload
        stuffed_payload = self.bit_stuff(rev_payload_with_crc)

        # Build complete frame
        frame = np.concatenate([
            self.PREAMBLE,
            self.START_FLAG,
            stuffed_payload,
            self.END_FLAG
        ])

         # Calculate padding length
        LEN_FRAME_MAX = 256
        LEN_PREAMBLE = len(self.PREAMBLE)
        LEN_START = len(self.START_FLAG)
        LEN_STUFFED_PAYLOAD = len(stuffed_payload)
        LEN_PADDING = LEN_FRAME_MAX - (LEN_PREAMBLE + LEN_START + LEN_STUFFED_PAYLOAD + LEN_START)
        
        # Add padding
        padding = np.zeros(LEN_PADDING, dtype=np.uint8)
        frame = np.concatenate([frame, padding])
        
        # Apply NRZI encoding
        frame = self.nrz_to_nrzi(frame)

        # Pack bits into bytes
        packed_frame = np.packbits(frame)
            
        # Copies packed_frame into the first len(packed_frame) bytes 
        # of port 0 output stream
        output_items[0][:len(packed_frame)] = packed_frame
        
        # Update last transmission time
        self.last_tx_time = time.time()

        return len(packed_frame)
    
    def set_payloads(self, binary_payloads=""):
        """Update payload list"""
        self.payload_list = self.process_payloads(binary_payloads)
        self.current_payload_index = 0
