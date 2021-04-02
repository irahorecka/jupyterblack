import signal


def init_worker() -> None:
    signal.signal(signal.SIGINT, signal.SIG_IGN)
