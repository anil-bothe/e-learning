from django.db import models
from app.model.base import Base


class Faqs(Base):
    question = models.CharField(max_length=50)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question

    class Meta:
        db_table = 'faqs'
        managed = True
        verbose_name = 'Faqs'
        verbose_name_plural = 'Faqs'
