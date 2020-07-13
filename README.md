# pi_homeeasy

This is a Python port of [piHomeEasy](https://github.com/nbogojevic/piHomeEasy). It lets you use a Raspberry Pi with a low-cost 433 MHz transmitter to send on/off control codes to RF-controlled power outlets that use the HomeEasy self-learning protocol.

Compatible devices have been sold in Europe under the following brands:

* Bye Bye Standby / Domia Lite (UK)
* Chacon (Belgium)
* Düwi (Germany)
* HomeEasy / Byron / Smartwares (Netherlands)
* Intertechno (Austria)
* KlikAanKlikUit (Netherlands)
* Anslut / Proove / Nexa / Telldus (Sweden)
* etc.

This package is designed to work well with [Home Assistant](https://www.home-assistant.io/). 


## Protocol

* http://tech.jolowe.se/home-automation-rf-protocols/
* https://homeeasyhacking.fandom.com/wiki/Advanced_Protocol


## Wiring

Raspberry Pi | 433 MHz transmitter module
--- | ---
5V Power | VCC
Ground | GND
GPIO/BCM 17 | DATA

For diagrams, see https://pinout.xyz/ and https://tutorials-raspberrypi.com/control-raspberry-pi-wireless-sockets-433mhz-tutorial/.  (The square module is the 433 MHz transmitter; the rectangular module is the 433 MHz receiver, not used here.)


## Usage

    $ python3 -m venv env
    $ source env/bin/activate
    (env) $ cd pi_homeeasy
    (env) $ pip install -r requirements.txt
    (env) $ python main.py 12345678 1 on
    # or
    (env) $ python
    >>> import pi_homeeasy
    >>> pi_homeeasy.send(17, 12325262, 1, True)
