from datetime import datetime

from utils import (
    Mode,
    Payload,
    Platform
)


def main():
    payload = Payload(
        event_name="撃剣部",
        platform=Platform.PCAndroid,
        start_date_time=datetime(2026, 1, 15, 11, 11),
        end_date_time=datetime(2026, 1, 15, 12, 34),
        mode=Mode.Registration
    )

    print(payload.url)


if __name__ == "__main__":
    main()
