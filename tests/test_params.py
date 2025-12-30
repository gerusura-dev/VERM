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
    pass


def test_params_build_mode():
    entry_id = Params.Mode.value
    registration = quote_plus(Mode.Registration.value)
    deregistration = quote_plus(Mode.Deregistration.value)

    assert Params.Mode.build(Mode.Registration) == f"entry.{entry_id}={registration}"
    assert Params.Mode.build(Mode.Deregistration) == f"entry.{entry_id}={deregistration}"
