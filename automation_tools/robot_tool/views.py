from django.views.generic.base import TemplateView
from django.shortcuts import render

# Create your views here.
class AceView(TemplateView):

    template_name = "index.html"
