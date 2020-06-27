from django.contrib import admin
from . import models


def activate(modeladmin, request, queryset):
    queryset.update(is_active=True,)


activate.short_description = "Mark as activate"


def deactivate(modeladmin, request, queryset):
    queryset.update(is_active=False,)


deactivate.short_description = "Mark as unactive"


def mark_new(modeladmin, request, queryset):
    queryset.update(is_new=True,)


mark_new.short_description = "Mark as new"


def mark_old(modeladmin, request, queryset):
    queryset.update(is_new=False,)


mark_old.short_description = "Mark as old"


# ---CATEGORY---
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    actions = [activate, deactivate]

    list_display = ["name", "parent", "is_active"]
    list_editable = ["parent"]
    ordering = ["name"]

    list_filter = ["is_active"]

    fieldsets = (
        (None, {"fields": ("parent", ("name", "slug"), "is_active")}),
        (None, {"fields": ("meta_title", ("meta_keywords", "meta_description",))}),
    )
    prepopulated_fields = {"slug": ("name",)}


# ---CHARACTERISTIC---
class CharacteristicInline(admin.TabularInline):
    model = models.Characteristic
    extra = 1
    max_num = 3


# ---IMAGE---
class ImageInline(admin.TabularInline):
    model = models.Image
    max_num = 20


# ---FILE MANAGER---
class FileManagerInline(admin.TabularInline):
    model = models.FileManager
    extra = 1
    max_num = 20


# ---PRODUCT---
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
        "description",
        "product_code",
        "brand__name",
        "category__name",
    ]
    actions = [activate, deactivate, mark_new, mark_old]

    list_display = [
        "name",
        "product_code",
        "category",
        "brand",
        "quantity",
        "price",
        "promotional_price",
        "is_on_promotion",
        "is_active",
        "is_new",
        "kg_weight",
    ]
    ordering = ["category"]

    list_filter = [
        "is_active",
        "is_new",
        "is_on_promotion",
        "brand",
        "category",
    ]
    date_hierarchy = "created_at"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("name", "slug"),
                    "description",
                    "category",
                    "brand",
                    ("is_active", "is_new"),
                    ("product_code", "quantity"),
                    ("price",),
                    ("promotional_price", "is_on_promotion"),
                    "youtube_url",
                    "meta_title",
                    ("meta_keywords", "meta_description"),
                    "kg_weight",
                    "main_image",
                )
            },
        ),
    )
    inlines = [ImageInline, FileManagerInline, CharacteristicInline]
    prepopulated_fields = {"slug": ("name",)}


# ---BRAND---
@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name"]

