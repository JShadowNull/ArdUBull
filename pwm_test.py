#!/usr/bin/env python3

import socket
import struct
import logging
import sys
from pymavlink import mavutil


# =============================
# Config
# =============================

# MAVLink input (receives forwarded messages from MAVProxy)
MAVLINK_UDP_PORT = 14551

# PWM output destination
UDP_IP = "192.168.1.14"
UDP_PORT = 5050

# RC channels to use (9 and 10)
RC_CH_AZIMUTH = 9   # Channel 9 for azimuth
RC_CH_ELEVATION = 10  # Channel 10 for elevation


# =============================
# Logging
# =============================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("PWM-MAVLINK-FORWARDER")


# =============================
# Main
# =============================

def main():
    logger.info(f"Starting MAVLink PWM Forwarder")
    logger.info(f"Listening for MAVLink on UDP port {MAVLINK_UDP_PORT}")
    logger.info(f"Forwarding CH{RC_CH_AZIMUTH} and CH{RC_CH_ELEVATION} to {UDP_IP}:{UDP_PORT}")

    # Create MAVLink connection (UDP listen)
    mav = mavutil.mavlink_connection(f'udpin:0.0.0.0:{MAVLINK_UDP_PORT}')

    # Create UDP socket for sending PWM values
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    logger.info("Waiting for RC_CHANNELS_OVERRIDE messages...")

    try:
        while True:
            # Receive MAVLink message
            msg = mav.recv_match(type='RC_CHANNELS_OVERRIDE', blocking=True)

            if msg is None:
                continue

            # Extract PWM values from channels 9 and 10 (indices 8 and 9)
            # RC_CHANNELS_OVERRIDE has fields: chan1_raw through chan18_raw
            az_pwm = msg.chan9_raw
            el_pwm = msg.chan10_raw

            # Only send if both channels have valid PWM values (not 65535/UINT16_MAX)
            if az_pwm == 65535 or el_pwm == 65535:
                logger.debug(f"Ignoring invalid PWM: az={az_pwm}, el={el_pwm}")
                continue

            # Pack as big-endian integers and send
            packed = struct.pack('!ii', az_pwm, el_pwm)
            send_sock.sendto(packed, (UDP_IP, UDP_PORT))

            logger.info(f"Forwarded | CH{RC_CH_AZIMUTH}={az_pwm}, CH{RC_CH_ELEVATION}={el_pwm}")

    except KeyboardInterrupt:
        logger.info("Stopping forwarder")

    finally:
        send_sock.close()
        mav.close()


if __name__ == "__main__":
    main()
