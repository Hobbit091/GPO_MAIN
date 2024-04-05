from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class sequence_desc(models.Model):
    M_ID = models.AutoField(primary_key=True)
    OEIS_ID = models.CharField(max_length=255, unique=True)
    special_title = models.TextField()
    number_of_parameters = models.IntegerField()
    recurrent_formula = models.TextField(blank=True, null=True)
    explicit_formula = models.TextField(blank=True, null=True)
    other_formula = models.TextField(blank=True, null=True)
    explicit_formula_latex = models.TextField(blank=True, null=True)
    other_formula_latex = models.TextField(blank=True, null=True)
    recurrent_formula_latex = models.TextField(blank=True, null=True)
    generating_function = models.TextField(blank=True, null=True)
    generating_function_latex = models.TextField(blank=True, null=True)

class interpretation(models.Model):
    Interp_ID = models.AutoField(primary_key=True)
    n_value = models.TextField()
    description = models.TextField()
    example_text = models.TextField(blank=True, null=True)
    example_image = models.ImageField(upload_to='images/')
    example_table = models.TextField(blank=True, null=True)
    example_image_process = ImageSpecField(source='example_image',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})


class algorithm(models.Model):
    Alg_ID = models.AutoField(primary_key=True)
    alg_name = models.TextField()
    title = models.TextField()
    number_of_parameters = models.IntegerField()
    parameters_name = models.TextField()
    capacity_formula = models.TextField(blank=True, null=True)
    capacity_formula_latex = models.TextField(blank=True, null=True)
    tree_structure = models.ImageField(upload_to='images/')
    pseudocode = models.TextField(blank=True, null=True)
    algorithm_code = models.TextField(blank=True, null=True)
    href_code = models.TextField(blank=True, null=True)

class sequence_tb(models.Model):
    M_ID = models.ForeignKey(sequence_desc, on_delete=models.CASCADE)
    Alg_ID = models.ForeignKey(algorithm, on_delete=models.CASCADE)
    Interp_ID = models.ForeignKey(interpretation, on_delete=models.CASCADE)