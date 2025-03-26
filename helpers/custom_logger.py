import logging
from constants import ROOT_DIR

class CustomLogger(logging.Logger):
    """
    A custom logger class for managing logs with extended functionality.

    This class extends the base logging.Logger to provide preconfigured logging settings,
    including a log file handler, a custom log format
    """
    def __init__(self, logger_name: str, config: dict):
        super().__init__(logger_name, config["log_level"])

        self.log_file_path = ROOT_DIR / config["log_file_name"]
        log_dir = self.log_file_path.parent
        if not log_dir.exists():
            log_dir.mkdir()

        handler = logging.FileHandler(self.log_file_path)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-5s | %(name)s | %(filename)s | %(message)s", datefmt="%Y/%m/%d %H:%M:%S")
        handler.setFormatter(formatter)
        self.addHandler(handler)

    def add_divider(self) -> None:
        """
        Append a divider line to the log file separating log sessions for better readability.
        """
        with open(self.log_file_path, "a") as log_file:
            log_file.write("----------------------------------------------------------------------------------------\n")