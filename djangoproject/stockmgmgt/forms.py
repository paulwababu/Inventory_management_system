from django import forms
from .models import Stock, OrderQuantity

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity', 'price']

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('Please enter category of item')
        
        for instance in Stock.objects.all():
            if instance.category == category:
                raise forms.ValidationError(category + ' is already created')
        return category

    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('Please enter item name')
        return item_name    

class StockSearchForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name']

class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity', 'price']

class IssueForm(forms.Form):
    quantity = forms.IntegerField(label='', min_value=1, widget=forms.NumberInput())
    class Meta:
        model = OrderQuantity
        fields = 'quantity'
    
    # Edit by bryan
    def __init__(self, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['quantity'].widget.attrs['style'] = 'width:100%; height:80%px;'


class ReceiveForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['receive_quantity', 'receive_by']        
