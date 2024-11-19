from django.http import HttpResponse
from django.http import JsonResponse

from django.template import loader
from django.shortcuts import render
import psycopg2
import json

from bdapp.exceptions.ALG import AlgIsNotFoundException
from bdapp.exceptions.SolveException import SolveException
from bdapp.exceptions.Interpritation_Selector_ID import Interpritation_Selector_IDNotFoundException
from bdapp.exceptions.OEISID import OEIS_IDNotFoundException
from bdapp.exceptions.base import ApplicationException
from bdapp.models import sequence_desc
from bdapp.models import interpretation 
from bdapp.models import sequence_tb 
from bdapp.models import algorithm
from django.http import HttpResponseBadRequest
from threading import Timer
import asyncio


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
    data = list(sequence_desc.objects.values('OEIS_ID'))  
    return JsonResponse(data, safe=False)


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


async def solve(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            alg_id = data.get('alg_id')
            params = data.get('params')
            print(params)

            news = await algorithm.objects.filter(Alg_ID=alg_id).afirst()
            if news:
                result = news.alg_code
                number_of_params = news.number_of_parameters

                n, k, m = 0, 0, 0
                res = None

                async def execute_with_timeout():
                    loop = asyncio.get_event_loop()
                    local_scope = {}

                    def execute_code():
                        exec(result, globals(), local_scope)

                    await loop.run_in_executor(None, execute_code)

                    Start = local_scope.get("Start")
                    if not Start:
                        raise ValueError("Функция Start не найдена в предоставленном коде")

                    if number_of_params == 1:
                        n = int(params.get('param1'))
                        return await loop.run_in_executor(None, Start, n)
                    elif number_of_params == 2:
                        n = int(params.get('param1'))
                        k = int(params.get('param2'))
                        return await loop.run_in_executor(None, Start, n, k)
                    elif number_of_params == 3:
                        n = int(params.get('param1'))
                        k = int(params.get('param2'))
                        m = int(params.get('param3'))
                        return await loop.run_in_executor(None, Start, n, k, m)
                    elif number_of_params == 4:
                        n = int(params.get('param1'))
                        k = params.get('param2')
                        m = int(params.get('param3'))
                        combObject = params.get('param4')
                        return await loop.run_in_executor(None, Start, n, k, m, combObject)
                    
                try:
                    res = await asyncio.wait_for(execute_with_timeout(), timeout=20)
                except asyncio.TimeoutError:
                    res = 'Превышено время ожидания'
                    return JsonResponse(res, safe=False)
                
                return JsonResponse(res, safe=False)
            else:
                res = 'Код не найден'
                return JsonResponse(res, safe=False)
        except TimeoutError as te:
            print(str(te))
            return JsonResponse({'error': str(te)}, status=408)
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

# def solve(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)

#             alg_id = data.get('alg_id')
#             params = data.get('params')
#             print(params)
          
#             news = algorithm.objects.filter(Alg_ID = alg_id)
#             if news: 
#                 result = news[0].alg_code
#                 number_of_params = news[0].number_of_parameters
#                 n=0
#                 k=0
#                 m=0
#                 res=None
#                 exec(result, globals())
#                 print(number_of_params)
#                 if number_of_params == 1:
#                     n = int(params.get('param1'))
#                     res = Start(n)
#                 elif number_of_params == 2:
#                     n = int(params.get('param1'))
#                     k = int(params.get('param2'))
#                     res = Start(n, k)
#                 elif number_of_params == 3:
#                     n = int(params.get('param1'))
#                     k = int(params.get('param2'))
#                     m = int(params.get('param3'))
#                     res = Start(n, k, m)
#                 elif number_of_params == 4:
#                     n = int(params.get('param1'))
#                     k = (params.get('param2'))
#                     m = int(params.get('param3'))
#                     combObject = params.get('param4')
#                     res = Start(n, k, m, combObject)
#                 return JsonResponse(res, safe=False)
#             else: 
#                 res = 'Код не найден'
#                 return JsonResponse(res, safe=False)
#         except Exception as e:
#             print(str(e))
#             return JsonResponse({'error': str(e)}, status=400)
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
def main_view(request):
    return render(request, 'main.html')
