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
    
    def __str__(self):
        return f"{self.special_title} - {self.OEIS_ID}"
    

class interpretation(models.Model):
    Interp_ID = models.AutoField(primary_key=True)
    n_value = models.TextField()
    description = models.TextField()
    example_text = models.TextField(blank=True, null=True)
    example_image = models.ImageField(upload_to='images/', blank=True, null=True)
    example_table = models.TextField(blank=True, null=True)
    example_image_process = ImageSpecField(source='example_image',
                                      #processors=[ResizeToFill(100, 50)],
                                      #format='JPEG',
                                      options={'quality': 60})
     
    def __str__(self):
        return F"{self.Interp_ID}"

class algorithm(models.Model):
    Alg_ID = models.AutoField(primary_key=True)
    alg_table_title = models.CharField(default="Описание алгоритма, Формула мощности, Структура дерева И/ИЛИ, Псевдокод алгоритма, Источник иформации")
    number_of_parameters = models.IntegerField()
    parameters_name = models.TextField()
    alg_name = models.TextField()
    description = models.TextField()
    field1_text = models.TextField(blank=True, null=True)
    field2_text = models.TextField(blank=True, null=True)
    tree_structure = models.ImageField(upload_to='images/',blank=True, null=True)
    pseudocode = models.TextField(blank=True, null=True)
    algorithm_code = models.TextField(blank=True, null=True)
    href_code = models.TextField(blank=True, null=True)

     
    def __str__(self):
        return self.alg_name

class sequence_tb(models.Model):
    M_ID = models.ForeignKey(sequence_desc, on_delete=models.CASCADE)
    Alg_ID = models.ForeignKey(algorithm, on_delete=models.CASCADE)
    Interp_ID = models.ForeignKey(interpretation, on_delete=models.CASCADE)

     
    def __str__(self):
        return F"{self.M_ID}"