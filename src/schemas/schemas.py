from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class ImageDataCreate:
    file_name: str
    file_path: str
    file_extension: str
    file_size: float
    description: Optional[str] = None


@dataclass
class ProcessedImageDataCreate:
    file_name: str
    file_path: str
    processed_at: datetime
