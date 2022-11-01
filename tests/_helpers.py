from typing import Type

from factory import Factory

from src.common.datamodels import DataModel


class DataModelTestBase:
    """Base test template for models."""

    datamodel_cls: Type[DataModel]
    factory_cls: Type[Factory]

    # ======================================================================
    # Basic tests
    # ======================================================================
    def test_instance_creation(self) -> None:
        """Test model instance can be created normally."""
        instance = self.factory_cls.create()
        assert isinstance(instance, self.datamodel_cls)
