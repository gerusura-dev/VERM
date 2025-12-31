from utils import EventManager
from utils import AutoSubmitter


def main():
    manager = EventManager()
    submitter = AutoSubmitter(debug=True)

    try:
        for payload in manager:
            submitter.submit(payload)
    finally:
        submitter.close()


if __name__ == "__main__":
    main()
