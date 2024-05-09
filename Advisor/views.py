from django.shortcuts import render

# Create your views here.
def advisor(request):
    return render(request,'advisor.html')