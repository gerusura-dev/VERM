import os
import sys
import logging
from datetime import datetime

def setup_logger(
    name: str = "VERM",
    log_dir: str = "logs",
    level: int = logging.INFO
) -> logging.Logger:
    """
    コンソールとファイルにログ出力ための設定を終えたLoggerオブジェクトを返す

    :param name: ログの名前
    :param log_dir: ログファイルを保存するディレクトリ
    :param level: ログ出力するレベル
    :return: ロガー
    """

    # ログファイルの保存先の作成
    os.makedirs(log_dir, exist_ok=True)

    # 保存先設定
    fmt =" %(asctime)s [%(levelname)s] %(name)s: %(message)s"
    datefmt = "%Y/%m/%d %H:%M:%S"
    date = datetime.now().strftime("%Y%m%d")
    time = datetime.now().strftime("%H%M%S")
    output_dir = os.path.join(log_dir, date)
    output_name = os.path.join(output_dir, time)
    os.makedirs(output_dir, exist_ok=True)

    # ログフォーマット作成
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

    # ロガー作成
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    # 標準出力設定
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # ファイル出力設定
    file_handler = logging.FileHandler(output_name, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    # handlerの重複防止処理
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
