from logging import basicConfig, getLogger, INFO

# Configure logging
basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = getLogger(__name__)
