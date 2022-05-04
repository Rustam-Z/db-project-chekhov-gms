from django.contrib import admin

from .models import (Person,
                     WorkingHours,
                     Registration,
                     Subscription,
                     Payment,
                     Deposit,
                     Location,
                     Equipment,
                     Gym,
                     Manager,
                     Supplier,
                     Coach,
                     Client,
                     Training,
                     WorkoutPlan,
                     Rank,
                     SportsWear,
                     Nutrition,
                     Purchase,
                     Order,
                     )


@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('number', 'currency', 'amount', 'subscription_number',)
    list_filter = ('currency',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'ssn',)  # TODO: filter by AGE range
    list_filter = ('gender',)
    search_fields = ('ssn', 'name__startswith',)


@admin.register(Manager)
class ManagerAdmin(PersonAdmin):
    list_display = PersonAdmin.list_display + ('seniority_level',)
    list_filter = ('gender', 'seniority_level', 'working_hours__weekday',)  # TODO: filter by AGE and SALARY range


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('retailer_name', 'product_name', 'product_type',)
    list_filter = ('product_type',)
    search_fields = ('retailer_name__startswith', 'product_name__startswith',)


@admin.register(Coach)
class CoachAdmin(PersonAdmin):
    list_display = PersonAdmin.list_display + ('licence_number', 'specialization',)
    list_filter = PersonAdmin.list_filter + ('specialization',)  # TODO: filter by AGE and SALARY range
    search_fields = PersonAdmin.search_fields + ('licence_number', 'specialization',)


@admin.register(Client)
class ClientAdmin(PersonAdmin):
    list_display = PersonAdmin.list_display + ('subscription',)
    search_fields = PersonAdmin.search_fields + ('subscription__number', 'registration__number', 'payment__transaction_number')


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'type', 'name', 'gym')
    list_filter = ('type', 'gym',)
    search_fields = ('type', 'gym__name',)


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'manager',)
    list_filter = ('capacity', 'manager', 'coaches',)
    search_fields = ('location__location', 'manager__name',)


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('exercise_name', 'duration',)
    list_filter = ('duration',)


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('coach', 'client', 'training',)
    list_filter = ('coach',)
    search_fields = ('coach__name', 'client__name', 'training__exercise_name')


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    search_fields = ('client__name', 'name', 'exercise_name__exercise_name',)


@admin.register(SportsWear)
class SportsWearAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'price', 'size', 'type', 'sells', 'provider',)
    list_filter = ('brand_name', 'sells', 'provider',)
    search_fields = ('brand_name__brand_name', 'type', 'provider__retailer_name', 'sells__name',)


@admin.register(Nutrition)
class NutritionAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'price', 'deals', 'supplier',)
    list_filter = ('supplier', 'name', 'deals',)
    search_fields = ('product_id', 'name', 'supplier__retailer_name', 'deals__name')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'deposit_number',)
    search_fields = ('brand_name__brand_name', 'deposit_number__number',)


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('manager', 'retailer_name',)
    search_fields = ('manager__name', 'retailer_name__retailer_name',)
