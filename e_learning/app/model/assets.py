from django.db import models


class Assets(models.Model):
    file = models.FileField(upload_to="assets/")

    class Meta:
        db_table = 'assets'
        managed = True
        verbose_name = 'Assets'
        verbose_name_plural = 'Assetss'
