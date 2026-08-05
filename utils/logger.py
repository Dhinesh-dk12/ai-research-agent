import sys
import os

from loguru import logger


os.makedirs("logs", exist_ok=True)

logger.remove()

# Console logs
logger.add(
    sys.stdout,
    level="INFO",
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    ),
)

# File logs
logger.add(
    "logs/research_agent.log",
    level="DEBUG",
    rotation="10 MB",
    retention="30 days",
    compression="zip",

    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level} | "
        "{name}:{function}:{line} | "
        "{message}"
    ),
)