from django.db import models

class Company(models.Model):
    company_name = models.CharField(max_length = 200)

    def __str__(self):
        return str(self.company_name)

    def __repr__(self):
        return ''.join(str(self.company_name).split()).lower()

class Contact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200)
    title = models.CharField(max_length = 200)
    phone = models.CharField(max_length = 200)
    email = models.EmailField()

class CompanyLocation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 200)
    state = models.CharField(max_length = 200)
    zipcode = models.IntegerField()

class ResumeBookOrderForm(models.Model):
    company = Company()
    comments = models.CharField(max_length = 5000)

class InfosessionRegistration(models.Model):
    company = Company()
    preferred_week = models.CharField(max_length = 5000)
    preferred_food = models.CharField(max_length = 5000)
    advertisements = models.CharField(max_length = 5000)
    comments = models.CharField(max_length = 5000)

class EventType(models.Model):
    event_type = models.CharField(max_length = 200)

    def __str__(self):
        return str(self.event_type)

class Event(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length = 500)
    event_type = EventType()
    food = models.CharField(max_length = 5000)
    prizes = models.CharField(max_length = 5000)
    turnout = models.IntegerField()
    company = Company()
    contact = Contact()
    officer = models.CharField(max_length = 200)
    feedback = models.CharField(max_length = 5000)
    comments = models.CharField(max_length = 5000)


class Transaction(models.Model):
    unique_text = models.CharField(max_length = 200, unique = True, primary_key = True)
    company_name = models.CharField(max_length = 200, unique = False, null = True)
    fee = models.DecimalField(max_digits = 5, decimal_places = 2)
    message = models.CharField(max_length = 5000)