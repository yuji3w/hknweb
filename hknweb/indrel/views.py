from django.shortcuts import render
from django.views import generic
from .models import ResumeBookOrderForm, InfosessionRegistration, Transaction, Company

def index(request):
    return render(request, 'indrel/index.html')

def resume_book(request):
    return render(request, 'indrel/resume_book.html')

def infosessions(request):
    return render(request, 'indrel/infosessions.html')

def career_fair(request):
    return render(request, 'indrel/career_fair.html')

def contact_us(request):
    return render(request, 'indrel/contact_us.html')

def transaction(request):
    unique_company = request.GET.get('unique-company', 'failed')
    transaction = Transaction.objects.get(pk = unique_company)
    return render(request, 'indrel/transactions.html',
                  {'Transaction': transaction})

class ResumeBookOrderFormView(generic.DetailView):
    model = ResumeBookOrderForm
    template_name = 'indrel/resume_book_order_form.html'

class InfosessionRegistrationView(generic.DetailView):
    model = InfosessionRegistration
    template_name = 'indrel/infosessions_registration.html'

def order_resume_book(request):
    pass

def register_info_session(request):
    pass