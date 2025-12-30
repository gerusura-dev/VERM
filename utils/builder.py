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
        today = datetime.now()

        if start_date_time < today:
            raise ValueError

        if end_date_time < today:
            raise ValueError

        if end_date_time < start_date_time:
            raise ValueError

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

    @property
    def url(self) -> str:
        return f"{BaseURL}&{'&'.join(self.__params())}"
