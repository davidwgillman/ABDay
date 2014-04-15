from django.db import models

# Create your models here.
class Patient(models.Model):
	name = models.CharField('Last, First', max_length=200)
	dob = models.DateField('Date of Birth')
	timeIn = models.DateTimeField('Time In')
	timeOut = models.DateTimeField('Time Out')

class Practitioner(models.Model):
	name = models.CharField('Last, First', max_length=200)

class Step(models.Model):
	number = models.IntegerField('Step Number')
	patient = models.ForeignKey(Patient)
	start = models.DateTimeField('Start Time')
	end = models.DateTimeField('End Time')

class Outcome(models.Model):
	step = models.ForeignKey(Step)
	key = models.CharField('Outcome Name', max_length=25)
	value = models.CharField('Outcome Value', max_length=25)


