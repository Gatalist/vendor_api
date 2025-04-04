from django.db import models
from django.urls import reverse


class BaseModel(models.Model):
    is_active = models.BooleanField("Активен", default=True)
    sorted = models.IntegerField("Сортировка", default=100)
    created = models.DateTimeField("Создан", auto_now_add=True)
    updated = models.DateTimeField("Обновлен", auto_now=True)

    class Meta:
        abstract = True


class Attribute(BaseModel):
    name = models.CharField('Имя', max_length=100)
    value = models.TextField('Значение')
    group = models.CharField('Группа', max_length=100)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, verbose_name="Продукт", null=True, blank=True)

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"


class Category(BaseModel):
    name = models.CharField('Имя', max_length=100)
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name="url")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
        return reverse("category_list", kwargs={"slug": self.slug})


class Product(BaseModel):
    idd = models.IntegerField()
    name = models.CharField("Название", max_length=250)
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name="url")
    category = models.ForeignKey(
        "Category", verbose_name="Категория", null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "product_detail",
            kwargs={"category": self.category.slug, "subcategory": self.category.slug, "slug": self.slug}
        )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['-created']


class ProductImage(models.Model):
    name = models.CharField("Заголовок", max_length=150)
    image = models.ImageField("Изображение", upload_to='products_image/')
    product = models.ForeignKey("Product", verbose_name = "Продукт", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name =  "Изображение товара"
        verbose_name_plural =  "Изображение товаров"