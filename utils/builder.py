import json
import hashlib
from logging import Logger
from typing import Tuple, Optional
from datetime import datetime
from dataclasses import dataclass

from .params import Mode, Params, Platform, Category, VRCEventCalendarBaseURL as BaseURL


@dataclass(slots=True)
class Payload:
    logger: Logger
    section: str
    event_name: str
    group_id: str
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
        logger: Logger,
        section: str,
        event_name: str,
        group_id: str,
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
        self.logger = logger

        self.__valid(
            event_name,
            group_id,
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
        self.group_id = group_id
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

    def __valid(
        self,
        event_name: str,
        group_id: str,
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
            self.logger.error(f"イベント名: {event_name} は不正です ... type(event_name): {type(event_name)})")
            raise TypeError

        if not isinstance(group_id, str):
            self.logger.error(f"グループID: {group_id} は不正です ... type(event_name): {type(group_id)})")
            raise TypeError

        if not isinstance(platform, Platform):
            self.logger.error(f"プラットフォーム名: {platform} は不正です ... type(platform): {type(platform)})")
            raise TypeError

        if not isinstance(start_date_time, datetime):
            self.logger.error(f"開始時刻: {start_date_time} は不正です ... type(start_date_tme): {type(start_date_time)})")
            raise TypeError

        if not isinstance(end_date_time, datetime):
            self.logger.error(f"終了時刻: {end_date_time} は不正です ... type(end_date_tme): {type(end_date_time)}")
            raise TypeError

        if not isinstance(mode, Mode):
            self.logger.error(f"登録モード: {mode} は不正です ... type(mode): {type(mode)}")
            raise TypeError

        if not isinstance(owner, str):
            self.logger.error(f"主催者: {owner} は不正です ... type(owner): {type(owner)}")
            raise TypeError

        if not isinstance(desc, str):
            self.logger.error(f"イベント説明: {desc} は不正です ... type(desc): {type(desc)}")
            raise TypeError

        if not isinstance(category, Category):
            self.logger.error(f"イベント分類: {category} は不正です ... type(category): {type(category)}")
            raise TypeError

        if not isinstance(condition, str) and condition is not None:
            self.logger.error(f"イベント参加資格: {condition} は不正です ... type(condition): {type(condition)}")
            raise TypeError

        if not isinstance(direction, str):
            self.logger.error(f"イベント参加方法: {direction} は不正です ... type(direction): {type(direction)}")
            raise TypeError

        if not isinstance(remarks, str):
            self.logger.error(f"備考: {remarks} は不正です ... type(remarks): {type(remarks)}")
            raise TypeError

        today = datetime.now()

        if start_date_time < today:
            self.logger.error(f"開始日時が過去です: start_date_time={start_date_time}, today={today}")
            raise ValueError

        if end_date_time < today:
            self.logger.error(f"終了日時が過去です: end_date_time={end_date_time}, today={today}")
            raise ValueError

        if end_date_time < start_date_time:
            self.logger.error(f"終了日時は開始日時の後である必要があります: end_date_time={end_date_time}, start_date_time={start_date_time}")
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
