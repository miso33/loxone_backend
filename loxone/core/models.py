from model_utils import Choices
from model_utils.models import SoftDeletableModel, StatusModel, TimeStampedModel


class BaseModel(SoftDeletableModel, TimeStampedModel, StatusModel):
    STATUS = Choices("active", "inactive")

    class Meta:
        abstract = True
