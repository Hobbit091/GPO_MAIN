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
                    'desc': interpretation_instance.description,  # Описание
                })
            return JsonResponse(list_interp, safe=False)
        else:
            raise OEIS_IDNotFoundException(oeis_id=oeis_id)

    except ApplicationException as exception:
        return HttpResponseBadRequest(content=exception.message)
    

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


def alg_Select(request):
    interp_id = request.GET.get('interp_id')  # Получаем ID интерпретации из запроса
    if not interp_id:
        return JsonResponse({"error": "interp_id is required"}, status=400)
    
    try:
        # Находим все записи sequence_tb, связанные с выбранной интерпретацией
        sequences = sequence_tb.objects.filter(Interp_ID=interp_id)
        algorithm_ids = [seq.Alg_ID_id for seq in sequences]  # Получаем список Alg_ID для связанных записей

        # Получаем алгоритмы из модели algorithm по Alg_ID
        algorithms = algorithm.objects.filter(Alg_ID__in=algorithm_ids)
        algorithms_data = [
            {
                'id': alg.Alg_ID,
                'name': alg.alg_name,
            }
            for alg in algorithms
        ]

        return JsonResponse(algorithms_data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def alg_SelectDetails(request):
    algName = request.GET.get('algName')  # Получаем ID интерпретации из запроса
    if not algName:
        return JsonResponse({"error": "В селекторе ничего не заполнено"}, status=400)
    
    try:
        news = algorithm.objects.filter(alg_name=algName)  # Фильтруем по description
        algorithms_list = [
            {
                'id': alg.Alg_ID,
                'name': alg.alg_name,
                'number_of_parameters': alg.number_of_parameters,
                'name_param': alg.parameters_name,
                'field1': alg.field1_name,
                'field1_d': alg.field1_desc,
                'field2': alg.field2_name,
                'field2_d': alg.field2_desc,
                'field3': alg.field3_name,
                'field3_d': alg.tree_structure_process.url,
                'field4': alg.field4_name,
                'field4_d': alg.field4_desc,
                'field5': alg.field5_name,
                'field5_d': alg.field5_desc,
                'alg_code ': alg.alg_code,
            }
            for alg in news
        ]

        return JsonResponse(algorithms_list, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)   

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
                    'example_table': interp.example_table,  # Описание
                    'example_image': interp.example_image_process.url,
                }
                for interp in news
            ]
            return JsonResponse(interpretations_list, safe=False)  # Возвращаем данные в формате JSON
        else:
            raise Interpritation_Selector_IDNotFoundException(interpritation_id="")
    except ApplicationException as exception:
        return HttpResponseBadRequest(content=exception.message)


def solve(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
           
            alg_id = data.get('alg_id')
            params = data.get('params')
            print(params)
          
          
            news = sequence_tb.objects.filter(Alg_ID = alg_id)
            
            if news:
                m_id = news[0].M_ID
                modele = sequence_tb.objects.filter(M_ID=m_id)

                result = modele[0].Alg_ID.alg_code

                number_of_params = modele[0].Alg_ID.number_of_parameters
 
                if number_of_params == 1:
                    # res = result.Start(n)
                    n = params.get('param1')
                    exec(result, globals())
                    # res = result.Start(n)
                elif number_of_params == 2:
                    # res = result.Start(n,k)
                    # n = params.get('param1')
                    # k = params.get('param2')
                    # print(n,k)
                    # exec(f"n = {n} \nk={k}\n"+result)  # Выполняем код алгоритма
                    # print('не гавно')
                    # print(res)
                    # res = result.Start(n,k)
                    n = params.get('param1')
                    k = params.get('param2')
                    print(n,k)
                    exec(result)  # Выполняем код алгоритма
                    
                    print('не гавно')
                    

                elif number_of_params == 3:
                    # res = result.Start(params[0], params[1], params[2])
                    n= params.get('param1')
                    k= params.get('param2')
                    m = params.get('param3')
                    exec(result, globals())  # Выполняем код алгоритма
                    # res = result.Start(n,k,m)
                return JsonResponse({'output': 'йоу'})
            else: 
                print('гавно')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

    
def main_view(request):
    return render(request, 'main.html')
