from django.shortcuts import redirect


def redirect_blog(request):
    return redirect('index_page_url', permanent=False)
