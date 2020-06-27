from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


# ---CATEGORY---
class Category(models.Model):
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.SET_NULL)

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text='Automatically created from category name for product page URL.'
    )

    is_active = models.BooleanField(default=True)

    meta_keywords = models.CharField(
        max_length=255, help_text='SEO keywords for meta tag, should be comma-delimited', blank=True)
    meta_description = models.CharField(
        max_length=255, help_text='Short and to the point content for description meta tag', blank=True)
    meta_title = models.CharField(
        max_length=255, help_text='Title meta tag', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('slug', 'parent')
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        category_name = self.parent
        subcategory_name = self.name

        while category_name is not None:
            return f'{category_name} -> {subcategory_name}'
        return f'{subcategory_name}'

    # def get_absolute_url(self):
    #     return reverse('category', kwargs={'slug': self.slug})


# ---BRAND---
class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# ---PRODUCT---
class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text='Automatically created from category name for product page URL.'
    )

    description = RichTextUploadingField()

    # Internal Product Number
    product_code = models.CharField(max_length=6, unique=True)

    main_image = models.ImageField(
        upload_to='product_images/')

    price = models.DecimalField(
        max_digits=7, decimal_places=2, default=0.00)
    promotional_price = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, default=0.00)

    quantity = models.DecimalField(
        max_digits=7, decimal_places=2, default=0.00)

    is_active = models.BooleanField(default=True)

    meta_description = models.CharField(
        max_length=255, help_text='Short and to the point content for description meta tag')
    meta_keywords = models.CharField(
        max_length=255, help_text='SEO keywords for meta tag, should be comma-delimited')
    meta_title = models.CharField(max_length=255, help_text='Title meta tag')

    is_new = models.BooleanField(default=True)

    youtube_url = models.URLField(max_length=255, blank=True)

    # kg_weigth is information for delivery purposes only
    kg_weight = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00, help_text='Only for delivery purposes')

    is_on_promotion = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    class Meta:
        ordering = ['category']

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('product_detail', kwargs={'slug': self.slug})


# ---CHARACTERISTIC---
class Characteristic(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, default=None, null=True)

    CHARACTERISTICS = (
        ('size', 'Size'),
        ('color', 'Color'),
        ('age', 'Age'),
    )

    characteristics = models.CharField(
        max_length=50, choices=CHARACTERISTICS, default=None)
    value = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.characteristics} - {self.value}'


# ---IMAGE---
class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return ''


# ---FILE MANAGER---
class FileManager(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    product_file = models.FileField(upload_to='product_files/')

    class Meta:
        verbose_name_plural = 'File Manager'

    def __str__(self):
        return ''
