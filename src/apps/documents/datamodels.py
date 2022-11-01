from typing import Any

from src.common.datamodels import DataModel


class CreateDocumentInput(DataModel):
    """Input datamodel definition for creation of model `Document`."""

    folder: str
    data: Any
