from logging import Logger

from utils import setup_logger
from utils import EventManager
from utils import AutoSubmitter


def main(logger: Logger):
    manager = EventManager(logger)
    # submitter = AutoSubmitter(logger)

    return

    try:
        for payload in manager:
            submitter.submit(payload)
    finally:
        submitter.close()


if __name__ == "__main__":
    generated_logger = setup_logger()

    generated_logger.info("自動登録処理開始")
    main(generated_logger)
    generated_logger.info("自動登録処理終了")
