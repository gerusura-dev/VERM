"""
VRCイベントカレンダーの自動入力に必要なGoogleFormsの入力欄の識別IDを管理し、
URLパラメータに使用する文字列を生成する機能を提供するクラス

実際に送信するURLパラメータの組み立て例
https://docs.google.com/forms/{フォーム情報}/viewform?usp=pp_url&entry.{識別ID}={値}&entry.{識別ID}={値}&...
"""


from enum import Enum
from typing import Union
from datetime import datetime
from urllib.parse import quote_plus


# VRCイベントカレンダーのイベント登録用GoogleFormsのベースURL定数
VRCEventCalendarBaseURL = "https://docs.google.com/forms/d/e/1FAIpQLSfJlabb7niRTf4rX2Q0wRc3ua9MuOEIKveo7NirR6zuOo6D9A/viewform?usp=pp_url"


class Platform(Enum):
    """
    イベントの対応プラットフォームを選択するための文字列を提供する
    """

    PC = "PC"
    PCAndroid = "PC/android"
    Android = "android+only"


class Mode(Enum):
    """
    イベントの登録と削除を選択する文字列を提供する
    """

    Registration = "イベントを登録する"
    Deregistration = "イベントを削除する"


class Params(Enum):
    """
    Google Forms の識別IDを定義

    EventName  ... 登録するイベントの名前を入力する（文字列）
    Platform   ... Android対応可否のラジオボタン
    StartDate  ... イベント開始日時
    EndDate    ... イベント終了日時
    Mode       ... 該当のイベントを登録or削除を選ぶ
    """

    EventName = 1319903296
    Platform = 412548841
    StartDate = 1310854397
    EndDate = 2042374434
    Mode = 1704463647

    def build(
        self,
        value: Union[str, int, bool, datetime, Platform, Mode]
    ) -> str:

        """
        URLパラメータとして利用できる文字列を作成する関数

        使用例
        param = Params.EventName.builder("撃剣部")
        戻り値例
        entry.1319903296=%E6%92%83%E5%89%A3%E9%83%A8
        %E6%92%83%E5%89%A3%E9%83%A8 は"撃剣部"を安全な形にエンコードしたもの

        :param value: 入力値
        :return: 組み立て済みURLパラメータ文字列(日付は必要なパラメータを全て文字列結合したものが返る)
        """

        result = ""
        entry = f"entry.{self.value}"

        if isinstance(value, Platform) or isinstance(value, Mode):
            value = value.value

        if isinstance(value, datetime):
            result += f"{entry}_year={quote_plus(str(value.year))}&"
            result += f"{entry}_month={quote_plus(str(value.month))}&"
            result += f"{entry}_day={quote_plus(str(value.day))}&"
            result += f"{entry}_hour={quote_plus(str(value.hour))}&"
            result += f"{entry}_minute={quote_plus(str(value.minute))}"
        else:
            result = f"{entry}={quote_plus(str(value))}"

        return result
