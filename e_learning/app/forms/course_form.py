from django import forms
from app.models import Chapter, Assets


class ChapterForm(forms.Form):
    name = forms.CharField(max_length=50)
    descriptions = forms.Textarea()
    youtube_link = forms.URLField()
    video = forms.FileField(upload_to="videos/")
    material = forms.ModelMultipleChoiceField(queryset=Assets.objects.all())
    is_youtube = forms.BooleanField(default=True)


class CourseForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=255)
    chapters = forms.ModelMultipleChoiceField(queryset=Chapter.objects.all())
    price = forms.IntegerField(min_value=1, max_value=100000)
    is_free = forms.BooleanField()
    likes = forms.IntegerField()
    rating = forms.IntegerField()
    poster = forms.IntegerField()
    banner = forms.IntegerField()
    category = forms.IntegerField()

class CategoryForm(forms.Form):
    name = forms.CharField(max_length=50)
    parent = forms.IntegerField(required=False)
    