from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import StatisticView
from api.serializers import StatisticSerializer


def platnosci_view(request):
    pass


@api_view()
def get_statistic_view(request):
    queryset = StatisticView.objects.all()
    serializer = StatisticSerializer(queryset, many=True)
    return Response(serializer.data)
