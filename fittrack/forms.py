from django import forms
from .models import  ExerciseSet,ProteinCal,CalCount



class WorkoutForm(forms.Form):
    pass


class ExerciseSetForm(forms.ModelForm):
    class Meta:
        model = ExerciseSet
        fields = ['exercise', 'sets', 'reps', 'weight','intensity']
        widgets = {
            'exercise': forms.Select(attrs={'class': 'form-control'}),
            'sets':forms.NumberInput(attrs={'class':'form-control','required':True}),
            'reps': forms.NumberInput(attrs={'class': 'form-control','required':True}),
            'weight': forms.NumberInput(attrs={'class': 'form-control','required':True}),
            'intensity':forms.Select(attrs={'class':'form-control'})
        }
        labels={
            'weight':'Weight (kg)'
        }

    workout_id = forms.IntegerField(widget=forms.HiddenInput(),required=False)


    

class ProtienCalForm(forms.ModelForm):
    class Meta:
        model = ProteinCal
        fields = ['age','weight','height','activity']
        widgets = {
            'age':forms.NumberInput(attrs={'class':'form-control','required':True}),
            'weight':forms.NumberInput(attrs={'class':'form-control','required':True}),
            'height':forms.NumberInput(attrs={'class':'form-control','required':True}),
            'activity':forms.Select(attrs={'class':'form-control','required':True})
        }
        labels= {
            'weight':'Weight (kg)',
            'height':'Height (cm)',
        }

class CalCountForm(forms.ModelForm):
    class Meta:
        model = CalCount
        fields = ['age','weight','height','gender','activity','goal']
        widgets = {
            'age':forms.NumberInput(attrs={'class':'form-control','required':True}),
            'weight':forms.NumberInput(attrs={'class':'form-control','required':True}),
            'height':forms.NumberInput(attrs={'class':'form-control','required':True}),
            'gender':forms.Select(attrs={'class':'form-control','required':True}),
            'activity':forms.Select(attrs={'class':'form-control','required':True}),
            'goal':forms.Select(attrs={'class':'form-control','required':True})
        }
        labels= {
            'weight':'Weight (kg)',
            'height':'Height (cm)',
        }