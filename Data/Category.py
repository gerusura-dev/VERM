from enum import Enum
from typing import Optional


class EventCategoryData(Enum):
    """
    VRChatEventCalendarに表示するイベントのカテゴリー
    """

    A = "アバター試着会"
    B = "改変アバター交流会"
    C = "その他交流会"
    D = "VR飲み会"
    E = "店舗系イベント"
    F = "音楽系イベント"
    G = "学術系イベント"
    H = "ロールプレイ"
    I = "初心者向けイベント"
    J = "定期イベント"

    @classmethod
    def get(cls, key: str) -> Optional["EventCategoryData"]:
        try:
            return cls.__getitem__(key)
        except KeyError:
            return None

    @property
    def data(self) -> str:
        return self.value


class GroupCategoryData(Enum):
    """
    VRChat内に表示するイベントのカテゴリー
    """

    A = "music"
    B = "gaming"
    C = "hangout"
    D = "exploring"
    E = "avatars"
    F = "film & media"
    G = "dance"
    H = "roleplaying"
    I = "performance"
    J = "wellness"
    K = "arts"
    L = "education"
    M = "other"

    @classmethod
    def get(cls, key: str) -> Optional["GroupCategoryData"]:
        try:
            return cls.__getitem__(key)
        except KeyError:
            return None

    @property
    def data(self) -> str:
        return self.value
