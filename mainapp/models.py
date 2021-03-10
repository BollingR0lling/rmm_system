from django.db import models


class Machine(models.Model):
    username = models.CharField(max_length=50, null=False, verbose_name='Username')
    password = models.CharField(max_length=100, null=False, verbose_name='Password')
    ip_address = models.GenericIPAddressField(max_length=15, null=False, verbose_name='Ip address')
    port = models.IntegerField(null=False, verbose_name='Port')
    machine_name = models.CharField(max_length=100, null=False, verbose_name='Computer name')
    os = models.CharField(max_length=50, null=False, verbose_name='Operating system')

    def __str__(self):
        return f'{self.os}:{self.machine_name}_{self.ip_address}:{self.port}'
