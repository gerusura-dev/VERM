from datetime import datetime

import pytest

from utils import (
    Mode,
    Platform,
    Payload
)


def test_builder_event_name():
    with pytest.raises(TypeError):
        Payload(
            event_name=1,
            platform=Platform.PC,
            start_date_time=datetime(2026, 1, 15, 11, 11),
            end_date_time=datetime(2026, 1, 15, 12, 34),
            mode=Mode.Registration
        )


def test_builder_platform():
    with pytest.raises(TypeError):
        Payload(
            event_name="撃剣部",
            platform=1,
            start_date_time=datetime(2026, 1, 15, 11, 11),
            end_date_time=datetime(2026, 1, 15, 12, 34),
            mode=Mode.Registration
        )


def test_builder_start_date_time():
    with pytest.raises(TypeError):
        Payload(
            event_name="撃剣部",
            platform=Platform.PC,
            start_date_time=1,
            end_date_time=datetime(2026, 1, 15, 12, 34),
            mode=Mode.Registration
        )


def test_builder_end_date_time():
    with pytest.raises(TypeError):
        Payload(
            event_name="撃剣部",
            platform=Platform.PC,
            start_date_time=datetime(2026, 1, 15, 11, 11),
            end_date_time=1,
            mode=Mode.Registration
        )


def test_builder_mode():
    with pytest.raises(TypeError):
        Payload(
            event_name="撃剣部",
            platform=Platform.PC,
            start_date_time=datetime(2026, 1, 15, 11, 11),
            end_date_time=datetime(2026, 1, 15, 12, 34),
            mode=1
        )


def test_builder_start_time_valid():
    with pytest.raises(ValueError):
        Payload(
            event_name="撃剣部",
            platform=Platform.PC,
            start_date_time=datetime(2025, 1, 15, 11, 11),
            end_date_time=datetime(2026, 1, 15, 12, 34),
            mode=Mode.Registration
        )

def test_builder_end_time_valid():
    with pytest.raises(ValueError):
        Payload(
            event_name="撃剣部",
            platform=Platform.PC,
            start_date_time=datetime(2026, 1, 15, 11, 11),
            end_date_time=datetime(2025, 1, 15, 12, 34),
            mode=Mode.Registration
        )


def test_builder_time_valid():
    with pytest.raises(ValueError):
        Payload(
            event_name="撃剣部",
            platform=Platform.PC,
            start_date_time=datetime(2026, 1, 15, 12, 34),
            end_date_time=datetime(2026, 1, 15, 11, 11),
            mode=Mode.Registration
        )
