class AppContext:
    def __init__(self):
        self.m_yml_cfg = None
        self.m_redis_client = None
        self.m_mysql_client = None


app_context = AppContext()