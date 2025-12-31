import json
import hashlib
from typing import Tuple, Optional
from datetime import datetime
from dataclasses import dataclass

from .params import Mode, Params, Platform, Category, VRCEventCalendarBaseURL as BaseURL


@dataclass(slots=True)
class Payload:
    section: str
    event_name: str
    platform: Platform
    start_date_time: datetime
    end_date_time: datetime
    mode: Mode
    owner: str
    desc: str
    category: Optional[Category]
    condition: str
    direction: str
    remarks: str

    def __init__(
        self,
        section: str,
        event_name: str,
        platform: Platform,
        start_date_time: datetime,
        end_date_time: datetime,
        mode: Mode,
        owner: str,
        desc: str,
        category: Optional[Category],
        condition: str,
        direction: str,
        remarks: str
    ) -> None:
        self.__valid(
            event_name,
            platform,
            start_date_time,
            end_date_time,
            mode,
            owner,
            desc,
            category,
            condition,
            direction,
            remarks
        )

        self.section = section

        self.event_name = event_name
        self.platform = platform
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.mode = mode
        self.owner = owner
        self.desc = desc
        self.category = category
        self.condition = condition
        self.direction = direction
        self.remarks = remarks

    def __params(self) -> Tuple[str, ...]:
        return (
            Params.EventName.build(self.event_name),
            Params.Platform.build(self.platform),
            Params.StartDate.build(self.start_date_time),
            Params.EndDate.build(self.end_date_time),
            Params.Mode.build(self.mode),
        )

    @staticmethod
    def __valid(
        event_name: str,
        platform: Platform,
        start_date_time: datetime,
        end_date_time: datetime,
        mode: Mode,
        owner: str,
        desc: str,
        category: Category,
        condition: str,
        direction: str,
        remarks: str
    ) -> None:
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

        if not isinstance(owner, str):
            raise TypeError

        if not isinstance(desc, str):
            raise TypeError

        if not isinstance(category, Category):
            raise TypeError

        if not isinstance(condition, str) and condition is not None:
            raise TypeError

        if not isinstance(direction, str):
            raise TypeError

        if not isinstance(remarks, str):
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

    @property
    def hash(self) -> str:
        return hashlib.sha256(self.json.encode("utf-8")).hexdigest()

    @property
    def json(self) -> str:
        return json.dumps(self.payload_identity())

    def payload_identity(self) -> dict:
        return {
            "event_name": self.event_name,
            "start": self.start_date_time.isoformat(timespec="minutes"),
            "end": self.end_date_time.isoformat(timespec="minutes"),
        }
