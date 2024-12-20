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
    
def search_SeqSelect(request):  
    data = list(sequence_desc.objects.values('OEIS_ID'))  
    return JsonResponse(data, safe=False)


def alg_TableTitle(request): 
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
    interp_id = request.GET.get('interp_id')  
    if not interp_id:
        return JsonResponse({"error": "interp_id is required"}, status=400)
    
    try:
        
        sequences = sequence_tb.objects.filter(Interp_ID=interp_id)
        algorithm_ids = [seq.Alg_ID_id for seq in sequences]  

        
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
    algName = request.GET.get('algName') 
    if not algName:
        return JsonResponse({"error": "В селекторе ничего не заполнено"}, status=400)
    
    try:
        news = algorithm.objects.filter(alg_name=algName)  
        algorithms_list = [
            {
                'id': alg.Alg_ID,
                'alg_type': alg.alg_type,
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

def interp_Select(request): 
    try:
        description = request.GET.get('description')  
        news = interpretation.objects.filter(description=description)  

        if news.exists():  
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
            return JsonResponse(interpretations_list, safe=False)  
        else:
            raise Interpritation_Selector_IDNotFoundException(interpritation_id="")
    except ApplicationException as exception:
        return HttpResponseBadRequest(content=exception.message)
    
# async def solve(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             alg_id = data.get('alg_id')
#             params = data.get('params')
#             print(params)

#             news = await algorithm.objects.filter(Alg_ID=alg_id).afirst()
#             if news:
#                 result = news.alg_code
#                 number_of_params = news.number_of_parameters

#                 n, k, m = 0, 0, 0
#                 res = None

#                 async def execute_with_timeout():
#                     loop = asyncio.get_event_loop()
#                     local_scope = {}

#                     def execute_code():
#                         exec(result, globals(), local_scope)

#                     await loop.run_in_executor(None, execute_code)

#                     Start = local_scope.get("Start")
#                     if not Start:
#                         raise ValueError("Функция Start не найдена в предоставленном коде")

#                     if number_of_params == 1:
#                         n = int(params.get('param1'))
#                         return await loop.run_in_executor(None, Start, n)
#                     elif number_of_params == 2:
#                         n = int(params.get('param1'))
#                         k = int(params.get('param2'))
#                         return await loop.run_in_executor(None, Start, n, k)
#                     elif number_of_params == 3:
#                         n = int(params.get('param1'))
#                         k = int(params.get('param2'))
#                         m = int(params.get('param3'))
#                         return await loop.run_in_executor(None, Start, n, k, m)
#                     elif number_of_params == 4:
#                         n = int(params.get('param1'))
#                         k = params.get('param2')
#                         m = int(params.get('param3'))
#                         combObject = params.get('param4')
#                         return await loop.run_in_executor(None, Start, n, k, m, combObject)
                    
#                 try:
#                     res = await asyncio.wait_for(execute_with_timeout(), timeout=20)
#                 except asyncio.TimeoutError:
#                     res = 'Превышено время ожидания'
#                     return JsonResponse(res, safe=False)
                
#                 return JsonResponse(res, safe=False)
#             else:
#                 res = 'Код не найден'
#                 return JsonResponse(res, safe=False)
#         except TimeoutError as te:
#             print(str(te))
#             return JsonResponse({'error': str(te)}, status=408)
#         except Exception as e:
#             print(str(e))
#             return JsonResponse({'error': str(e)}, status=400)
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

# from functools import wraps
# import errno
# import os
# from threading import Timer

# def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
#     def decorator(func):
#         @wraps(func)
#         def _handle_timeout(*args, **kwargs):
#             def _raise_timeout():
#                 raise TimeoutError
#             timer = Timer(seconds, _raise_timeout)
#             timer.start()
#             try:
#                 result = func(*args, **kwargs)
#             finally:
#                 timer.cancel()
#             return result
#         return _handle_timeout
#     return decorator

# @timeout(20)
# def solve(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)

#             alg_id = data.get('alg_id')
#             params = data.get('params')

          
#             news = algorithm.objects.filter(Alg_ID = alg_id)
#             if news: 
#                 result = news[0].alg_code
#                 number_of_params = news[0].number_of_parameters
#                 n=0
#                 k=0
#                 m=0
#                 res=None
#                 exec(result, globals())
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
#             res = 'Превышено время ожидания вычисления, возможно, вы поставили слишком большие значения параметров'
#             return JsonResponse(res, safe=False)
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
import asyncio
from django.http import JsonResponse
from asgiref.sync import sync_to_async
import json

async def execute_with_timeout(code, params, number_of_params, alg_type):
    try:
        globals_dict = globals()
        exec(code, globals_dict)  

        n = int(params.get('param1')) if params.get('param1') else None
        k = int(params.get('param2')) if params.get('param2') else None
        m = int(params.get('param3')) if params.get('param3') else None
        combObject = params.get('combObject') if params.get('combObject') else None
        rank = int(params.get('Rank')) if params.get('Rank') else None
        print(alg_type)
        if alg_type == 'Listing':
            if number_of_params == 1:
                result = await asyncio.to_thread(globals_dict['Start'], n)
            elif number_of_params == 2:
                result = await asyncio.to_thread(globals_dict['Start'], n, k)
            elif number_of_params == 3:
                result = await asyncio.to_thread(globals_dict['Start'], n, k, m)
        elif alg_type == 'Rank':
            if number_of_params == 1:
                result = await asyncio.to_thread(globals_dict['Start'], n, combObject)
            elif number_of_params == 2:
                result = await asyncio.to_thread(globals_dict['Start'], n, k, combObject)
            elif number_of_params == 3:
                result = await asyncio.to_thread(globals_dict['Start'], n, k, m, combObject)
        elif alg_type == 'Unrank':
            if number_of_params == 1:
                result = await asyncio.to_thread(globals_dict['Start'], n, rank)
            elif number_of_params == 2:
                result = await asyncio.to_thread(globals_dict['Start'], n, k, rank)
            elif number_of_params == 3:
                result = await asyncio.to_thread(globals_dict['Start'], n, k, m, rank)
        else:
            result = 'Некорректное количество параметров'
        return result
    except Exception as e:
        return f"Ошибка выполнения: {str(e)}"


async def solve(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            alg_id = data.get('alg_id')
            params = data.get('params')
            
            news = await sync_to_async(list)(algorithm.objects.filter(Alg_ID=alg_id))
            if news:
                alg_code = news[0].alg_code
                number_of_params = news[0].number_of_parameters
                alg_type = news[0].alg_type
                try:
                    result = await asyncio.wait_for(
                        execute_with_timeout(alg_code, params, number_of_params, alg_type),
                        timeout=20
                    )
                    return JsonResponse(result, safe=False)
                except asyncio.TimeoutError:
                    return JsonResponse(
                        'Превышено время ожидания вычисления. Попробуйте уменьшить параметры.',
                        safe=False,
                    )
            else:
                return JsonResponse('Код не найден', safe=False)
        except Exception as e:
            return JsonResponse(
                f"Произошла ошибка: {str(e)}", safe=False, status=500
            )
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


def main_view(request):
    return render(request, 'main.html')
