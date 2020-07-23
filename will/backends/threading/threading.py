from threading import Thread as _Thread


# XXX: maybe has better way to terminate thread
class Thread(_Thread):
    def terminate(self):
        self._terminate = True

    def is_alive(self):
        return (
            not (hasattr(self, "_terminate") and self._terminate) and super().is_alive()
        )


def bootstrap():
    return Thread
