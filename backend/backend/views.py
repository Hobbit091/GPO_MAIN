from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render


from bdapp.models import sequence_desc
from bdapp.models import interpretation
from bdapp.models import sequence_tb 


def show(request):
    template = loader.get_template('index.html')
    context = {}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)


def search1(request):
    oeis_id = request.GET.get('oeis_id')  
    if oeis_id:
        news = sequence_desc.objects.filter(OEIS_ID=oeis_id)
    else:
        return HttpResponse('Error')
    return render(request, 'index.html', {'news': news})

def search(request):
    oeis_id = request.GET.get('oeis_id')  
    if oeis_id:
        news = sequence_desc.objects.filter(OEIS_ID=oeis_id)
        if news:
            m_id = news[0].M_ID
            sequence_tb_object_count = sequence_tb.objects.filter(M_ID=m_id).count()
            modele= sequence_tb.objects.filter(M_ID=m_id)
            # return HttpResponse(interpretation_modele[0].Interp_ID.example_image_process, content_type = 'image/jpg') вернуть изображение 
            return render(request, 'index.html', {'object': modele[0]})
        else:
            return HttpResponse('Error: OEIS_ID not found')
    else:
        return HttpResponse('Error')
    
