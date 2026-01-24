"""

# WARNING CODE
  2040000番台割り当て

  - WARNING: 2040001 => 公開範囲の設定値が不正

"""


# SECTION: Packages(Built-in)
import logging
from enum import Enum
from typing import Optional

# SECTION: Packages(Original)
from Utils import get_logger


# SECTION: Public Class
class VisibilityData(Enum):
    """
    イベントの公開範囲を設定する
    """

    A = "public"
    B = "group"

    # SECTION: Property
    @property
    def data(self) -> str:
        # Process
        return self.value

    # SECTION: Public Methods
    @classmethod
    def get(cls, key: str) -> Optional["VisibilityData"]:
        # Initialize
        logger: logging.Logger

        # Process
        logger = get_logger()

        try:
            return cls.__getitem__(key)
        except KeyError:
            # WARNING: 2040001
            logger.warning(f"WARNING: 2040001 => 公開範囲 {key} はありません")
            return None
