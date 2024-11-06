from django.http import HttpResponse
from django.http import JsonResponse

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



def search_sequence(request): 
    try:
        list_seq = []
        oeis_id = request.GET.get('oeis_id')
        news = sequence_desc.objects.filter(OEIS_ID=oeis_id).first()
        if news:
            list_seq.append({
                'id': news.OEIS_ID,  
                'name': news.special_title,  
                'number_of_parameters': news.number_of_parameters,  
                'explicit_formula_latex': news.explicit_formula_latex,  
                'recurrent_formula': news.recurrent_formula,  
                'recurrent_formula_latex': news.recurrent_formula_latex,  
                'other_formula_latex': news.other_formula_latex,  
                'generating_function_latex': news.generating_function_latex,  
               })
            return JsonResponse(list_seq, safe=False)
        else:
            raise OEIS_IDNotFoundException(oeis_id=oeis_id)

    except ApplicationException as exception:
        return HttpResponseBadRequest(content=exception.message)

def search_InterpSelect(request): 
    try:
        list_interp = []
        oeis_id = request.GET.get('oeis_id')
        news = sequence_desc.objects.filter(OEIS_ID=oeis_id)

        if news:
            m_id = news[0].M_ID
            sequence_records = sequence_tb.objects.filter(M_ID=m_id)

            for record in sequence_records:
                interpretation_instance = record.Interp_ID
                list_interp.append({
                    'id': interpretation_instance.Interp_ID,  # ID интерпретации
                    'n_value': interpretation_instance.n_value,  # Описание
                    'desc': interpretation_instance.description,  # Описание
                    'example_table': interpretation_instance.example_table,
                    'example_text': interpretation_instance.example_text,  # Описание
                    #'example_image': interpretation_instance.example_image,  # Описание
                    #'example_image_process': interpretation_instance.example_image_process,  # Описание
                })
            return JsonResponse(list_interp, safe=False)
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


def interp_Select(request):  # Получить интерпретацию по description
    try:
        description = request.GET.get('description')  # Получаем description из GET-запроса
        news = interpretation.objects.filter(description=description)  # Фильтруем по description

        if news.exists():  # Проверяем, есть ли результаты
            # Преобразуем результаты в список словарей
            interpretations_list = [
                {
                    'id': interp.Interp_ID,
                    'n_value': interp.n_value,
                    'description': interp.description,
                    'example_text': interp.example_text,
                    # Добавьте другие поля, которые хотите вернуть
                }
                for interp in news
            ]
            return JsonResponse(interpretations_list, safe=False)  # Возвращаем данные в формате JSON
        else:
            raise Interpritation_Selector_IDNotFoundException(interpritation_id="")
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