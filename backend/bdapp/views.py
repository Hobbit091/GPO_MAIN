from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import psycopg2
import json

from bdapp.models import sequence_desc
from bdapp.models import interpretation 
from bdapp.models import sequence_tb 
from bdapp.models import algorithm

def show(request): #Заглушка, чтобы загружать стартову страницу
    template = loader.get_template('index.html')
    context = {}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)

def search_sequence(request): # Вывести инфу о определенной последовательности
    oeis_id = request.GET.get('oeis_id')
    if oeis_id:
        news = sequence_desc.objects.filter(OEIS_ID=oeis_id)
        if news:
            response = HttpResponse(news)
            return response
        else:
            return HttpResponse('Error: OEIS_ID not found')
    else:
        return HttpResponse('Error')

def search_InterpSelect(request): #Получить на сколько интерпретаций селекттор и сами интепретации, чтобы вставить в селектор. На выход идет лист, из него обращаться 
    list_interp=[]
    oeis_id = request.GET.get('oeis_id')
    if oeis_id:
        news = sequence_desc.objects.filter(OEIS_ID=oeis_id)
        if news:
            m_id = news[0].M_ID
            sequence_tb_object_count = sequence_tb.objects.filter(M_ID=m_id).count()
            interpretation_modele= sequence_tb.objects.filter(M_ID=m_id)
            for i in range(0,sequence_tb_object_count):
                list_interp.append(interpretation_modele[i].Interp_ID)
            response = HttpResponse(list_interp)
            return response
        else:
            return HttpResponse('Error: OEIS_ID not found')
    else:
        return HttpResponse('Error')


def solve(request): #Выполнить код который хранится в бд
    oeis_id = request.GET.get('oeis_id')
    if oeis_id:
        news = sequence_desc.objects.filter(OEIS_ID=oeis_id)
        if news:
            m_id = news[0].M_ID
            modele= sequence_tb.objects.filter(M_ID=m_id)
            result=modele[0].Alg_ID.algorithm_code
            number_of_params = modele[0].Alg_ID.number_of_parameters
            n = 5 #Сюда вбить параметры с формы, смотря сколько их
            k = 3  
            result=exec(result, globals())
            if number_of_params == 1:
                res = resp.Start(n)
                
            if number_of_params == 2:
                res = resp.Start(n,k)
            
            if number_of_params == 3:
                res = resp.Start(n,k,m)
            
            response = HttpResponse(res)
            return response
        else:
            return HttpResponse('Error: OEIS_ID not found')
    else:
        return HttpResponse('Error')
        