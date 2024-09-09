from django.shortcuts import render

def show_main(request):
    product = {
        'name' : 'R34',
        'price': '$100,000',
        'description': 'A cool car'
    }

    return render(request, "main.html", product)