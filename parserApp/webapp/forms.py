from django import forms
from django.forms import Select

from .models import Area, ChildRole, EducationLevel, Experience, Employment, Schedule


class ParserForm(forms.Form):
    choices = list(Area.objects.all().values_list('area_name'))
    query_text = forms.CharField(max_length=100,
                                 required=False,
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'placeholder': 'Запрос',
                                         'style': 'width: 25%;'
                                                  'margin-left: 32%'
                                     }))
    region = forms.ModelChoiceField(queryset=Area.objects.all(),
                                    widget=forms.Select(
                                        attrs={
                                            'class': 'form-select',
                                            'style': 'width: 25%;'
                                                     'margin-left: 32%;'
                                        }
                                    ))
    expr = forms.ModelChoiceField(queryset=Experience.objects.all(),
                                  required=False,
                                  widget=forms.Select(
                                      attrs={
                                          'class': 'form-select',
                                          'style': 'width: 25%;'
                                                   'margin-left: 32%;'
                                      }
                                  ))
    empl = forms.ModelChoiceField(queryset=Employment.objects.all(),
                                  required=False,
                                  widget=forms.Select(
                                      attrs={
                                          'class': 'form-select',
                                          'style': 'width: 25%;'
                                                   'margin-left: 32%;'
                                      }
                                  ))
    schedl = forms.ModelChoiceField(queryset=Schedule.objects.all(),
                                    required=False,
                                    widget=forms.Select(
                                        attrs={
                                            'class': 'form-select',
                                            'style': 'width: 25%;'
                                                     'margin-left: 32%;'
                                        }
                                    ))
    jobs = forms.ModelMultipleChoiceField(queryset=ChildRole.objects.all().order_by('role_name'),
                                          widget=forms.CheckboxSelectMultiple(), required=False)

