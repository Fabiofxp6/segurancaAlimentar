from logging import Formatter, LogRecord


class HttpStatusFormatter(Formatter):
    def format(self, record: LogRecord) -> str:
        status = getattr(record, "status_code", "-")
        return f"{record.levelname} {record.name} HTTP {status}"
