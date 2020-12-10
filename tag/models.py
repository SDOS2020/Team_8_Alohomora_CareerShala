from django.db import models
import tagulous.models


# Create your models here.
class Tag(tagulous.models.TagTreeModel):
    class TagMeta:
        force_lowercase = True
