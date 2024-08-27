from logging import basicConfig, getLogger, INFO


# Configure logging
basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = getLogger(__name__)


def read_file(file_path: str) -> list:
    """
    Reads file, each content on a new line.

    Args:
        file_path (str): Path to the file containing contents.

    Returns:
        list: A list of contents.
    """
    try:
        with open(file_path, 'r') as file:
            content = [line.strip() for line in file if line.strip()]
        return content
    except Exception as e:
        logger.error(f"Error reading product IDs from file: {e}")
        return []
