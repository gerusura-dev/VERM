# SECTION: Packages(Built-in)
from enum import Enum


# SECTION: Public Class
class ModeData(Enum):
    """
    イベントの登録と削除を選択する文字列を提供する
    """

    Registration = "イベントを登録する"
    Deregistration = "イベントを削除する"

    # SECTION: Property
    @property
    def data(self) -> str:
        # Process
        return self.value
