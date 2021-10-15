import sys

from containers import Container


class StartUp:
    container = Container()
    container.config.mongodb_url.from_env("TIKA_URL")
    container.config.tika_server.from_env("MONGO_CONNECTION")
    container.wire(modules=[sys.modules[__name__]])