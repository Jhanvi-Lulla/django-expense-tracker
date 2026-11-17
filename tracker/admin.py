from django.contrib import admin
from .models import expense


@admin.register(expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("Expense_reason", "Amount", "user")
    list_filter = ("user",)
    search_fields = ("Expense_reason",)
