"""

# ERROR CODE
  1000000番台割り当て

  - ERROR: 1000001 => 設定値が見つからない
  - ERROR: 1000002 => 必須入力項目が入力されていない
  - ERROR: 1000003 => 設定値の形式が不正

# WARNING CODE
  2000000番台割り当て

  - WARNING: 2000001 => 値が不正

"""

# NOTE: value_error関数は独自定義エラーに置換したい


# SECTION: Packages(Built-in)
import uuid
import logging
from typing import Any, List, Optional
from datetime import datetime, timedelta
from configparser import ConfigParser

# SECTION: Packages(Original)
from .Logger import get_logger
from Data import (
    GroupCategoryData,
    EventCategoryData,
    PlatformData,
    VisibilityData
)


# SECTION: Parser Utilities


def value_error(message: str, value: Any, _: Optional[Exception] = None) -> None:
    # Initialize
    logger: logging.Logger

    # Process
    logger = get_logger()
    logger.error(message)
    logger.error(f"VALUE: {value}")
    raise ValueError(message)


def value_warning(message: str, value: Any) -> None:
    # Initialize
    logger: logging.Logger

    # Process
    logger = get_logger()
    logger.warning(message)
    logger.warning(f"VALUE: {value}")


def exist_check(config: ConfigParser, section: str, config_name: str) -> str:
    # Initialize
    value: Optional[str]

    # Process
    value = config.get(section, config_name, fallback=None)
    if value is None:
        # ERROR: 1000001
        value_error(f"ERROR: 1000001 => 設定値に '{config_name}' が見つかりません", value)

    return value


def require_check(value: str, config_name: str) -> None:
    # Process
    if len(value) == 0:
        # ERROR: 1000002
        value_error(f"ERROR: 1000002 => '{config_name}' は必須入力項目です", value)


def require_parser_template(config: ConfigParser, section: str, config_name: str) -> str:
    # Initialize
    value: str

    # Process
    value = exist_check(config, section, config_name)
    require_check(value, config_name)

    return value


def uuid_parser(value: Any, config_name:str, uuid_str: str) -> None:
    # Process
    try:
        uuid.UUID(uuid_str)
    except (ValueError, TypeError, AttributeError):
        # ERROR: 1000003
        value_error(f"ERROR: 1000003 => 設定値の '{config_name}' の形式が不正です", value)


# SECTION: Parser


def event_name_parser(config: ConfigParser, section: str) -> str:
    # INFO: Require

    # Initialize
    config_name: str

    # Process
    config_name = "EVENT_NAME"
    return require_parser_template(config, section, config_name)


def group_id_parser(config: ConfigParser, section: str) -> str:
    # INFO: Require

    # Initialize
    value:       str
    uuid_str:    str
    config_name: str

    # Process
    config_name = "GROUP_ID"
    value = require_parser_template(config, section, config_name)

    uuid_str = value.split("_")[-1]
    uuid_parser(value, config_name, uuid_str)

    return value


def group_category_parser(config: ConfigParser, section: str) -> str:
    # INFO: Require

    # Initialize
    value:       str
    category:    Optional[GroupCategoryData]
    config_name: str

    # Process
    config_name = "GROUP_CATEGORY"
    value = require_parser_template(config, section, config_name)

    category = GroupCategoryData.get(value)
    if category is None:
        # ERROR: 1000003
        value_error(f"ERROR: 1000003 => 設定値の '{config_name}' の形式が不正です", value)

    return category.data


def platform_parser(config: ConfigParser, section: str) -> str:
    # INFO: Require

    # Initialize
    value:       str
    platform:    Optional[PlatformData]
    config_name: str

    # Process
    config_name = "PLATFORM"
    value = require_parser_template(config, section, config_name)

    platform = PlatformData.get(value)
    if platform is None:
        # ERROR: 1000003
        value_error(f"ERROR: 1000003 => 設定値の '{config_name}' の形式が不正です", value)

    return platform.data


def base_date_parser(config: ConfigParser, section: str) -> datetime:
    # INFO: Require

    # Initialize
    value:       str
    base_date:   Optional[datetime]
    config_name: str

    # Process
    base_date = None
    config_name = "BASE_DATE"
    value = require_parser_template(config, section, config_name)

    try:
        base_date = datetime.strptime(value, "%Y/%m/%d %H:%M")
    except ValueError:
        # ERROR: 1000003
        value_error(f"ERROR: 1000003 => 設定値の '{config_name}' の形式が不正です", value)

    if base_date is None:
        # NOTE: 値の初期化でNoneを入れているので、念のためにチェック（おそらくこのifが引っかかることはない）
        # ERROR: 1000003
        value_error(f"ERROR: 1000003 => 設定値の '{config_name}' の形式が不正です", value)

    return base_date


def event_time_parser(config: ConfigParser, section: str) -> timedelta:
    # INFO: Require

    # Initialize
    value:       str
    event_time:  Optional[float]
    config_name: str

    # Process
    event_time = None
    config_name = "EVENT_TIME"
    value = require_parser_template(config, section, config_name)

    try:
        event_time = float(value)
    except ValueError:
        # ERROR: 1000003
        value_error(f"ERROR: 1000003 => 設定値の '{config_name}' の形式が不正です", value)

    if event_time is None:
        # NOTE: 値の初期化でNoneを入れているので、念のためにチェック（おそらくこのifが引っかかることはない）
        # ERROR: 1000003
        value_error(f"ERROR: 1000003 => 設定値の '{config_name}' の形式が不正です", value)

    return timedelta(hours=event_time)


def owner_parser(config: ConfigParser, section: str) -> str:
    # INFO: Require

    # Initialize
    config_name: str

    # Process
    config_name = "OWNER"
    return require_parser_template(config, section, config_name)


def description_parser(config: ConfigParser, section: str) -> str:
    # Initialize
    config_name: str

    # Process
    config_name = "DESC"
    return exist_check(config, section, config_name)


def event_category_parser(config: ConfigParser, section: str) -> List[str]:
    # Initialize
    value:       str
    item:        str
    items:       List[str]
    category:    Optional[EventCategoryData]
    categories:  List[str]
    config_name: str

    # Process
    categories = []
    config_name = "EVENT_CATEGORY"
    value = exist_check(config, section, config_name)

    if len(value) != 0:
        try:
            items = [s.strip() for s in value.split(",") if s.strip()]
            for item in items:
                category = EventCategoryData.get(item)
                if category is None:
                    # WARNING: 2000001
                    value_warning(f"WARNING: 2000001 => '{config_name}' の {item} は無効な値です", value)
                    continue
                categories.append(category.data)
        except Exception as e:
            # ERROR: 1000003
            value_error(f"ERROR: 1000003 => 設定値の '{config_name}' の形式が不正です", value, e)

    return categories


def condition_parser(config: ConfigParser, section: str) -> str:
    # Initialize
    config_name: str = "JOIN_CONDITION"

    # Process
    return exist_check(config, section, config_name)


def director_parser(config: ConfigParser, section: str) -> str:
    # Initialize
    config_name: str = "JOIN_DIRECTION"

    # Process
    return exist_check(config, section, config_name)


def remarks_parser(config: ConfigParser, section: str) -> str:
    # Initialize
    config_name: str = "REMARKS"

    # Process
    return exist_check(config, section, config_name)


def thumbnail_parser(config: ConfigParser, section: str) -> str:
    # Initialize
    value:       str
    uuid_str:    str
    config_name: str = "EVENT_THUMBNAIL"

    # Process
    value = exist_check(config, section, config_name)

    uuid_str = value.split("_")[-1]
    uuid_parser(value, config_name, uuid_str)

    return value


def visibility_parser(config: ConfigParser, section: str) -> str:
    # INFO: Require

    # Initialize
    value:       str
    visibility:  Optional[VisibilityData]
    config_name: str = "VISIBILITY"

    # Process
    value = require_parser_template(config, section, config_name)

    visibility = VisibilityData.get(value)
    if visibility is None:
        # ERROR: 1000003
        value_error(f"ERROR: 1000003 => 設定値の '{config_name}' の形式が不正です", value)

    return visibility.data


def notification_parser(config: ConfigParser, section: str) -> bool:
    # INFO: Require

    # Initialize
    value:       Optional[bool]
    config_name: str = "NOTIFICATION"

    # Process
    value = config.getboolean(section, config_name, fallback=None)
    if value is None:
        # ERROR: 1000002
        value_error(f"ERROR: 1000002 => '{config_name}' は必須入力項目です", value)

    return value
