'''
from django.utils import timezone
from apps.textbin.models import Text
from pinax.stripe.actions import plans
from rest_framework.response import Response
from rest_framework import status


def execute_delete_expired_texts(api=False):
    now = timezone.now()
    expired_texts = Text.objects.filter(expiration_datetime__lt=now)
    if expired_texts:
        expired_texts.delete()

        return Response(
            {
                'detail': 'Deleted {0} expired texts.'.format(len(expired_texts))
            },
            status=status.HTTP_200_OK
        )


def execute_sync_plans(api=False):
    try:
        plans.sync_plans()
    except:
        return Response(
            {
                'detail': 'Internal server error.'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response(
        {
            'detail': 'Synced plans.'
        },
        status=status.HTTP_200_OK
    )
'''
