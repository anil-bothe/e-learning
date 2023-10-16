from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from app.models import Faqs
from app.forms.faqs_form import FAQForm


def list(request):
    msg = ''
    if request.method == "POST":
        data = request.POST
        obj = Faqs()
        forms = FAQForm(data)
        if forms.is_valid():
            obj.question = data.get("question")
            obj.answer = data.get("answer")
            obj.save()
            msg = "Sucessfully updated FAQ!"
        else:
            msg = "<br>".join([f"{key} is required" for key in forms.errors.as_data().keys()])

    faqs = Faqs.objects.all()
    return render(request, 'admin/faqs/list.html', {"faqs": faqs, "msg": msg})

def destroy(request, faq_id):
    obj = Faqs.objects.get(id=faq_id)
    obj.delete()
    return redirect("faqs-list")

def retrive_faq(request, faq_id):
    obj = Faqs.objects.get(id=faq_id)
    if request.method == "POST":
        data = request.POST
        forms = FAQForm(data)
        if forms.is_valid():
            obj.question = data.get('question')
            obj.answer = data.get('answer')
            obj.save()
        return redirect("faqs-list")
    
    d = {"id": obj.id, "question": obj.question, "answer": obj.answer}
    return JsonResponse(d)