from typing import Tuple
from datetime import datetime
from dataclasses import dataclass

from .params import (
    Mode,
    Params,
    Platform,
    VRCEventCalendarBaseURL as BaseURL
)


@dataclass(slots=True)
class Payload:
    event_name: str
    platform: Platform
    start_date_time: datetime
    end_date_time: datetime
    mode: Mode

    def __init__(
        self,
        event_name: str,
        platform: Platform,
        start_date_time: datetime,
        end_date_time: datetime,
        mode: Mode
    ) -> None:
        self.__valid(event_name, platform, start_date_time, end_date_time, mode)

        self.event_name = event_name
        self.platform = platform
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.mode = mode

    def __params(self) -> Tuple[str, ...]:
        return (
            Params.EventName.build(self.event_name),
            Params.Platform.build(self.platform),
            Params.StartDate.build(self.start_date_time),
            Params.EndDate.build(self.end_date_time),
            Params.Mode.build(self.mode)
        )

    @staticmethod
    def __valid(
        event_name: str,
        platform: Platform,
        start_date_time: datetime,
        end_date_time: datetime,
        mode: Mode
    ):
        if not isinstance(event_name, str):
            raise TypeError

        if not isinstance(platform, Platform):
            raise TypeError

        if not isinstance(start_date_time, datetime):
            raise TypeError

        if not isinstance(end_date_time, datetime):
            raise TypeError

        if not isinstance(mode, Mode):
            raise TypeError

        today = datetime.now()

        if start_date_time < today:
            raise ValueError

        if end_date_time < today:
            raise ValueError

        if end_date_time < start_date_time:
            raise ValueError

    @property
    def url(self) -> str:
        return f"{BaseURL}&{'&'.join(self.__params())}"
