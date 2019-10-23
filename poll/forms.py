from django import forms
from poll.models import Poll,Choice

class PollForm(forms.ModelForm):
    choice1=forms.CharField(
                                label="First Choice", 
                                required=True,
                                widget=forms.TextInput(
                                    attrs={'class':'form-control'}
                                    )
                            )
    choice2=forms.CharField(
                                label="Second Choice", 
                                required=True,
                                widget=forms.TextInput(
                                    attrs={'class':'form-control'}
                                    )
                            )
    class Meta:
        model = Poll
        fields = ['text','choice1','choice2']
        widgets={
            'text':forms.Textarea(attrs={'class':'form-control','rows':5,'cols':20})
        }

class EditPollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['text']
        widgets={
            'text':forms.Textarea(attrs={'class':'form-control','rows':5,'cols':20})
        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
    