from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from core.models import User, Job, Application
from .serializers import JobSerializer

# Create your views here.
@api_view(['GET'])
def homeView(request):
    return Response("Hello Zecpath Backend")

class JobView(APIView):
    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many = True)
        return Response(serializer.data)

class JobCreateView(APIView):
    def post(self, request):
        serializer = JobSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer._errors)
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)