import os
import sys
import logging
from datetime import datetime


__fmt = "[%(asctime)s] [%(levelname)s] %(message)s"
__datefmt = "%Y/%m/%d %H:%M:%S"


def get_logger(name: str = "VERM", log_dir: str = "logs", level: int = logging.INFO) -> logging.Logger:
    """
    ロガーを返す機能を提供する
    既にロガーが作成されていれば、作成済みのロガーを返す

    :param name: ログの名前
    :param log_dir: ログファイルを保存するディレクトリ
    :param level: ログ出力するレベル
    :return: ロガー
    """

    # ログファイル保存先のルートを作成
    os.makedirs(log_dir, exist_ok=True)

    # ロガー作成
    logger = logging.getLogger(name)

    # すでに設定済みならそのまま返す
    if logger.handlers:
        return logger

    # ログファイルの個別保存先を作成
    output_name = __setup_dirs(log_dir)

    # 未作成であればロガーの初期設定から実行する
    logger.setLevel(level)
    logger.propagate = False

    # ログのフォーマットを作成
    formatter = logging.Formatter(fmt=__fmt, datefmt=__datefmt)

    # ログハンドラーの作成
    stdout_handler = __setup_stdout_handler(level, formatter)
    file_handler = __setup_file_handler(level, formatter, output_name)

    # ハンドラーを設定
    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)

    return logger


def __setup_dirs(log_dir: str) -> str:
    """
    ログファイルを保存する個別保存先を作成する

    :param log_dir: ログファイルを保存するディレクトリ
    :return: ログファイルの名前
    """

    now = datetime.now()
    date = now.strftime("%Y%m%d")
    time = now.strftime("%H%M%S_%f")
    output_dir = os.path.join(log_dir, date)
    output_name = os.path.join(output_dir, time + ".log")
    os.makedirs(output_dir, exist_ok=True)

    return output_name


def __setup_stdout_handler(level: int, formatter: logging.Formatter) -> logging.StreamHandler:
    """
    標準出力用のログハンドラー

    :param level: ログ出力するレベル
    :param formatter: 出力するログのフォーマット
    :return: ログハンドラー
    """

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler


def __setup_file_handler(level: int, formatter: logging.Formatter, output_name: str) -> logging.FileHandler:
    """
    ファイル出力用のログハンドラー

    :param level: ログ出力するレベル
    :param formatter: 出力するログのフォーマット
    :param output_name: 出力するログファイルの名前
    :return: ログハンドラー
    """

    handler = logging.FileHandler(output_name, encoding="utf-8")
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler
