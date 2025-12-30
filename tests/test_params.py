from datetime import datetime
from urllib.parse import quote_plus

from utils import (
    Mode,
    Params,
    Platform
)


def test_params_build_event_name():
    entry_id = Params.EventName.value
    event_name = "撃剣部"
    encoded_event_name = quote_plus(event_name)

    assert Params.EventName.build(event_name) == f"entry.{entry_id}={encoded_event_name}"


def test_params_build_platform():
    entry_id = Params.Platform.value
    pc = quote_plus(Platform.PC.value)
    pc_android = quote_plus(Platform.PCAndroid.value)
    android = quote_plus(Platform.Android.value)

    assert Params.Platform.build(Platform.PC) == f"entry.{entry_id}={pc}"
    assert Params.Platform.build(Platform.PCAndroid) == f"entry.{entry_id}={pc_android}"
    assert Params.Platform.build(Platform.Android) == f"entry.{entry_id}={android}"


def test_params_build_date():
    test_date = datetime(2026, 1, 15, 12, 34)
    entry_id_start = Params.StartDate.value
    entry_id_end = Params.EndDate.value

    start_date = (
        f"entry.{entry_id_start}_year={quote_plus(str(test_date.year))}&"
        f"entry.{entry_id_start}_month={quote_plus(str(test_date.month))}&"
        f"entry.{entry_id_start}_day={quote_plus(str(test_date.day))}&"
        f"entry.{entry_id_start}_hour={quote_plus(str(test_date.hour))}&"
        f"entry.{entry_id_start}_minute={quote_plus(str(test_date.minute))}")

    end_date = (
        f"entry.{entry_id_end}_year={quote_plus(str(test_date.year))}&"
        f"entry.{entry_id_end}_month={quote_plus(str(test_date.month))}&"
        f"entry.{entry_id_end}_day={quote_plus(str(test_date.day))}&"
        f"entry.{entry_id_end}_hour={quote_plus(str(test_date.hour))}&"
        f"entry.{entry_id_end}_minute={quote_plus(str(test_date.minute))}"
    )

    assert Params.StartDate.build(test_date) == start_date
    assert Params.EndDate.build(test_date) == end_date


def test_params_build_mode():
    entry_id = Params.Mode.value
    registration = quote_plus(Mode.Registration.value)
    deregistration = quote_plus(Mode.Deregistration.value)

    assert Params.Mode.build(Mode.Registration) == f"entry.{entry_id}={registration}"
    assert Params.Mode.build(Mode.Deregistration) == f"entry.{entry_id}={deregistration}"
