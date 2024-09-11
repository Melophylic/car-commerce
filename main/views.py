from django.shortcuts import render

def show_main(request):
    product = {
        'name' : 'R34',
        'price': '$100,000',
        'description': 'A cool car',
        'nama' : 'Muhammad Nadzim Tahara',
        'npm' : '2306275430',
        'kelas' : 'PBP C 2024'
    }
    return render(request, "main.html", product)

# def show_me(request):
#     myself = {
#         'nama' : 'Muhammad Nadzim Tahara',
#         'npm' : '2306275430',
#         'kelas' : 'PBP C 2024'
#     }
#     return render(request, "main.html", myself)