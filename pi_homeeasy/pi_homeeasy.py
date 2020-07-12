# Python port of https://github.com/nbogojevic/piHomeEasy/

try:
    import RPi.GPIO as GPIO
except ImportError:
    pass

import argparse
import functools
import logging
import sys
import time


logging.basicConfig()
logger = logging.getLogger(__name__)
logger_str = ""


def digital_write(pin: int, value: bool) -> None:
    """Simulate Arduino/wiringPi digitalWrite().
    """
    if "RPi.GPIO" in sys.modules:
        GPIO.output(pin, (GPIO.HIGH if value else GPIO.LOW))


def delay_microseconds(us) -> None:
    """Simulate Arduino/wiringPi delayMicroseconds().

    Note: Due to limitations of Python and Linux (Raspberry Pi OS),
    this may not perform precisely for small delay times.
    """
    time.sleep(us / 1000000.0)


def send_bit(pin: int, b: bool) -> None:
    """Send a bit pulse (describes 0 or 1) 
    1 = 310µs high then 1340µs low
    0 = 310µs high then 310µs low
    Encoding is a manchester code  
    See: http://en.wikipedia.org/wiki/Manchester_code
    """
    digital_write(pin, True)
    delay_microseconds(310)  # 275 originally, but tweaked.
    digital_write(pin, False)
    if b:
        delay_microseconds(1340)  # 1225 originally, but tweaked.
    else:
        delay_microseconds(310)

    global logger_str
    logger_str += "1" if b else "0"


def send_pair(pin: int, b: bool) -> None:
    """Data is encoded as two bits when transmitted:
    value 0 = transmitted 01
    value 1 = transmitted 10
    """
    send_bit(pin, b)
    send_bit(pin, not b)


def send_value(pin: int, value: int, length: int) -> None:
    """Sends value as binary of given length
    """
    length -= 1
    while length >= 0:
        b = (value & (1 << length)) != 0
        send_pair(pin, b)
        length -= 1


def _send(pin: int, emitter: int, receiver: int, on_off: bool) -> None:
    global logger_str

    # Do the latch sequence..
    digital_write(pin, True)
    delay_microseconds(275)  # bit of radio shouting before we start.
    digital_write(pin, False)
    delay_microseconds(9900)  # False for 9900 for latch 1
    digital_write(pin, True)  # True
    delay_microseconds(275)  # wait a moment 275µs
    digital_write(pin, False)  # False again for 2675µs - latch
    delay_microseconds(2675)
    # End on a True
    digital_write(pin, True)

    # Send emitter code (26 bits, 0-25)
    send_value(pin, emitter, 26)
    logger_str += f"(#{emitter}) "

    # Send group flag (always 0, bit 26)
    # Group activates all receivers associated to an emitter
    # Receiver code of -1 means activate group
    send_pair(pin, (receiver == -1))
    logger_str += f"({(receiver == -1)}) "

    # Send command on or off (bit 27)
    # This command can be sent as 11 (not only as 01 or 10).
    # In that case it is dimmer command, and another 4 bits need to be sent. This is not supported.
    send_pair(pin, on_off)
    logger_str += f"({on_off}) "

    # Send device code as 4 bits (bits 27-31)
    send_value(pin, (receiver if receiver >= 0 else 0), 4)
    logger_str += f"(#{(receiver if receiver >= 0 else 0)}) "

    digital_write(pin, True)  # Ending latch
    delay_microseconds(275)  # wait 275µs
    digital_write(pin, False)  # and finish signal for 2675µs

    logger.debug(logger_str)
    logger_str = ""


def send(pin: int, emitter: int, receiver: int, on_off: bool) -> None:
    if "RPi.GPIO" in sys.modules:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)

    try:
        for _ in range(3):  # Repeat 3x
            _send(pin, emitter, receiver, on_off)
    finally:
        if "RPi.GPIO" in sys.modules:
            GPIO.cleanup()


def main():
    def _int_range_check(min_value, max_value, string):
        value = int(string)
        if value < min_value or value > max_value:
            raise argparse.ArgumentTypeError(
                f"Must be integer between {min_value} and {max_value}"
            )
        return value

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument(
        "-p",
        "--pin",
        type=int,
        default=17,
        help="BCM pin number (see https://pinout.xyz/) Default: 17.",
    )
    parser.add_argument(
        "emitter_id",
        type=functools.partial(_int_range_check, 1, (1 << 26) - 1),
        help="Unique emitter number. Example: 12325262.",
    )
    parser.add_argument(
        "receiver_id",
        type=functools.partial(_int_range_check, -1, 15),
        help="Receiver number, or -1 for group command.",
    )
    parser.add_argument("command", choices=["on", "off"], help="Command to send.")

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    send(args.pin, args.emitter_id, args.receiver_id, (args.command == "on"))


if __name__ == "__main__":
    main()
