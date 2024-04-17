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
    n = 5  # Общее количество элементов
    k = 3  # Размер комбинации
    oeis_id = request.GET.get('oeis_id')
    if oeis_id:
        news = sequence_desc.objects.filter(OEIS_ID=oeis_id)
        if news:
            m_id = news[0].M_ID
            sequence_tb_object_count = sequence_tb.objects.filter(M_ID=m_id).count()
            modele= sequence_tb.objects.filter(M_ID=m_id)
            # return HttpResponse(interpretation_modele[0].Interp_ID.example_image_process, content_type = 'image/jpg') вернуть изображение 
            result=modele[0].Alg_ID.algorithm_code
            n = 5  # Общее количество элементов
            k = 3  # Размер комбинации
            result=exec(result, globals())
            combination_generator = CombinationColex(n, k)
            res=combination_generator.Start()
            response = HttpResponse(res[0])
            return response
            #return HttpResponse(modele[0].Interp_ID.example_image_process, content_type = 'image/jpg') 
            #return HttpResponse(modele[0].Alg_ID.algorithm_code)
            #return render(request, 'index.html', {'object': modele[0]})
        else:
            return HttpResponse('Error: OEIS_ID not found')
    else:
        return HttpResponse('Error')

def solve(request):
    oeis_id = request.GET.get('oeis_id')
    news = sequence_desc.objects.filter(OEIS_ID=oeis_id)
    m_id = news[0].M_ID
    sequence_tb_object_count = sequence_tb.objects.filter(M_ID=m_id).count()
    modele= sequence_tb.objects.filter(M_ID=m_id)
    # return HttpResponse(interpretation_modele[0].Interp_ID.example_image_process, content_type = 'image/jpg') вернуть изображение 
    result=modele[0].Alg_ID.algorithm_code
    number_of_params = modele[0].Alg_ID.number_of_parameters
    n = 5 
    k = 3  
    result=exec(result, globals())
    #combination_generator = CombinationColex(n, k)
    #resp = CombinationColex()
    if number_of_params == 1:
        res = resp.Start(n)
        
    if number_of_params == 2:
        res = resp.Start(n,k)
      
    if number_of_params == 3:
        res = resp.Start(n,k,m)
    
    response = HttpResponse(res)
    return response
    