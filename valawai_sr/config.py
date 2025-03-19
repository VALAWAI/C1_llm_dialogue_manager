import os


class EnvironmentVariables:
    """Class for shared variables to keep consistent defaults."""

    rmq_host = os.getenv("RMQ_HOST", "host.docker.internal")
    """The hostname of the message broker."""

    exchange = os.getenv("EXCHANGE", "amq.topic")
    """The exchange to use for dialogue messages."""

    text_interface_key = os.getenv("TEXT_INTERFACE_KEY", "valawai.c0.text-interface")
    """The channel to use for dialogue messages."""

    reflect_interface_key = os.getenv(
        "REFLECT_INTERFACE_KEY", "valawai.c2.observations.reflections"
    )
    """The channel to use for reflection messages."""

    def add(self, name: str, default: str) -> None:
        """Add a new environment variable for uniformity."""
        setattr(self, name, os.getenv(name.upper(), default))


env = EnvironmentVariables()
