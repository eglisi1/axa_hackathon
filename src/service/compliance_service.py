from util.logger import get_logger

class AnalysisService:
    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger(__name__, config)