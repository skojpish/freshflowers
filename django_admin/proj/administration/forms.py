from django.forms import ModelForm, FileInput
from .models import ExcelInput, PriceList

class ExcelForm(ModelForm):
    class Meta:
        model = ExcelInput
        fields = ['excel_file']

        widgets = {
            'excel_file': FileInput(attrs={
                'class': 'form-control'
            })
        }

class PriceListForm(ModelForm):
    class Meta:
        model = PriceList
        fields = ['price_list']

        widgets = {
            'price_list': FileInput(attrs={
                'class': 'form-control'
            })
        }