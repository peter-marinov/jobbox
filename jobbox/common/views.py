from django.shortcuts import render


def index(request):
    context = request
    return render(request, 'common/index.html')