"""
VRCイベントカレンダーの自動入力に必要なGoogleFormsの入力欄の識別IDを管理し、
URLパラメータに使用する文字列を生成する機能を提供するクラス

実際に送信するURLパラメータの組み立て例
https://docs.google.com/forms/{フォーム情報}/viewform?usp=pp_url&entry.{識別ID}={値}&entry.{識別ID}={値}&...
"""


# SECTION: Package(Original)
from .Params import Params
from .Mode import ModeData
from .Payload import Payload
from .Platform import PlatformData
from .Visibility import VisibilityData
from .Category import (
    EventCategoryData,
    GroupCategoryData
)
