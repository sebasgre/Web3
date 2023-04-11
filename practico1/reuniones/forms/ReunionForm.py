from reuniones import forms

from reuniones.models import Reunion
from reuniones.models.Usuario import Usuario


class ReunionForm(forms.ModelForm):
    nombre_reunion = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fecha_hora = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control'})
    )
    dueño = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        label='dueño',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    asistentes = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    class Meta:
        model = Reunion
        fields = ['nombre_reunion', 'fecha_hora', 'dueño', 'asistentes']