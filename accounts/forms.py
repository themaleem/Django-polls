from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegistrationForm(forms.Form):
    username=forms.CharField(
                                label="username", 
                                required=True,
                                widget=forms.TextInput(
                                    attrs={'class':'form-control'}
                                    )
                            )

    email=forms.EmailField(
                            required=False,
                            widget=forms.TextInput(
                                    attrs={'class':'form-control'}
                                    )
                            )

    password=forms.CharField(
                                label="password", 
                                required=True,
                                widget=forms.PasswordInput(
                                    attrs={'class':'form-control'}
                                    )
                            )

    password2=forms.CharField(
                                label="confirm password",
                                required=True,
                                widget=forms.PasswordInput(
                                    attrs={'class':'form-control'}
                                    )
                            )


    def clean_email(self):
        email = self.cleaned_data["email"]
        qs=User.objects.filter(email=email)
        if qs.exists():
            raise ValidationError("Email already exists.")
        return email
    
    def clean(self):
        clean_data=super().clean()
        p1=clean_data.get('password')
        p2=clean_data.get('password2')
        if p1!=p2:
            raise ValidationError("Password do not match")