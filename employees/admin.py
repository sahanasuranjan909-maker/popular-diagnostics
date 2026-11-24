from django.contrib import admin
from .models import Employee, CollectionRequest

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "full_name", "phone", "availability", "updated_at")
    list_filter = ("availability",)
    search_fields = ("employee_id", "full_name", "phone", "email")

@admin.register(CollectionRequest)
class CollectionRequestAdmin(admin.ModelAdmin):
    list_display = ("case_number", "customer_name", "status", "payout_amount", "created_at")
    list_filter = ("status", "collection_type")
    search_fields = ("case_number", "customer_name", "address", "pin_code")
