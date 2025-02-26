from django.shortcuts import render, redirect
from .models import Profile
from .forms import ContactForm
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io


def accept(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        summary = request.POST.get("summary", "")
        degree = request.POST.get("degree", "")
        school = request.POST.get("school", "")
        university = request.POST.get("university", "")
        previous_work = request.POST.get("previous_work", "")
        skills = request.POST.get("skills", "")
        employed = request.POST.get("employed", "")
        if employed == 'on':
            employed = True
        else:
            employed = False
            profile = Profile(name=name, email=email,
                              phone=phone, summary=summary,
                              degree=degree, school=school,
                              university=university,
                              previous_work=previous_work,
                              skills=skills, employed=employed)
            profile.save()
    return render(request, 'pdf/accept.html')


def resume(request, id):
    user_profile = Profile.objects.get(pk=id)
    return render(request, 'pdf/resume.html', {'user_profile': user_profile})


def resume(request, id):
    user_profile = Profile.objects.get(pk=id)
    template = loader.get_template('pdf/resume.html')
    html = template.render({'user_profile': user_profile})
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    filename = "resume.pdf"
    return response


def list(request):
    profiles = Profile.objects.all()
    return render(request, 'pdf/list.html', {'profiles': profiles})


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = ContactForm()
        return render(request, 'contact.html', {'form': form})
