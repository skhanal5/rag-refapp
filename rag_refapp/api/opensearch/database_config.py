class DatabaseConfig:

    # turn to factory method
    def __init__(
        self,
        hostname: str,
        port: int,
        auth: tuple,
        ssl_flag: bool,
        verify_cert_flag: bool,
        ssl_show_warn: bool,
    ):
        self.hostname = hostname
        self.port = port
        self.auth = auth
        self.ssl_flag = ssl_flag
        self.verify_cert_flag = verify_cert_flag
        self.ssl_show_warn = ssl_show_warn
