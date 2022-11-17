import os
import json
import requests
import base64
from src.config.celery import app
from io import BytesIO
from pathlib import Path
from django.template.loader import render_to_string
from src.api.models import Check
from django.conf import settings
from django.core.files.base import File, ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile


def get_pdf_check(html):
    url = settings.URL_PDF_RENDER
    b = base64.b64encode(bytes(html, 'utf-8'))
    base64_str = b.decode('utf-8')
    data = {
        'contents': base64_str,
    }
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response


def get_order_dict(order):
    order_dict = {}
    order_dict.update(order)
    return order_dict


@app.task
def rendered_pdf_kitchen(data):
    check_id = data.get('check_id', None)
    if check_id is not None:
        check = Check.objects.get(id=int(check_id))
        order_dict = get_order_dict(check.order)
        order_number = order_dict.pop('order_number')
        html = render_to_string(settings.KITCHEN_CHECK_TEMPLATE, {'order': order_dict})
        response = get_pdf_check(html)
        if response.status_code == 200:
            check.status = "rendered"
            check.save()
        pdf_field = check.pdf_file
        buffer = BytesIO()
        buffer.write(response.content)
        pdf_file = ContentFile(buffer.getvalue())
        pdf_name = f"{order_number}_{check.type}.pdf"
        pdf_field.save(pdf_name, InMemoryUploadedFile(pdf_file, None, pdf_name, "application/pdf", pdf_file.tell, None))
        check.save()
        return True
    else:
        return False


@app.task
def rendered_pdf_client(data):
    check_id = data.get('check_id', None)
    if check_id is not None:
        check = Check.objects.get(id=int(check_id))
        total_price = 0
        order_dict = get_order_dict(check.order)
        order_number = order_dict.pop('order_number')
        for item in order_dict.values():
            total_price += int(item['price'])
        html = render_to_string(settings.CLIENT_CHECK_TEMPLATE, {'order': order_dict, 'total_price': total_price})
        response = get_pdf_check(html)
        if response.status_code == 200:
            check.status = "rendered"
            check.save()
        pdf_field = check.pdf_file
        buffer = BytesIO()
        buffer.write(response.content)
        pdf_file = ContentFile(buffer.getvalue())
        pdf_name = f"{order_number}_{check.type}.pdf"
        pdf_field.save(pdf_name, InMemoryUploadedFile(pdf_file, None, pdf_name, "application/pdf", pdf_file.tell, None))
        check.save()
        return True
    else:
        return False
