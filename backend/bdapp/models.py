from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django_ckeditor_5.fields import CKEditor5Field

class sequence_desc(models.Model):
    M_ID = models.AutoField(primary_key=True)
    OEIS_ID = models.CharField(max_length=255, unique=True)
    sequence_description = CKEditor5Field(verbose_name='Описание', config_name='extends', default='')
    
    def __str__(self):
        return f"{self.special_title} - {self.OEIS_ID}"
    
class interpretation(models.Model):
    Interp_ID = models.AutoField(primary_key=True)
    interpretation_name = models.TextField()
    interpretation_description = CKEditor5Field(verbose_name='Описание', config_name='extends', default='')
    def __str__(self):
        return f"{self.interpretation_name}"
    
class algorithm(models.Model):
    ALG_TYPE_CHOICES = [
        ('Listing', 'Listing'),
        ('Rank', 'Rank'),
        ('Unrank', 'Unrank'),
    ]

    Alg_ID = models.AutoField(primary_key=True)
    alg_name = models.TextField(blank=False, null=False)
    alg_type = models.CharField(
        max_length=10,
        choices=ALG_TYPE_CHOICES,
        default='Listing'
    )
    parameters_name = models.TextField(blank=False, null=False,default="N")
    number_of_parameters = models.IntegerField(blank=False, null=False)
    field_name = models.TextField(default="", blank=True, null=False)
    field_description = CKEditor5Field(verbose_name='Описание', config_name='extends', default='')
    alg_code = models.TextField(blank=False, null=False)
     
    def __str__(self):
        return self.alg_name

class sequence_tb(models.Model):
    M_ID = models.ForeignKey(sequence_desc, on_delete=models.CASCADE)
    Alg_ID = models.ForeignKey(algorithm, on_delete=models.CASCADE)
    Interp_ID = models.ForeignKey(interpretation, on_delete=models.CASCADE)

     
    def __str__(self):
        return F"{self.M_ID}"