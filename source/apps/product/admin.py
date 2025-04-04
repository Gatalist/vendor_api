from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Attribute, ProductImage, Product


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="auto">')

    get_image.short_description = "Изображение"


class ProductAttributeInline(admin.TabularInline):
    model = Attribute
    extra = 1
    fields = ("name", "value")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_image", )
    list_display_links = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.poster.url}" width="50" height="auto">')

    get_image.short_description = "Изображение"
    readonly_fields = ("get_image", )


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "value", "group", "category", "category", "product")
    list_display_links = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("idd", "name", "get_image", "category", "created", "is_active")
    list_display_links = ("name",)
    list_filter = ("category", "is_active")
    search_fields = ("idd", "name",)
    save_on_top = True
    save_as = True
    actions = ['publish', 'unpublish']
    list_editable = ("is_active",)

    prepopulated_fields = {"slug": ("name",)}

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="50" height="auto">')

    get_image.short_description = "Изображение"

    readonly_fields = ("get_image",)

    inlines = [ProductAttributeInline, ProductImageInline,]

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(is_active=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        if row_update == 2:
            message_bit = '2 записи были обновлены'
        else:
            message_bit = f'{row_update} записей было обновлено'

        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(is_active=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        if row_update == 2:
            message_bit = '2 записи были обновлены'
        else:
            message_bit = f'{row_update} записей было обновлено'

        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change',)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_image", "product",)
    list_display_links = ("name",)
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50" height="auto">')

    get_image.short_description = "Изображение"
