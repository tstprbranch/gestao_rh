import json
import csv
import xlwt

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.models import User

from .models import RegistroHoraExtra
from .forms import RegistroHoraExtraForm
from django.views.generic import (
    ListView,
    UpdateView,
    DeleteView,
    CreateView
)


class HoraExtraList(ListView):
    model = RegistroHoraExtra

    def get_queryset(self):
        empresa_logada = self.request.user.funcionario.empresa
        return RegistroHoraExtra.objects.filter(funcionario__empresa=empresa_logada)


class HoraExtraEdit(UpdateView):
    model = RegistroHoraExtra
    form_class = RegistroHoraExtraForm


class HoraExtraDelete(DeleteView):
    model = RegistroHoraExtra
    success_url = reverse_lazy('list_hora_extra')

class HoraExtraNovo(CreateView):
    model = RegistroHoraExtra
    form_class = RegistroHoraExtraForm

    def get_form_kwargs(self):
        kwargs = super(HoraExtraNovo, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

class UtilizouHoraExtra(View):
    def post(self, *args, **kwargs):
        

        registro_hora_extra = RegistroHoraExtra.objects.get(id=kwargs['pk'])
        registro_hora_extra.utilizada = True
        registro_hora_extra.save()

        response = json.dumps(
            {'mensagem': 'Requisicao executada', 
            'horas': float(empregado.total_horas_extra)})
        
        return HttpResponse(response, content_type='application/json')

class ExportarParaCSV(View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename"'

        registro_he = RegistroHoraExtra.objects.filter(utilizada=False)

        writer = csv.writer(response)
        writer.writerow(['id', 'Motivo', 'Funcionario', 'Horas'])

        for registro in registro_he:
            writer.writerow([
                registro.id,
                registro.motivo,
                registro.funcionario,
                registro.horas
            ])

        return response


class ExportarExcel(View):
    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="users.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Banco de Horas')

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['ID', 'MOTIVO', 'FUNCIONARIO', 'HORAS']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        registros = RegistroHoraExtra.objects.filter(utilizada=False)

        row_num = 1
        for registro in registros:
            ws.write(row_num, 0, registro.id)
            ws.write(row_num, 1, registro.motivo)
            ws.write(row_num, 2, registro.funcionario.nome)
            ws.write(row_num, 3, registro.horas)
            row_num += 1

        wb.save(response)
        return response

