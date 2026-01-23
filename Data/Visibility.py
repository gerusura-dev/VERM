from enum import Enum
from typing import Optional
from urllib.parse import quote_plus


class VisibilityData(Enum):
    """
    イベントの公開範囲を設定する
    """

    A = "public"
    B = "group"

    @classmethod
    def get(cls, key: str) -> Optional["VisibilityData"]:
        try:
            return cls.__getitem__(key)
        except KeyError:
            return None

    @property
    def data(self) -> str:
        return self.value
