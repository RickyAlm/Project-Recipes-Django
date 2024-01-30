from django.shortcuts import render


def forms(request):
    return render(request, 'authors/pages/home.html')
