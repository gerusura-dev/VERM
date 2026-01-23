from enum import Enum
from typing import Union
from datetime import datetime
from urllib.parse import quote_plus


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

    def build(self, value: Union[str, datetime]) -> str:
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

        entry = f"entry.{self.value}"

        if isinstance(value, datetime):
            params = ["year", "month", "day", "hour", "minute"]
            results = [f"{entry}_{param}={quote_plus(str(getattr(value, param)))}" for param in params]
            result = "&".join(results)
        else:
            result = f"{entry}={quote_plus(value)}"

        return result
