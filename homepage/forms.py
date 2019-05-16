from django import forms 
from databases import models


class RegularlySendForm(forms.ModelForm):
    class Meta:
        model = models.RegularlySend 
        fields = ('repetition','text')
        # labels = {
        #     'repetition':'重复',
        # }
        widgets = {
            'repetition':forms.Select(
                attrs = {
                    'class':'form-control input-fixed',
                    'id':'repetition'
                }
            ),
            'text':forms.Textarea()
        }