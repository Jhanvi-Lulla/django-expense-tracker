from django import forms
from .models import expense


class ItemFormModel(forms.ModelForm):
    """One form used for both Add and Update."""

    class Meta:
        model = expense
        fields = ["Expense_reason", "Amount", "Image"]
        labels = {
            "Expense_reason": "Your expense",
            "Amount": "Amount (Rs.)",
            "Image": "Image link (optional)",
        }
        widgets = {
            "Expense_reason": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Chai"}),
            "Amount": forms.NumberInput(attrs={"class": "form-control", "min": "0", "step": "0.01"}),
            "Image": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["Image"].required = False  # image is optional now

    def clean_Amount(self):
        amount = self.cleaned_data["Amount"]
        if amount < 0:
            raise forms.ValidationError("Amount cannot be negative.")
        return amount
