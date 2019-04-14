from datetime import datetime

from quotepad.models import Text
from quotepad.serializers import BinaryTextEncoder, FOOTER, HEADER


def test_no_text():
    test_text = Text(text="", active=True, created=datetime.now())
    expected_binary = bytes(HEADER + FOOTER)
    observed_binary = BinaryTextEncoder.serialize(test_text)

    assert observed_binary == expected_binary


def test_single_letter():
    text = "a"
    test_text = Text(text=text, active=True, created=datetime.now())
    expected_binary = HEADER + bytes(text, 'ascii') + bytes([0x01]) + FOOTER
    observed_binary = BinaryTextEncoder.serialize(test_text)

    assert observed_binary == expected_binary


def test_longer_text():
    text = 'test'
    test_text = Text(text=text, active=True, created=datetime.now())
    expected_binary = HEADER + bytes.fromhex('74 01 65 01 73 01 74 01') + FOOTER
    observed_binary = BinaryTextEncoder.serialize(test_text)

    assert observed_binary == expected_binary
