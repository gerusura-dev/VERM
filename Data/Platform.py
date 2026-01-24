"""

# WARNING CODE
  2030000番台割り当て

  - WARNING: 2030001 => プラットフォームの設定値が不正

"""


# SECTION: Packages(Built-in)
import logging
from enum import Enum
from typing import Optional

# SECTION: Packages(Original)
from Utils import get_logger


# SECTION: Public Class
class PlatformData(Enum):
    """
    イベントの対応プラットフォームを選択するための文字列を提供する
    """

    PC        = "PC"
    PCAndroid = "PC/android"
    Android   = "android only"

    # SECTION: Property
    @property
    def data(self) -> str:
        # Process
        return self.value

    # SECTION: Public Methods
    @classmethod
    def get(cls, key: str) -> Optional["PlatformData"]:
        # Initialize
        logger: logging.Logger

        # Process
        logger = get_logger()

        if key == "A":
            return PlatformData.PC
        elif key == "B":
            return PlatformData.PCAndroid
        elif key == "C":
            return PlatformData.Android
        else:
            # WARNING: 2030001
            logger.warning(f"WARNING: 2030001 => プラットフォーム {key} はありません")
            return None
