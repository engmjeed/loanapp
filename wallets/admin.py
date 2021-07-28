# from django.contrib import admin
# from .models import CashTransaction
# from .const import TransactionType

# # Register your models here.

# class CashTransactionAdmin(admin.ModelAdmin):

#     fields = (
#             "id",
#             "type",
#             "value",
#             "subject",
#             "final_balance",
#             "initial_balance",
#             "details",
#             "created_at",
#         )
    
#     readonly_fields = (
#             "id",
#             "type",
#             "value",
#             "subject",
#             "final_balance",
#             "initial_balance",
#             "details",
#             "created_at",
#         )
#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_add_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

# admin.site.register(CashTransaction,CashTransactionAdmin)

