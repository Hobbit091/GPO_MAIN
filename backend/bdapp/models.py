from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class sequence_desc(models.Model):
    M_ID = models.AutoField(primary_key=True)
    OEIS_ID = models.CharField(max_length=255, unique=True)
    special_title = models.TextField()
    number_of_parameters = models.IntegerField()
    recurrent_formula = models.TextField(blank=True, null=True)
    explicit_formula_latex = models.TextField(blank=True, null=True)
    other_formula_latex = models.TextField(blank=True, null=True)
    recurrent_formula_latex = models.TextField(blank=True, null=True)
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
                                      processors=[ResizeToFill(300, 200)],
                                      #format='JPEG',
                                      options={'quality': 60})
     
    def __str__(self):
        return F"{self.Interp_ID}"

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
    field1_name=models.TextField(default="")
    field1_desc=models.TextField(default="")
    field2_name=models.TextField(default="")
    field2_desc=models.TextField(default="")
    field3_name=models.TextField(default="")
    tree_structure = models.ImageField(upload_to='images/',blank=True, null=True)
    tree_structure_process = ImageSpecField(source='tree_structure',
                                      processors=[ResizeToFill(400, 400)],
                                      #format='JPEG',
                                      options={'quality': 60})
    field4_name=models.TextField(default="")
    field4_desc=models.TextField(default="")
    field5_name=models.TextField(default="")
    field5_desc=models.TextField(default="")
    alg_code = models.TextField(blank=False, null=False)
   


     
    def __str__(self):
        return self.alg_name

class sequence_tb(models.Model):
    M_ID = models.ForeignKey(sequence_desc, on_delete=models.CASCADE)
    Alg_ID = models.ForeignKey(algorithm, on_delete=models.CASCADE)
    Interp_ID = models.ForeignKey(interpretation, on_delete=models.CASCADE)

     
    def __str__(self):
        return F"{self.M_ID}"