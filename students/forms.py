from django import forms
from .models import Strength, Student, Talent, Interest


class StrengthForm(forms.ModelForm):
    class Meta:
        model = Strength
        fields = [
            "titulo",
            "descripcion",
            "nivel_desarrollo",
            "visible_dashboard",
            "observaciones",
        ]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "nivel_desarrollo": forms.NumberInput(
                attrs={
                    "class": "form-range",
                    "type": "range",
                    "min": "1",
                    "max": "5",
                    "step": "1",
                    "id": "id_nivel_desarrollo",
                }
            ),
            "visible_dashboard": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class TalentForm(forms.ModelForm):
    class Meta:
        model = Talent
        fields = [
            "titulo",
            "descripcion",
            "nivel_desarrollo",
            "visible_dashboard",
            "observaciones",
        ]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "nivel_desarrollo": forms.NumberInput(
                attrs={
                    "class": "form-range",
                    "type": "range",
                    "min": "1",
                    "max": "5",
                    "step": "1",
                    "id": "id_nivel_desarrollo",
                }
            ),
            "visible_dashboard": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = [
            "titulo",
            "descripcion",
            "nivel_interes",
            "visible_dashboard",
            "observaciones",
        ]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "nivel_interes": forms.NumberInput(
                attrs={
                    "class": "form-range",
                    "type": "range",
                    "min": "1",
                    "max": "5",
                    "step": "1",
                    "id": "id_nivel_interes",
                }
            ),
            "visible_dashboard": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class StudentPhotoForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["foto", "foto_pos_x", "foto_pos_y"]
        widgets = {
            "foto": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "foto_pos_x": forms.NumberInput(
                attrs={
                    "class": "form-range",
                    "type": "range",
                    "min": "0",
                    "max": "100",
                    "step": "1",
                    "id": "id_foto_pos_x",
                }
            ),
            "foto_pos_y": forms.NumberInput(
                attrs={
                    "class": "form-range",
                    "type": "range",
                    "min": "0",
                    "max": "100",
                    "step": "1",
                    "id": "id_foto_pos_y",
                }
            ),
        }