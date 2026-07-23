from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PredictionResult, ResultStatus
 
 
class ResultStatusInline(admin.TabularInline):
    model = ResultStatus
    extra = 0
    verbose_name = "Status Record"
    verbose_name_plural = "Status Records"
 
 
class AdminPredictionResult(admin.ModelAdmin):
    list_display = ['id', 'label', 'confidence', 'created_at']
    list_filter = ['label']
    search_fields = ['label']
    inlines = [ResultStatusInline]
 
 
class AdminResultStatus(admin.ModelAdmin):
    list_display = ['id', 'result', 'status', 'caption', 'created_at']
    list_filter = ['status']
    search_fields = ['caption']
 
 
admin.site.register(PredictionResult, AdminPredictionResult)
admin.site.register(ResultStatus, AdminResultStatus)
 
