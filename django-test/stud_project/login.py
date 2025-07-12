import json
import logging
import random
import uuid

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)


# 自定义用户
class MyUser:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return f'MyUser(id={self.id}, username="{self.username}")'


# 自定义JWT解析
class MyJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token.get("user_id")
            username = validated_token.get("username", "匿名用户")
            password = validated_token.get("password", "默认密码")

            if not user_id:
                raise exceptions.AuthenticationFailed("token中没有user_id")

            # 构造自定义用户对象
            return MyUser(user_id, username, password)
        except Exception as e:
            raise InvalidToken(f"无效token: {str(e)}")


@csrf_exempt
@api_view(['POST'])
def custom_token_view(request):
    """
    token生成
    :param request:
    :return:
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')

        # todo 验证用户名和密码

        # 生成token
        user = MyUser(id=random.randint(1000, 9999), username=username, password=password)
        refresh = RefreshToken.for_user(user)
        return JsonResponse({'access': str(refresh.access_token), 'refresh': str(refresh)}, status=200)
    except Exception as e:
        return JsonResponse({'code': 500, 'message': str(e)}, status=500)
