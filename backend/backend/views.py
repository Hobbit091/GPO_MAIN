from django.http import HttpResponse
from django.template import loader
from bdapp.models import sequence_desc
from django.shortcuts import render
from bdapp.models import interpretation
from bdapp.models import sequence_tb 

def show(request):
    template = loader.get_template('index.html')
    context = {}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)

def search(request):
    oeis_id = request.GET.get('oeis_id')  
    if oeis_id:
        news = sequence_desc.objects.filter(OEIS_ID=oeis_id)
    else:
        return HttpResponse('Error')
    # return HttpResponse(sequence_desc.objects.filter(OEIS_ID=str(oeis_id)))
    return render(request, 'index.html', {'news': news})