from django.db import models
from django.conf import settings
import os
from PIL import Image
from django.utils.text import slugify

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(
         upload_to='produto_imagens/%Y/%m', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField()
    preco_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices= (
        ('V', 'Variável'),
        ('S', 'Simples'),
        )      
    )

    def get_preco_formatado(self):
        return f"R$ {self.preco_marketing:.2f}".replace('.', ',')
    get_preco_formatado.short_description = 'Preco'

    def get_preco_promocional_formatado(self):
        return f"R$ {self.preco_marketing_promocional:.2f}".replace('.', ',')
    get_preco_promocional_formatado.short_description = 'Preco Promo'


    def __str__(self):
        return self.nome
    
    @staticmethod
    def resize_image(img, new_width=800):
        #print(img.name)
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size
        
        if(original_width <= new_width):
            img_pil.close()
            print(f"{img.name} de tamanho OK")
            return
        
        new_height = round((new_width * original_height) / original_width)

        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)

        new_img.save(
            img_full_path, 
            optimaze=True,
            quality=50
        )

        print(f"{img.name} Redimensionada")

    def save(self, *args, **kwargs):
        
        if not self.slug:
            
            slug = slugify(self.nome)
            print(slug)
            self.slug = slug
        
        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)
       




     
class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE) 
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome
    
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'


