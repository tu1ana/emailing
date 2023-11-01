from django import forms

from main.models import Emailing, Message, Client


class StyleFormMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class EmailingForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Emailing
        fields = '__all__'
        # exclude = ('status',)


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = ('subject', 'body', 'client', 'emailing')


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'
