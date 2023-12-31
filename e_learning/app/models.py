from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=50)
    message = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'contact'
        managed = True
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
