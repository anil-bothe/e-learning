from django.db import models
from app.model.base import Base
from app.model.assets import Assets


class Chapter(Base):
    name = models.CharField(max_length=50)
    descriptions = models.TextField()
    youtube_link = models.URLField()
    video = models.FileField(upload_to="videos/")
    material = models.ManyToManyField(Assets)
    is_youtube = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'chapter'
        managed = True
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'


class CourseCategory(Base):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)


class Course(Base):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    chapters = models.ManyToManyField(Chapter)
    price = models.IntegerField()
    is_free = models.BooleanField(default=False)
    likes = models.IntegerField()
    rating = models.IntegerField()
    poster = models.ForeignKey(Assets, on_delete=models.SET_NULL, null=True, related_name="poster")
    banner = models.ForeignKey(Assets, on_delete=models.SET_NULL, null=True, related_name="banner")

    category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True)

    STATUS_BY = (
        (0, "Inactive"),
        (1, "Active"),
        (2, "Deleted"),
    )
    status = models.IntegerField(choices=STATUS_BY, default=1)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'course'
        managed = True
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

