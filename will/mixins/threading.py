import importlib
from will import settings


class ThreadingMixing:
    def bootstrap_threading(self):
        if not hasattr(self, "threading"):
            module_name = getattr(settings, "THREADING_BACKEND", "process")
            if "." not in module_name:
                module_name = "".join(["will.backends.threading.", module_name])
            threading_module = importlib.import_module(module_name)
            self.threading = threading_module.bootstrap()

    def create_process(self, target, args=(), kwargs={}):
        self.bootstrap_threading()
        return self.threading(target=target, args=args, kwargs=kwargs)
