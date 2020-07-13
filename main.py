import pi_homeeasy

import argparse
import functools
import logging


def main():
    logging.basicConfig()

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
        logging.getLogger().setLevel(logging.DEBUG)

    pi_homeeasy.send(
        args.pin, args.emitter_id, args.receiver_id, (args.command == "on")
    )


if __name__ == "__main__":
    main()
