from logging import Logger

from utils import setup_logger
from utils import EventManager
from utils import AutoSubmitter
from utils import login


def main(logger: Logger):
    manager = EventManager(logger)
    submitter = AutoSubmitter(logger)

    try:
        for payload in manager:
            logger.info("VRCイベントカレンダー登録開始")
            # イベントカレンダー登録処理
            # submitter.submit(payload)
            logger.info("VRCイベントカレンダー登録完了")

            logger.info("VRC内カレンダー登録開始")
            # カレンダー登録処理
            cookies = login(logger)
            submitter.registration(payload, cookies)
            logger.info("VRC内カレンダー登録完了")
    except Exception as e:
        print(e)
    # finally:
        # submitter.close()


if __name__ == "__main__":
    generated_logger = setup_logger()

    generated_logger.info("自動登録処理開始")
    main(generated_logger)
    generated_logger.info("自動登録処理終了")
