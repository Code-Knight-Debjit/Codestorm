from django.shortcuts import render
from datetime import date

# Create your views here.
def home(request):
    return render(request, 'MarketPulse/index.html')