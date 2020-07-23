import importlib
import logging
import dill as pickle
import functools
from will import settings


class PubSubMixin(object):

    def bootstrap_pubsub(self):
        pass

    @property
    def pubsub(self):
        if hasattr(self, "_pubsub") and self._pubsub is not None:
            return self._pubsub
        module_name = ''.join([
            'will.backends.pubsub.',
            getattr(settings, 'PUBSUB_BACKEND', 'redis'),
            '_pubsub'
        ])
        pubsub_module = importlib.import_module(module_name)

        # Now create our pubsub object using the bootstrap function
        # from within the import
        self._pubsub = pubsub_module.bootstrap(settings)
        return self._pubsub

    def subscribe(self, topic):
        self.bootstrap_pubsub()
        try:
            return self.pubsub.subscribe(topic)
        except Exception:
            logging.exception("Unable to subscribe to %s", topic)

    def publish(self, topic, obj):
        self.bootstrap_pubsub()
        try:
            return self.pubsub.publish(topic, obj)
        except Exception:
            logging.exception("Unable to publish %s to %s", (obj, topic))

    def unsubscribe(self, topic):
        self.bootstrap_pubsub()
        try:
            return self.pubsub.unsubscribe(topic)
        except Exception:
            logging.exception("Unable to unsubscribe to %s", topic)
