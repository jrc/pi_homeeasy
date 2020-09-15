# The domain of your component. Equal to the filename of your component.
DOMAIN = "rpi_rf_homeeasy"


# "requirements": [
#     "pi_homeeasy>=0.0.4"
# ]


def setup(hass, config):
    """Setup the rpi_rf_homeeasy component."""
    # States are in the format DOMAIN.OBJECT_ID.
    # hass.states.set("rpi_rf_homeeasy.Hello_World", "Works!")

    # Return boolean to indicate that initialization was successfully.
    return True
