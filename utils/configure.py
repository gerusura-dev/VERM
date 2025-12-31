import os
from typing import List, Iterator, Optional
from configparser import ConfigParser
from datetime import datetime, timedelta

from .builder import Payload
from .params import Mode, Platform, Category


class EventManager:
    def __init__(self, config_file: str = "config.ini") -> None:
        if not os.path.isfile(config_file):
            raise FileNotFoundError()

        self.__config = ConfigParser()
        self.__config.read(config_file, encoding="utf-8")

        self.event_list = self.__config_parser()

    def __iter__(self) -> Iterator[Payload]:
        return iter(self.event_list)

    def __config_parser(self) -> List[Payload]:
        event_list = []

        for section in self.__config.sections():
            event_name = self.__config[section]["EVENT_NAME"]
            platform = Platform.get_platform(self.__config[section]["PLATFORM"])
            base_date = datetime.strptime(self.__config[section]["BASE_DATE"], "%Y/%m/%d %H:%M")
            event_time = self.__config.getfloat(section, "EVENT_TIME")
            owner = self.__config[section]["OWNER"]
            desc = self.__config[section]["DESC"]
            category = self.__config[section]["CATEGORY"]
            condition = self.__config[section]["JOIN_CONDITION"]
            direction = self.__config[section]["JOIN_DIRECTION"]
            remarks = self.__config[section]["REMARKS"]

            if platform is None:
                raise ValueError

            category = category if category != "" else None
            if category is not None:
                category = Category.get_category(int(category))

            start_date_time = self.__calc_next_date(base_date)
            if start_date_time is None:
                continue

            end_date_time = start_date_time + timedelta(hours=event_time)
            mode = Mode.Registration

            os.makedirs("tracer", exist_ok=True)
            os.makedirs(f"tracer/{section}", exist_ok=True)

            payload = Payload(
                section=section,
                event_name=event_name,
                platform=platform,
                start_date_time=start_date_time,
                end_date_time=end_date_time,
                mode=mode,
                owner=owner,
                desc=desc,
                category=category,
                condition=condition,
                direction=direction,
                remarks=remarks
            )

            if not os.path.exists(f"tracer/{section}/{payload.hash}.json"):
                event_list.append(payload)

        return event_list

    @staticmethod
    def __calc_next_date(base_date: datetime, now: Optional[datetime] = None) -> datetime:
        if now is None:
            now = datetime.now()

        base_weekday = base_date.weekday()
        now_weekday = now.weekday()

        days_ahead = (base_weekday - now_weekday) % 7

        candidate = now + timedelta(days=days_ahead)
        candidate = candidate.replace(
            hour=base_date.hour,
            minute=base_date.minute,
            second=0,
            microsecond=0,
        )

        if candidate <= now:
            candidate += timedelta(days=7)

        return candidate
