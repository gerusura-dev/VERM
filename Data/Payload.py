"""

# ERROR CODE
  1020000番台割り当て

  - ERROR: 1020001 => イベント開始日時が過去です
  - ERROR: 1020002 => イベント終了日時が過去です
  - ERROR: 1020003 => イベント終了日時がイベント開始日時より過去です

"""


# SECTION: Packages(Built-in)
import os
import json
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Any, List, Dict, Tuple

# SECTION: Packages(Original)
import Const
from .Params import Params
from Utils import get_logger


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


# SECTION: Public Class
class Payload(PayloadBase):
    def __init__(self, **kwargs: Any) -> None:
        # Initialize
        self.logger: logging.Logger

        # Process
        self.logger = get_logger()
        self.__valid(kwargs["start_date_time"], kwargs["end_date_time"])
        super().__init__(**kwargs)

    # SECTION: Property
    @property
    def forms_url(self) -> str:
        """
        事前入力有りGoogle Formsの組み立て済みURLを返す

        :return: Google FormsへのURL文字列
        """

        # Process
        return f"{Const.FORMS}&{'&'.join(self.__params())}"

    @property
    def payload_identity(self) -> Dict[str, str]:
        """
        登録処理が完了しているかを確認するために用いるハッシュ値とJSONデータの元データを提供する

        :return: ハッシュ作成、JSONファイル向けデータ
        """

        # Process
        return {
            "section": self.section,
            "event_name": self.event_name,
            "start": self.start_date_time.isoformat(timespec="minutes"),
            "end": self.end_date_time.isoformat(timespec="minutes"),
        }

    @property
    def json_forms(self) -> str:
        """
        Google Formsの登録処理の完了を示すファイルを生成するためのJSONデータを提供する
        payload_identity
        に追加で
        key=target, value=GoogleForms
        が入る

        :return: Google Forms用JSONデータ
        """

        # Initialize
        identity: Dict[str, str]

        # Process
        identity = self.payload_identity
        identity["target"] = "GoogleForms"
        return json.dumps(identity)

    @property
    def json_vrc_api(self) -> str:
        """
        VRChat内イベントカレンダーへの登録処理の完了を示すファイルを生成するためのJSONデータを提供する
        payload_identity
        に追加で
        key=target, value=VRChatAPI
        が入る

        :return: VRChat内イベントカレンダー用JSONデータ
        """

        # Initialize
        identity: Dict[str, str]

        # Process
        identity = self.payload_identity
        identity["target"] = "VRChatAPI"
        return json.dumps(identity)

    @property
    def hash_forms(self) -> str:
        """
        Google Forms用のハッシュ値を提供する

        :return: ハッシュ値文字列
        """

        # Process
        return hashlib.sha256(self.json_forms.encode("utf-8")).hexdigest()

    @property
    def hash_vrc_api(self) -> str:
        """
        VRChatAPI用のハッシュ値を提供する

        :return: ハッシュ値文字列
        """

        # Process
        return hashlib.sha256(self.json_vrc_api.encode("utf-8")).hexdigest()

    @property
    def lock_target_forms(self) -> Path:
        """
        Google Forms用のロックファイル保存先を提供する

        :return: 保存先のPath
        """

        # Process
        return Path(f"tracer/{self.section}/{self.hash_forms}.json")

    @property
    def lock_target_vrc_api(self) -> Path:
        """
        VRChatAPI用のロックファイルの保存先を提供する

        :return: 保存先のPath
        """

        # Process
        return Path(f"tracer/{self.section}/{self.hash_vrc_api}.json")

    @property
    def lock_exist_forms(self) -> bool:
        """
        Google Forms用のロックファイルが存在するかの結果をBool値で提供する

        :return: ロックファイルが存在するか否かのBool値
        """

        # Process
        return os.path.exists(self.lock_target_forms)

    @property
    def lock_exist_vrc_api(self) -> bool:
        """
        VRChatAPI用のロックファイルが存在するかの結果をBool値で提供する

        :return: ロックファイルが存在するか否かのBool値
        """

        # Process
        return os.path.exists(self.lock_target_vrc_api)

    # SECTION: Private Methods
    def __valid(self, start: datetime, end: datetime) -> None:
        """
        イベントの開始日時と終了日時が現在時刻より未来であること、
        イベントの終了日時が開始日時より未来であることを確認する

        :param start: イベント開始日時
        :param end: イベント終了日時
        :return: None
        """

        # Initialize
        flag1:   bool
        flag2:   bool
        flag3:   bool
        message: str
        today:   datetime = datetime.today()

        # Process
        flag1 = today < start  # イベント開始日時が現在より未来であるかのBool値
        flag2 = today < end    # イベント終了日時が現在より未来であるかのBool値
        flag3 = start < end    # イベントの終了日時が開始日時より未来であるかのBool値

        if not flag1:
            # ERROR: 1020001
            message = f"ERROR: 1020001 => イベント開始日時が過去です"
            self.logger.error(message)
            self.logger.error(f"VALUE: {start}")
            raise ValueError(message)

        if not flag2:
            # ERROR: 1020002
            message = f"ERROR: 1020002 => イベント終了日時が過去です"
            self.logger.error(message)
            self.logger.error(f"VALUE: {end}")
            raise ValueError(message)

        if not flag3:
            # ERROR: 1020003
            message = f"ERROR: 1020003 => イベント終了日時がイベント開始日時より過去です"
            self.logger.error(message)
            self.logger.error(f"VALUE: start={start} => end={end}")
            raise ValueError(message)

    def __params(self) -> Tuple[str, str, str, str, str]:
        """
        Google Formsの事前入力設定用のパラメータを返す

        :return: URLパラメータ文字列
        """

        # Process
        return (
            Params.EventName.build(self.event_name),
            Params.Platform.build(self.platform),
            Params.StartDate.build(self.start_date_time),
            Params.EndDate.build(self.end_date_time),
            Params.Mode.build(self.mode)
        )
