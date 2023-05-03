from django.db import models
from django.forms import fields
from .models import predictionModel1
from django import forms

class PredictionForm1(forms.ModelForm):
    class Meta:
        # To specify the model to be used to create form
        model = predictionModel1
        # It includes all the fields of model
        fields = '__all__'