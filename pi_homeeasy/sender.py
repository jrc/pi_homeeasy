# Python port of https://github.com/nbogojevic/piHomeEasy/

import logging
import sys
import time


logger = logging.getLogger(__name__)
logger_str = ""


try:
    import RPi.GPIO as GPIO
except ImportError as e:
    logger.error("Can't import RPi.GPIO ({}). Enabling debug logging.".format(e))
    logger.setLevel(logging.DEBUG)


def digital_write(pin: int, value: bool) -> None:
    """Like Arduino/wiringPi's digitalWrite()."""
    if "RPi.GPIO" in sys.modules:
        GPIO.output(pin, (GPIO.HIGH if value else GPIO.LOW))


def delay_microseconds(us) -> None:
    """Like Arduino/wiringPi's delayMicroseconds().

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
    """Sends value as binary of given length"""
    length -= 1
    while length >= 0:
        b = (value & (1 << length)) != 0
        send_pair(pin, b)
        length -= 1


def _send_once(emitter: int, receiver: int, on_off: bool, gpio_pin: int) -> None:
    global logger_str

    # Do the latch sequence..
    digital_write(gpio_pin, True)
    delay_microseconds(275)  # bit of radio shouting before we start.
    digital_write(gpio_pin, False)
    delay_microseconds(9900)  # False for 9900 for latch 1
    digital_write(gpio_pin, True)  # True
    delay_microseconds(275)  # wait a moment 275µs
    digital_write(gpio_pin, False)  # False again for 2675µs - latch
    delay_microseconds(2675)
    # End on a True
    digital_write(gpio_pin, True)

    # Send emitter code (26 bits, 0-25)
    send_value(gpio_pin, emitter, 26)
    logger_str += f"(#{emitter}) "

    # Send group flag (always 0, bit 26)
    # Group activates all receivers associated to an emitter
    # Receiver code of -1 means activate group
    send_pair(gpio_pin, (receiver == -1))
    logger_str += f"({(receiver == -1)}) "

    # Send command on or off (bit 27)
    # This command can be sent as 11 (not only as 01 or 10).
    # In that case it is dimmer command, and another 4 bits need to be sent. This is not supported.
    send_pair(gpio_pin, on_off)
    logger_str += f"({on_off}) "

    # Send device code as 4 bits (bits 28-31)
    send_value(gpio_pin, (receiver if receiver >= 0 else 0), 4)
    logger_str += f"(#{(receiver if receiver >= 0 else 0)}) "

    digital_write(gpio_pin, True)  # Ending latch
    delay_microseconds(275)  # wait 275µs
    digital_write(gpio_pin, False)  # and finish signal for 2675µs

    logger.debug(logger_str)
    logger_str = ""


def send(emitter: int, receiver: int, on_off: bool, gpio_pin: int) -> None:
    if "RPi.GPIO" in sys.modules:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin, GPIO.OUT)

    try:
        for _ in range(5):
            _send_once(emitter, receiver, on_off, gpio_pin)
            delay_microseconds(10)
    finally:
        if "RPi.GPIO" in sys.modules:
            GPIO.cleanup()
