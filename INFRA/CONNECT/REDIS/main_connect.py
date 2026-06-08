from INFRA.CONNECT.REDIS.connect import app
from INFRA.CORE.config import Settings_Redis
def main_redis():
    return app(backend=Settings_Redis().backend(), broker=Settings_Redis().broker())