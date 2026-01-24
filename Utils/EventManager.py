"""

# ERROR CODE
  1030000番台割り当て

  - ERROR: 1030001 => config.iniの基本的な書式に問題がある

"""


# SECTION: Packages(Built-in)
import os
from logging import Logger
from typing import List, Iterator
from datetime import datetime, timedelta
from configparser import ConfigParser

# SECTION: Packages(Original)
from Data import Payload, ModeData
from .DataParser import (
    get_logger,
    event_name_parser,
    group_id_parser,
    group_category_parser,
    platform_parser,
    base_date_parser,
    event_time_parser,
    owner_parser,
    description_parser,
    event_category_parser,
    condition_parser,
    director_parser,
    remarks_parser,
    thumbnail_parser,
    visibility_parser,
    notification_parser
)


# SECTION: Public Class
class EventManager:
    def __init__(self, config_file: str = "config.ini") -> None:
        # Initialize
        self.logger: Logger
        self.config: ConfigParser
        self.events: List[Payload]

        # Process
        self.logger = get_logger()
        self.logger.info("EventManager initialize start")

        # 設定ファイルの存在確認
        if not os.path.isfile(config_file):
            message = "config.iniファイルがありません"
            self.logger.error(message)
            raise FileNotFoundError(message)

        # 設定ファイル読込
        self.config = ConfigParser()

        try:
            # NOTE: .iniファイルの基本的な書き方に問題があった場合はここでトラブル
            self.config.read(config_file, encoding="utf-8")
        except Exception as e:
            # ERROR: 1030001
            self.logger.error(e)
            self.logger.error("Error: 1030001 => config.iniの書式が不正です")
            raise e

        # 登録するイベントの一覧を取得
        self.events = self.__parser()
        if self.events:
            for event in self.events:
                self.logger.info(f"New Event: {event.event_name}")
        else:
            self.logger.info(f"New Event: なし")

        self.logger.info("EventManager initialize end")

    def __iter__(self) -> Iterator[Payload]:
        return iter(self.events)

    # SECTION: Private Methods
    def __parser(self) -> List[Payload]:
        # Initialize
        event_name:     str
        group_id:       str
        group_category: str
        platform:       str
        owner:          str
        base_date:      datetime
        event_time:     timedelta
        desc:           str
        event_category: List[str]
        condition:      str
        direction:      str
        remarks:        str
        thumbnail:      str
        visibility:     str
        notification:   bool
        start_date_time: datetime
        end_date_time:   datetime
        mode:            str
        events:          List[Payload] = []

        # Process
        for section in self.config.sections():
            kwargs = {
                "section": section,
                "event_name": event_name_parser(self.config, section),
                "group_id": group_id_parser(self.config, section),
                "group_category": group_category_parser(self.config, section),
                "platform": platform_parser(self.config, section),
                "mode": ModeData.Registration.data,
                "owner": owner_parser(self.config, section),
                "desc": description_parser(self.config, section),
                "event_category": event_category_parser(self.config, section),
                "condition": condition_parser(self.config, section),
                "direction": director_parser(self.config, section),
                "remarks": remarks_parser(self.config, section),
                "thumbnail": thumbnail_parser(self.config, section),
                "visibility": visibility_parser(self.config, section),
                "notification": notification_parser(self.config, section)
            }


            base_date = base_date_parser(self.config, section)
            event_time = event_time_parser(self.config, section)

            kwargs["start_date_time"] = self.__calc_next_date(base_date)
            kwargs["end_date_time"] = kwargs["start_date_time"] + event_time

            payload = Payload(**kwargs)

            if payload.lock_exist_forms and payload.lock_exist_vrc_api:
                # NOTE: lock_exist_forms and lock_exist_vrc_apiがTrue => 登録が全て完了している状態
                continue

            events.append(payload)

        return events


    @staticmethod
    def __calc_next_date(base_date: datetime) -> datetime:
        """
        base_dateと同じ曜日で最も近い未来の日時を計算して返す機能を提供する

        :param base_date: 設定ファイルに書かれた基準日時（この時刻を元に最も近い未来の日付が計算される）
        :return: イベントを開催する日時
        """

        # Initialize
        now:        datetime
        days_ahead: int
        candidate:  datetime

        # Process
        now = datetime.now()

        # NOTE: 基準日時と現在の曜日の差分日数を計算（現在日時から何日足せば良いか判断する）
        days_ahead = (base_date.weekday() - now.weekday()) % 7

        # NOTE: 現在時刻に差分日数を足し、時刻を開催時刻に変更する
        candidate = now + timedelta(days=days_ahead)
        candidate = candidate.replace(
            hour=base_date.hour,
            minute=base_date.minute,
            second=0,
            microsecond=0
        )

        # NOTE: もし仮に計算後の日時が現在と同じor過去である場合、さらに一週間後を指定する
        if candidate <= now:
            candidate += timedelta(days=7)

        return candidate
