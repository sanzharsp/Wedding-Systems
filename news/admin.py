from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class Author_Admin(UserAdmin):
    model = Author
    list_display = ('email', 'is_superuser','is_staff')
    list_filter = ('email', 'is_superuser',)
    fieldsets = (
        ('Общая информация', {'fields': ('email',)}),
        ('Права доступа и аутентификация', {'fields': ('is_staff','is_superuser')}),

    )
    add_fieldsets = (
        ('General information', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',)},

        ),
         ('Права доступа и аутентификация', {'fields': ('is_staff','is_superuser')}),
    )
    search_fields = ('email',)
    ordering = ('email',)



class Wedding_Admin(admin.ModelAdmin):
    model = Wedding
    list_display = ('WeddingName','name','coming','spouse','I_cant_come')
    list_filter = ('name','coming','spouse','I_cant_come','created_at','WeddingName')
    search_fields = ('name','coming','spouse','I_cant_come')
    ordering = ('name','coming','spouse','I_cant_come')


class WeddingName_Admin(admin.ModelAdmin):
    model = WeddingName
    list_display = ('name','description','created_at','WeddingDate',)
    list_filter = ('name','description','created_at','WeddingDate',)
    search_fields = ('name','description','created_at','WeddingDate',)
    ordering = ('name','description','created_at','WeddingDate',)


admin.site.register(Author,Author_Admin)
admin.site.register(WeddingName,WeddingName_Admin)
admin.site.register(Wedding,Wedding_Admin)

# Register your models here.