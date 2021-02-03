from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework import mixins, viewsets, generics
from .serializers import *
from .models import *
import json
from django.core.serializers.json import DjangoJSONEncoder



class BoroughViewSet(viewsets.ModelViewSet):
    serializer_class = BoroughSerializer

    def get_queryset(self):
        queryset = Borough.objects.all()
        return queryset

class IndexViewSet(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'
    
    def get(self, request):
        borough = request.GET.get('borough', '')
        cyclist_injuries = CollisionLocation.objects.filter(borough__borough=borough.upper())
        citi_bikes = CitiBikeStation.objects.all()
        data = [[{'lat':x.latitude, 'lng':x.longitude} for x in cyclist_injuries],[{'lat':x.station_latitude, 'lng':x.station_longitude, 'station_id':x.station_id} for x in citi_bikes]]
        r= json.dumps(data, cls=DjangoJSONEncoder)
        return Response({'boroughs': r})