from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'name': 'Rhaken Shaquille Akbar Yanuanda',
        'class' : 'PBP B',
        'description' : 'saya suka tidur :V',
    }

    return render(request, "main.html", context)