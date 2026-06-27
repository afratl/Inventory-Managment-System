from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from django.db import models
from slugify import slugify
from django.conf import settings

User = get_user_model()

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def total_products(self):
        # İlişkili ürünlerin stok toplamını hesaplar
        return self.product_set.aggregate(total_stock=models.Sum('stock'))['total_stock'] or 0

    
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image =models.ImageField( upload_to='brand' , null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(editable=False ,default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Firm(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    image =models.ImageField( upload_to="firm",null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Purchases(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # birim fiyat
    price_total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, editable=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)  # Yeni kategori alanı

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        old_quantity = 0

        if not is_new:
            old_quantity = Purchases.objects.get(pk=self.pk).quantity

        # Toplam fiyat hesapla
        self.price_total = self.price * self.quantity

        # Kategoriyi üründen al
        if is_new:
            self.category = self.product.category

        # Stok artırma işlemi
        fark = self.quantity if is_new else self.quantity - old_quantity

        with transaction.atomic():
            super().save(*args, **kwargs)
            self.product.stock += fark  # Satın alma olduğu için stok artırılır
            self.product.save()

    def __str__(self):
        return f"{self.product} - {self.quantity} adet alindi"

        
    
class Sales(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, editable=False)

    def save(self, *args, **kwargs):
        is_new = self._state.adding  # yeni mi, güncelleme mi?
        old_quantity = 0

        if not is_new:
            old_quantity = Sales.objects.get(pk=self.pk).quantity

        # Toplam fiyat hesapla
        self.price_total = self.price * self.quantity

        # Mevcut stok yetersizse satışa izin verme
        fark = self.quantity if is_new else self.quantity - old_quantity
        if self.product.stock < fark:
            raise ValidationError("Yetersiz stok: bu kadar ürün stokta yok.")

        with transaction.atomic():
            super().save(*args, **kwargs)
            self.product.stock -= fark
            self.product.save()

    def delete(self, *args, **kwargs):
        # Silindiğinde stok geri eklensin
        self.product.stock += self.quantity
        self.product.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.quantity} adet satıldı"
