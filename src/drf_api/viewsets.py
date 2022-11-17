import json
from django.db.models import Q
from django.http import FileResponse
from rest_framework import viewsets, renderers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from src.config.celery import app
from django.http import JsonResponse
from src.api.models import Check, Printer
from .serializers import CheckSerializer, PrinterSerializer
from .rendereds import PassthroughRenderer


def get_order_json(order):
    return json.loads(order.replace("\'", "\""))


class ResponsePdfViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer

    @action(methods=['get'], detail=True, renderer_classes=(PassthroughRenderer,))
    def download(self, *args, **kwargs):
        instance = self.get_object()
        file_handle = instance.pdf_file.open()
        response = FileResponse(file_handle, content_type='application/pdf')
        response['Content-Length'] = instance.pdf_file.size
        response['Content-Disposition'] = 'attachment; filename="%s"' % instance.pdf_file.name.split('/')[-1]

        return response


class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer

    def list(self, request, *args, **kwargs):
        api_key = self.kwargs.get('api_key', None)
        if api_key:
            try:
                printer = Printer.objects.get(api_key=api_key)
                checks = Check.objects.filter(printer=printer, status='rendered')
                serializer = CheckSerializer(checks, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Printer.DoesNotExist:
                return JsonResponse({'Для цього принтера чеків доступних для друку не знайдено'}, status=status.HTTP_404_NOT_FOUND)
        return super(PrinterViewSet, self).list(request, *args, **kwargs)


class CheckViewSet(viewsets.ModelViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        point_id = data.get("point_id", None)
        order = data.get('order', {})
        order_dict = get_order_json(order)
        checks = Check.objects.filter(Q(printer=Printer.objects.filter(point_id=1).first()) |
                                      Q(printer=Printer.objects.filter(point_id=1).last()))
        for check in checks:
            if order_dict['order_number'] == check.order['order_number']:
                return JsonResponse({"data": f"Замовлення з номером {order_dict['order_number']} вже існує"},
                                    status=status.HTTP_400_BAD_REQUEST)
        if Printer.objects.filter(point_id=int(point_id)).exists():
            printers = Printer.objects.filter(point_id=int(point_id))
            for printer in printers:
                if printer.check_type == 'kitchen':
                    data_models = {'printer': printer, 'type': 'kitchen', 'status': data.get('status', 'new'),
                                   'order': order_dict}
                    check = Check.objects.create(**data_models)
                    data_task = {'check_id': check.id}
                    # app.send_task('printer.main.tasks.rendered_pdf_kitchen', [data_task])
                else:
                    data_models = {'printer': printer, 'type': 'client', 'status': data.get('status', 'new'),
                                   'order': order_dict}
                    check = Check.objects.create(**data_models)
                    data_task = {'check_id': check.id}
                    # app.send_task('printer.main.tasks.rendered_pdf_client', [data_task])

            return JsonResponse({"data": "Чек успішно створено"}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'data': "Принтер не знайдено"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        data = request.data
        try:
            check = Check.objects.get(id=int(kwargs.get('pk', None)))
            check.status = data.get('status', None)
            check.save()
            return JsonResponse({'status': True}, status=status.HTTP_200_OK)
        except Check.DoesNotExist:
            return JsonResponse({'data': "Заказу не знайдено"}, status=status.HTTP_404_NOT_FOUND)