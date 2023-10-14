from django.shortcuts import render, redirect
from app.models import Faqs


def list(request):
    if request.method == "POST":
        data = request.POST
        obj = Faqs()
        obj.question = data.get("question")
        obj.answer = data.get("answer")
        obj.save()

    faqs = Faqs.objects.all()
    return render(request, 'admin/faqs/list.html', {"faqs": faqs})

def destroy(request, faq_id):
    obj = Faqs.objects.get(id=faq_id)
    obj.delete()
    return redirect("faqs-list")