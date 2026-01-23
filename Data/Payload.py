"""

# ERROR CODE
  1100000番台割り当て

  - ERROR: 1100001 => イベント開始日時が過去です
  - ERROR: 1100002 => イベント終了日時が過去です
  - ERROR: 1100003 => イベント終了日時がイベント開始日時より過去です

"""


# SECTION: Packages
import os
import json
import hashlib
from datetime import datetime
from dataclasses import dataclass
from typing import Any, List, Tuple

import Const
from Utils import get_logger
from .Params import Params


# SECTION: Base Class
@dataclass(slots=True)
class PayloadBase:
    """
    登録するデータを保持するクラス

    [対象] 変数名 ... 説明
    対象は以下の何れか
    A ... VRChat内グループイベント登録用の値
    B ... VRChatイベントカレンダー登録用の値
    C ... AとB両方で使われる
    D ... AでもBでも使われない（内部処理用など）

    [D] section         ... 1イベント分のデータが格納されているユニットの名前（EVENT1やEVENT2等、EVENT{自然数}が文字列で入る）
    [C] event_name      ... イベント名
    [A] group_id        ... イベントを開催するグループのグループID
    [A] group_category  ... 開催イベントのジャンル（複数選択不可, VRChat内グループイベント用）
    [B] platform        ... イベントの対応プラットフォーム
    [C] start_date_time ... イベントの開始日時
    [C] end_date_time   ... イベントの終了日時
    [B] mode            ... イベントの登録または削除のフラグ
    [B] owner           ... イベントの主催者
    [C] desc            ... イベントの内容説明
    [B] event_category  ... 開催イベントのジャンル（複数選択可, VRChatイベントカレンダー用）
    [B] condition       ... イベントへの参加条件
    [B] direction       ... イベントへの参加方法
    [B] remarks         ... イベントに関する備考
    [A] thumbnail       ... イベント情報のサムネイル
    [A] visibility      ... イベントの公開範囲
    [A] notification    ... イベント登録を行なったことをグループメンバーに通知するかどうか
    """

    section:         str
    event_name:      str
    group_id:        str
    group_category:  str
    platform:        str
    start_date_time: datetime
    end_date_time:   datetime
    mode:            str
    owner:           str
    desc:            str
    event_category:  List[str]
    condition:       str
    direction:       str
    remarks:         str
    thumbnail:       str
    visibility:      str
    notification:    bool


# SECTION: I/F


class Payload(PayloadBase):
    def __init__(self, **kwargs: Any) -> None:
        self.logger = get_logger()

        self.__valid(kwargs["start_date_time"], kwargs["end_date_time"])

        super().__init__(**kwargs)

    def __valid(self, start: datetime, end: datetime) -> None:
        # NOTE: イベント日時が未来であること、開始日時より終了日時が未来であることを確認する

        # Initialize
        flag1:   bool
        flag2:   bool
        flag3:   bool
        message: str
        today:   datetime = datetime.today()

        # Process
        flag1 = today < start
        flag2 = today < end
        flag3 = start < end

        if not flag1:
            # ERROR: 1100001
            message = f"ERROR: 1100001 => イベント開始日時が過去です"
            self.logger.error(message)
            self.logger.error(f"VALUE: {start}")
            raise ValueError(message)

        if not flag2:
            # ERROR: 1100002
            message = f"ERROR: 1100002 => イベント終了日時が過去です"
            self.logger.error(message)
            self.logger.error(f"VALUE: {end}")
            raise ValueError(message)

        if not flag3:
            # ERROR: 1100003
            message = f"ERROR: 1100003 => イベント終了日時がイベント開始日時より過去です"
            self.logger.error(message)
            self.logger.error(f"VALUE: start={start} => end={end}")
            raise ValueError(message)

    def __params(self) -> Tuple[str, ...]:
        return (
            Params.EventName.build(self.event_name),
            Params.Platform.build(self.platform),
            Params.StartDate.build(self.start_date_time),
            Params.EndDate.build(self.end_date_time),
            Params.Mode.build(self.mode)
        )

    @property
    def forms_url(self) -> str:
        return f"{Const.FORMS}&{'&'.join(self.__params())}"

    @property
    def payload_identity(self) -> dict:
        return {
            "section": self.section,
            "event_name": self.event_name,
            "start": self.start_date_time.isoformat(timespec="minutes"),
            "end": self.end_date_time.isoformat(timespec="minutes"),
        }

    @property
    def json_forms(self) -> str:
        identity = self.payload_identity
        identity["target"] = "GoogleForms"
        return json.dumps(identity)

    @property
    def json_vrc_api(self) -> str:
        identity = self.payload_identity
        identity["target"] = "VRChatAPI"
        return json.dumps(identity)

    @property
    def hash_forms(self) -> str:
        return hashlib.sha256(self.json_forms.encode("utf-8")).hexdigest()

    @property
    def hash_vrc_api(self) -> str:
        return hashlib.sha256(self.json_vrc_api.encode("utf-8")).hexdigest()

    @property
    def lock_target_forms(self) -> str:
        return f"tracer/{self.section}/{self.hash_forms}.json"

    @property
    def lock_target_vrc_api(self) -> str:
        return f"tracer/{self.section}/{self.hash_vrc_api}.json"

    @property
    def lock_exist_forms(self) -> bool:
        return os.path.exists(self.lock_target_forms)

    @property
    def lock_exist_vrc_api(self) -> bool:
        return os.path.exists(self.lock_target_vrc_api)
