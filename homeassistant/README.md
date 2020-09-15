# Home Assistant - Raspberry Pi RF HomeEasy/Nexa Integration

The existing [Raspberry Pi RF](https://www.home-assistant.io/integrations/rpi_rf) is based on `rpi-rf`, which is in turn based on `rc-switch`, which is [not](https://github.com/sui77/rc-switch/issues/42) [compatible](https://github.com/sui77/rc-switch/pull/124) with HomeEasy/Nexa devices. (?) though see https://github.com/milaq/rpi-rf/pull/5 …?


## Installation

1. Install `config/custom_components/rpi_rf_homeeasy` in your Home Assistant's `config` directory. (You might want to use the [Samba add-on](https://www.home-assistant.io/getting-started/configuration/#editing-configuration-via-sambawindows-networking) to do this.)
2. Add the following to your Home Assistant's `config/configuration.yaml`:

    # Example configuration.yaml entry
    switch:
        platform: rpi_rf_homeeasy

        # gpio_pin: 17
        # emitter: 52078445
        # receiver: 0

3. Go to http://homeassistant.local:8123/config/server_control and restart the Home Assistant server.
