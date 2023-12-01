from django import forms
from django.contrib import admin

from .models import Item, Order, Discount, Tax


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('items', 'tax', 'discount')

    def clean(self):
        cleaned_data = super(OrderForm, self).clean()['items']
        st = set()
        for i in cleaned_data:
            st.add(i.currency)
        if len(st) > 1:
            raise forms.ValidationError("Товары в заказе должны быть одной валюты")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderForm


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    fields = ('display_name', 'description', 'percentage', 'inclusive', 'active', 'tax_hash')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('tax_hash', 'percentage', 'inclusive')
        else:
            return ('tax_hash',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    fields = ('percent_off', 'discount_hash')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('percent_off', 'discount_hash')
        else:
            return ('discount_hash')


admin.site.register(Item)
