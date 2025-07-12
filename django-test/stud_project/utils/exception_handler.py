import logging

from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    自定义异常处理器，返回统一格式 JSON
    """
    # 默认处理（处理 DRF 内置异常：如权限失败、认证失败、请求方法错误等）
    response = exception_handler(exc, context)

    if response is not None:
        # 可根据异常类型调整 message 内容
        detail = response.data.get('detail', str(exc))
        logger.warning(f"捕获DRF异常：{str(exc)}")
        return Response({
            'code': response.status_code,
            'message': detail,
        }, status=response.status_code)
    else:
        # 非 DRF 异常（如代码中的普通 Python 异常）
        logger.error(f"捕获未处理异常：{str(exc)}", exc_info=True)
        return Response({
            'code': 500,
            'message': '服务器内部错误，请联系管理员',
            'error': str(exc)
        }, status=500)
