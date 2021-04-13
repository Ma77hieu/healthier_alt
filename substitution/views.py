from django.shortcuts import render


def results(request):
    return render(request, 'results.html')


def details(request):
    return render(request, 'detailprod.html')
