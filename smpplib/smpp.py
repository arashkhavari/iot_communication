"""SMPP module"""

from . import pdu
from . import command


def make_pdu(command_name, **kwargs):
    """Return PDU instance"""

    f = command.factory(command_name, **kwargs)

    return f


def parse_pdu(data, **kwargs):
    """Parse binary PDU"""

    command = pdu.extract_command(data)

    if command is None:
        return None

    new_pdu = make_pdu(command, **kwargs)
    new_pdu.parse(data)

    return new_pdu