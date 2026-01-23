from enum import Enum


class ModeData(Enum):
    """
    イベントの登録と削除を選択する文字列を提供する
    """

    Registration = "イベントを登録する"
    Deregistration = "イベントを削除する"

    @property
    def data(self) -> str:
        return self.value
