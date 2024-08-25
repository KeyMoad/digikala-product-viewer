from logging import basicConfig, getLogger, INFO


# Configure logging
basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = getLogger(__name__)


def read_product_ids(file_path: str) -> list:
    """
    Reads product IDs from a file, each ID on a new line.

    Args:
        file_path (str): Path to the file containing product IDs.

    Returns:
        list: A list of product IDs.
    """
    try:
        with open(file_path, 'r') as file:
            product_ids = [line.strip() for line in file if line.strip()]
        return product_ids
    except Exception as e:
        logger.error(f"Error reading product IDs from file: {e}")
        return []
