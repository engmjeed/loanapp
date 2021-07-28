from django.core.cache import cache


from factory.uri import uri


class WalletLock(object):
    def __init__(self, wallet, *, timeout=None, expire=None, sleep=None):
        self.wallet = wallet
        timeout = 10 if timeout is None else timeout
        sleep = 0.25 if sleep is None else sleep
        self.lock = cache.lock(
            self.key, timeout=expire, blocking_timeout=timeout, sleep=sleep
        )

    @property
    def key(self):
        try:
            return self.__dict__["key"]
        except KeyError:
            rv = self.__dict__["key"] = uri(
                "wallet",
                self.wallet.__class__.__name__,
                str(self.wallet.user.id),
                str(self.wallet.id),
            )
            return rv

    def locked(self):
        return self.lock.locked()

    def __enter__(self):
        if self.lock.acquire(blocking=True):
            return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.lock.release()
