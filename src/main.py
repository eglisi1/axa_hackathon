from util.logger import get_logger


def main() -> None:
    """Main entry point of the app."""
    logger = get_logger(__name__)
    logger.info("Hello, world!")

if __name__ == "__main__":
    main()