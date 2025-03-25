from django import forms
from event.models import Event, Category

""" Mixins """
class StyledFormMixin:
    default_classes = 'border-2 bg-gray-200 rounded-lg p-3 focus:outline-none mb-3'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call the parent's __init__ method
        self.apply_default_classes()

    def apply_default_classes(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    'class':f'{self.default_classes}',
                    'placeholder':'HH:MM:SS'
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': 'max-h-40 overflow-y-auto'
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': f'bg-gray-200 p-2 mb-3'
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class':f'{self.default_classes}',
                })
            elif isinstance(field.widget, forms.TextInput) or isinstance(field.widget, forms.EmailInput) or isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs.update({
                    'class':f'{self.default_classes} w-full',
                    'placeholder': f'Enter {field.label}'
                })
            
            
class EventModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category', 'media']
        widgets ={
            'date':forms.SelectDateWidget,
            'time':forms.TimeInput,
            'media': forms.ClearableFileInput(attrs={
                'class': 'border-2 bg-gray-200 rounded-lg p-3 w-full',
                'accept': 'image/*',  # Only allow image files
            })
        }

class CategoryModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
