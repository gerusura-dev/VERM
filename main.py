from logging import Logger
from Utils import EventManager, get_logger
from VRCAPI import LoginRequest
from GoogleForms import FormsRequest


def main(logger: Logger):
    manager = EventManager()
    forms = FormsRequest(test=True)
    api = LoginRequest()

    for payload in manager:
        logger.info("VRCイベントカレンダー登録開始")
        forms.submit(payload)
        logger.info("VRCイベントカレンダー登録完了")

    for payload in manager:
        logger.info("VRC内カレンダー登録開始")
        api.submit(payload)
        logger.info("VRC内カレンダー登録完了")

    forms.close()


if __name__ == "__main__":
    generated_logger = get_logger()

    generated_logger.info("自動登録処理開始")
    main(generated_logger)
    generated_logger.info("自動登録処理終了")
