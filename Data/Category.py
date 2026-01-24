"""
# WARNING CODE
  2020000番台割り当て

  - WARNING: 2020001 => イベントカテゴリーの設定値が不正
  - WARNING: 2020002 => グループカテゴリーの設定値が不正

"""


# SECTION: Packages(Built-in)
import logging
from enum import Enum
from typing import Optional

# SECTION: Packages(Original)
from Utils import get_logger


# SECTION: Public Class
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

    # SECTION: Property
    @property
    def data(self) -> str:
        # Process
        return self.value

    # SECTION: Public Methods
    @classmethod
    def get(cls, key: str) -> Optional["EventCategoryData"]:
        # Initialize
        logger: logging.Logger

        # Process
        logger = get_logger()
        try:
            return cls.__getitem__(key)
        except KeyError:
            # WARNING: 2020001
            logger.warning(f"WARNING: 2020001 => カテゴリー {key} はありません")
            return None


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

    # SECTION: Property
    @property
    def data(self) -> str:
        # Process
        return self.value

    # SECTION: Public Methods
    @classmethod
    def get(cls, key: str) -> Optional["GroupCategoryData"]:
        # Initialize
        logger: logging.Logger

        # Process
        logger = get_logger()
        try:
            return cls.__getitem__(key)
        except KeyError:
            # WARNING: 2020002
            logger.warning(f"WARNING: 2020002 => カテゴリー {key} はありません")
            return None
