from django.contrib import admin
from myapp.models import MyIntData, MyColData, UserInfo
# Register your models here.
admin.site.register(MyIntData)
# admin.site.register(MyColData)

# 用decorate來導入MyColData，建立一個class，讓admin頁面多了contentㄉ

@admin.register(MyColData)
class MyColDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'content',)

admin.site.register(UserInfo)
