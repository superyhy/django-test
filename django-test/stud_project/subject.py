import json
import logging

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from stud_project.login import MyJWTAuthentication
from stud_project.models import TbSubject

"""
学科相关的业务
"""
logger = logging.getLogger(__name__)


@csrf_exempt
def subject_add(request):
    """
    插入数据
    :param request:
    :return:
    """
    try:
        # 解析请求参数
        data = json.loads(request.body.decode('utf-8'))
        # 参数校验
        required_fields = ['name', 'intro', 'is_hot']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'该字段必填 {field}'}, status=400)
        # 对象构建
        subject = TbSubject(
            name=data['name'],
            intro=data['intro'],
            is_hot=int(data.get('is_hot', 0))
        )
        subject.save()

        return JsonResponse({
            'no': subject.no,
            'name': subject.name,
            'intro': subject.intro
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': ''}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def subject_query(request):
    """
    查询数据
    支持传入id进行精确查询，不传则返回全部数据
    示例请求：/subject_query?id=1
    """
    try:
        if request.method != 'GET':
            return JsonResponse({'error': '仅支持GET请求'}, status=405)

        subject_id = request.GET.get('no')  # 获取 GET 参数 id

        if subject_id:
            # 如果传了 id，进行精确查询
            try:
                subject = TbSubject.objects.get(no=subject_id)
                data = {
                    'no': subject.no,
                    'name': subject.name,
                    'intro': subject.intro,
                    'is_hot': subject.is_hot,
                }
                return JsonResponse({'data': data}, status=200)
            except TbSubject.DoesNotExist:
                return JsonResponse({'error': '未找到对应的学科'}, status=404)
        else:
            # 未传 id，查询全部
            subjects = TbSubject.objects.all()
            data = []
            for subject in subjects:
                data.append({
                    'no': subject.no,
                    'name': subject.name,
                    'intro': subject.intro,
                    'is_hot': subject.is_hot,
                })
            return JsonResponse({'data': data}, status=200, safe=False)

    except Exception as e:
        logger.error(f'查询学科失败：{str(e)}')
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def subject_delete(request):
    """
    刪除學科
    :param request:
    :return:
    """
    try:
        if request.method != 'GET':
            return JsonResponse({'code': 400, 'message': '当前仅支持GET请求'}, status=405)

        subject_no = request.GET.get('no')

        if subject_no:
            # 校验是否存在
            subject = TbSubject.objects.get(no=subject_no)
            if not subject:
                raise ObjectDoesNotExist('学科不存在')
            # 执行删除
            subject.delete()
            return JsonResponse({'code': 200, 'message': '删除成功'}, status=200)

        else:
            raise ValidationError('学科编号必填')
    except ValidationError as ve:
        return JsonResponse({'code': 500, 'message': str(ve)}, status=500)
    except Exception as e:
        logger.error(f'删除学科失败,{e}', exc_info=True)
        return JsonResponse({'code': 500, 'message': str(e)}, status=500)


@api_view(['POST'])
@authentication_classes([MyJWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
@transaction.atomic
def subject_update(request):
    '''
    更新学科
    :param request:
    :return:
    '''
    try:
        user = request.user
        if not user:
            raise ValidationError('登录失败')
        else:
            logger.info(str(user))
        # 解析请求参数
        data = json.loads(request.body.decode('utf-8'))
        # 参数校验
        required_fields = ['no', 'name', 'intro', 'is_hot']
        for field in required_fields:
            if field not in data:
                raise ValidationError(f'该参数必填，参数名={field}')
        TbSubject.objects.filter(no=data['no']).update(name=data['name'], intro=data['intro'], is_hot=data['is_hot'])
        return JsonResponse({'code': 200, 'message': '更新成功'}, status=200)
    except ValidationError as ve:
        return JsonResponse({'code': 405, 'message': str(ve)}, status=502)
    except Exception as e:
        logger.error(f'更新学科信息失败：{str(e)}', exc_info=True)
        return JsonResponse({'code': 500, 'message': str(e)}, status=500)
