from django import forms
from event.models import Event, Category, Participant

""" Mixins """
class StyledFormMixin:
    default_classes = 'border-2 bg-gray-200 rounded-lg p-3'
    def apply_default_classes(self):
        print('inside apply default function')
        for field_name, field in self.fields.items():
            # print(type(field.widget))
            if isinstance(field.widget, forms.TextInput) or isinstance(field.widget, forms.EmailInput):
                # its also help you to find out problem
                # print('N')
                field.widget.attrs.update({
                    'class':f'{self.default_classes} w-full',
                    'placeholder': f'Enter {field.label.lower()}'
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                # print('inside select_date_widget')
                field.widget.attrs.update({
                    'class': f'{self.default_classes} mt-3'
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': 'mb-3'
                })
            elif isinstance(field.widget, forms.TimeInput):
                # print('inside time input')
                field.widget.attrs.update({
                    'class':f'{self.default_classes}',
                    'placeholder':'HH:MM:SS'
                })
            elif isinstance(field.widget, forms.Select):
                # print('inside select widget')
                field.widget.attrs.update({
                    'class':f'text-2xl bg-green-500 font-bold',
                })
            
            
class EventModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets ={
            'date':forms.SelectDateWidget,
            'time':forms.TimeInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_default_classes()


class CategoryModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_default_classes()


class ParticipantModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'
        widgets={
            'events': forms.CheckboxSelectMultiple,
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_default_classes()