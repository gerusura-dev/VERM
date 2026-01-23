from enum import Enum
from typing import Optional
from urllib.parse import quote_plus


class PlatformData(Enum):
    """
    イベントの対応プラットフォームを選択するための文字列を提供する
    """

    PC = "PC"
    PCAndroid = "PC/android"
    Android = "android only"

    @classmethod
    def get(cls, key: str) -> Optional["PlatformData"]:
        if key == "A":
            return PlatformData.PC
        elif key == "B":
            return PlatformData.PCAndroid
        elif key == "C":
            return PlatformData.Android
        else:
            return None

    @property
    def data(self) -> str:
        return self.value
