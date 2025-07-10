from django import forms


# A form for creating a new service.
class CreateNewService(forms.Form):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price_hour = forms.DecimalField(
        decimal_places=2, max_digits=5, min_value=0.00)
    field = forms.ChoiceField(required=True)

    def __init__(self, *args, choices='', ** kwargs):
        super(CreateNewService, self).__init__(*args, **kwargs)
        # Dynamically set the choices for the 'field' dropdown based on the company's field.
        if choices:
            self.fields['field'].choices = choices
        # adding placeholders to form fields
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Service Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'

        self.fields['name'].widget.attrs['autocomplete'] = 'off'


# A form for requesting a service.
class RequestServiceForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter Address'}), label='Address')
    service_time = forms.DecimalField(decimal_places=1, max_digits=5, min_value=0.00, widget=forms.NumberInput(attrs={'placeholder': 'Enter service hours'}), label='Service Time (hours)')
