from django.db import models

CHECK_TYPE_CHOICES = (
    ('new', 'new'),
    ("rendered", 'rendered'),
    ("printed", 'printed')
)

PRINTER_TYPE_CHOICES = (
    ('kitchen', 'kitchen'),
    ('client', 'client')
)


class Printer(models.Model):
    class Meta:
        verbose_name = "Printer"
        verbose_name_plural = "Printers"

    name = models.CharField(max_length=250, null=True, blank=True, verbose_name='Name Printer')
    api_key = models.CharField(max_length=250, verbose_name='Key access API', blank=True, null=True, unique=True)
    check_type = models.CharField(choices=PRINTER_TYPE_CHOICES,
                                  max_length=10, verbose_name='Check type', blank=True, null=True)
    point_id = models.IntegerField(verbose_name='Point printer')

    def __str__(self):
        return self.name


class Check(models.Model):
    class Meta:
        verbose_name = 'Check'
        verbose_name_plural = 'Checks'

    printer_id = models.ForeignKey(Printer, blank=True, related_name='printer', on_delete=models.CASCADE)
    type = models.CharField(choices=PRINTER_TYPE_CHOICES, max_length=512, verbose_name='Type check', blank=True,
                            null=True)
    order = models.JSONField(verbose_name='Order information', null=True, blank=True)
    status = models.CharField(choices=CHECK_TYPE_CHOICES, max_length=15, default=CHECK_TYPE_CHOICES[0][1],
                              verbose_name='Status check', blank=True, null=True)
    pdf_file = models.FileField(verbose_name='Check format PDF', upload_to='media/pdf')

    def __str__(self):
        return self.status
