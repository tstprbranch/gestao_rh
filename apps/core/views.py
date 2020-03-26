from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db.models import Sum

from rest_framework import viewsets
from rest_framework import permissions
from apps.core.serializers import UserSerializer, GroupSerializer

from apps.registro_hora_extra.models import RegistroHoraExtra
from apps.empresa.models import Empresa



@login_required
def home(request):
    data = {}
    data['usuario'] = request.user
    funcionario = request.user.funcionario
    data['total_funcionarios'] = funcionario.empresa.total_funcionarios
    data['total_funcionarios_ferias'] = funcionario.empresa.total_funcionarios_ferias
    data['total_funcionarios_doc_pendente'] = funcionario.empresa.total_funcionarios_doc_pendente
    data['total_funcionarios_doc_ok'] = funcionario.empresa.total_funcionarios_doc_ok
    data['total_funcionarios_rg'] = 10
    data['total_hora_extra_utlizadas'] = RegistroHoraExtra.objects.filter(
    	funcionario__empresa=funcionario.empresa, utilizada=True).aggregate(Sum('horas'))['horas__sum']
    data['total_hora_extra_pendente'] = RegistroHoraExtra.objects.filter(
    	funcionario__empresa=funcionario.empresa, utilizada=False).aggregate(Sum('horas'))['horas__sum']

    return render(request, 'core/index.html', data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]