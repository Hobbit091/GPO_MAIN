from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import psycopg2
import json

from bdapp.models import sequence_desc
from bdapp.models import interpretation
from bdapp.models import sequence_tb 
from bdapp.models import algorithm


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
    number=5
    oeis_id = request.GET.get('oeis_id')  
    if oeis_id:
        news = sequence_desc.objects.filter(OEIS_ID=oeis_id)
        if news:
            m_id = news[0].M_ID
            sequence_tb_object_count = sequence_tb.objects.filter(M_ID=m_id).count()
            modele= sequence_tb.objects.filter(M_ID=m_id)
            # return HttpResponse(interpretation_modele[0].Interp_ID.example_image_process, content_type = 'image/jpg') вернуть изображение 

            result=modele[0].Alg_ID.algorithm_code
            # json_data = {"number": number}
            # result = exec(code, json_data)
            # json_data = json.dumps(result)
            # response = HttpResponse(json_data, content_type="application/json")
            result=exec(result, globals())

            result=factorial(5)

            response = HttpResponse(result)
            return response
        
            # return HttpResponse(modele[0].Alg_ID.algorithm_code)
            # return render(request, 'index.html', {'object': modele[0]})
        else:
            return HttpResponse('Error: OEIS_ID not found')
    else:
        return HttpResponse('Error')
    
