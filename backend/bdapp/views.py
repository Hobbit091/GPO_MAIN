from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import psycopg2
import json

from bdapp.exceptions.ALG import AlgIsNotFoundException
from bdapp.exceptions.Interpritation_Selector_ID import Interpritation_Selector_IDNotFoundException
from bdapp.exceptions.OEISID import OEIS_IDNotFoundException
from bdapp.exceptions.base import ApplicationException
from bdapp.models import sequence_desc
from bdapp.models import interpretation 
from bdapp.models import sequence_tb 
from bdapp.models import algorithm
from django.http import HttpResponseBadRequest


def show(request): #Заглушка, чтобы загружать стартову страницу
    template = loader.get_template('index.html')
    context = {}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)

def search_sequence(request): # Вывести инфу о определенной последовательности
    try:
        oeis_id = request.GET.get('oeis_id')
        news = sequence_desc.objects.filter(OEIS_ID=oeis_id)
        if news:            
            response = HttpResponse(news)
            return response
        else:
            raise OEIS_IDNotFoundException(oeis_id=oeis_id)
    except ApplicationException as exception:
       return HttpResponseBadRequest(content=exception.message)
    # if oeis_id:
    #     news = sequence_desc.objects.filter(OEIS_ID=oeis_id)
    #     if news:
    #         response = HttpResponse(news)
    #         return response
    #     else:
    #         return HttpResponse('Error: OEIS_ID not found')
    # else:
    #     return HttpResponse('Error')

def search_InterpSelect(request): #Получить на сколько интерпретаций селекттор и сами интепретации, чтобы вставить в селектор. На выход идет лист, из него обращаться 
    try:
        list_interp=[]
        oeis_id = request.GET.get('oeis_id')
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
            raise OEIS_IDNotFoundException(oeis_id=oeis_id)
    except ApplicationException as exception:
        return HttpResponseBadRequest(content=exception.message)
    # list_interp=[]
    # oeis_id = request.GET.get('oeis_id')
    # if oeis_id:
    #     news = sequence_desc.objects.filter(OEIS_ID=oeis_id)
    #     if news:
    #         m_id = news[0].M_ID
    #         sequence_tb_object_count = sequence_tb.objects.filter(M_ID=m_id).count()
    #         interpretation_modele= sequence_tb.objects.filter(M_ID=m_id)
    #         for i in range(0,sequence_tb_object_count):
    #             list_interp.append(interpretation_modele[i].Interp_ID)
    #         response = HttpResponse(list_interp)
    #         return response
    #     else:
    #         return HttpResponse('Error: OEIS_ID not found')
    # else:
    #     return HttpResponse('Error')

def search_SeqSelect(request): #Получить список последовательностей объектом, дальше параметрами можно вытягивать все что угодно 
    news=[]
    news = sequence_desc.objects.all()
    response = HttpResponse(news)
    return response

def alg_TableTitle(request): #Получить списком то какие поля будут у таблицы
    try:
        alg_name = request.GET.get('alg_name')
        news = algorithm.objects.filter(alg_name=alg_name)
        if news:
            response=HttpResponse(news[0].alg_table_title.split(","))
            return response
        raise AlgIsNotFoundException(alg_name=alg_name)
    except ApplicationException as exception:
        return HttpResponseBadRequest(content=exception.message)
    # if alg_name:
    #     news = algorithm.objects.filter(alg_name=alg_name)
    #     if news:
    #         response=HttpResponse(news[0].alg_table_title.split(","))
    #         return response
    #     else:
    #         return HttpResponse('Error: Alg not found')
    # else:
    #     return HttpResponse('Error')


def interp_Select(request): #Получить интепретацию по ID, которое будет взято из селектора
    try:
        interp_id = request.GET.get('interp_id')
        news = interpretation.objects.filter(Interp_id=interp_id)
        if news:
            return HttpResponse(news)
        else:
            raise Interpritation_Selector_IDNotFoundException()
    except ApplicationException as exception:
        return HttpResponseBadRequest(content=exception.message)
    # if interp_id:
    #     news = interpretation.objects.filter(Interp_ID=interp_id)
    #     if news:
    #         return HttpResponse(news)
    #     else:
    #         return HttpResponse('Error: Interpretation not found')
    # else:
    #     return HttpResponse('Error')

def solve(request): 
    try:
        oeis_id = request.GET.get('oeis_id')
        news = sequence_desc.objects.filter(OEIS_ID=oeis_id)
        if news:
            m_id = news[0].M_ID
            modele= sequence_tb.objects.filter(M_ID=m_id)
            result=modele[0].Alg_ID.algorithm_code
            number_of_params = modele[0].Alg_ID.number_of_parameters
            n = 5 #Сюда вбить параметры с формы, смотря сколько их
            k = 3  
            m= 4
            result=exec(result, globals())
            if number_of_params == 1:
                res = result.Start(n)
               
            if number_of_params == 2:
                res = result.Start(n,k)
            
            if number_of_params == 3:
                res = result.Start(n,k,m)
            
            response = HttpResponse(res)
            return response
        else:
            raise OEIS_IDNotFoundException(oeis_id=oeis_id)
    except ApplicationException as exception:
        return HttpResponseBadRequest(content=exception.message)
    

def main_view(request):
    return render(request, 'main.html')
    
  