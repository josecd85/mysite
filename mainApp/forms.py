from django import forms
from .models import Alertas

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit

class AlertForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AlertForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['titulo'].widget.attrs['readonly'] = True
            self.fields['estado'].widget.attrs['readonly'] = True
            self.fields['descrip'].widget.attrs['readonly'] = True
            self.fields['descrip'].label= 'Descripción'
            self.fields['comment'].label= 'Comentario'

    class Meta:
        model = Alertas
        fields = ('titulo', 'descrip', 'estado', 'comment')
        

class ResetPassForm(forms.Form):
    pass_user = forms.CharField(max_length=50, widget=forms.PasswordInput, label='Nueva Contraseña')
    pass_confirm = forms.CharField(max_length=50, widget=forms.PasswordInput, label="Repetir Contraseña")
