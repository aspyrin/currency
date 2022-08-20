import uuid

from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import ValidationError

from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            # 'password',
        )

    def clean_email(self):
        """
        :return: email in low register
        """
        email = self.cleaned_data.get("email")
        return email.lower()

    def clean(self):
        """
        check password1 = password2
        :return: ValidationError
        """
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['password1'] != cleaned_data['password2']:
                raise forms.ValidationError('Passwords missmatch!')

        return cleaned_data

    def _post_clean(self):
        """
        validation password
        :return: ValidationError
        """
        super()._post_clean()
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        """
        save User object and send email
        """
        instance = super().save(commit=False)
        instance.username = str(uuid.uuid4())
        instance.set_password(self.cleaned_data['password1'])
        instance.is_active = False

        if commit:
            instance.save()

        self._send_activation_email()

        return instance

    def _send_activation_email(self):
        """
        generate activation link send email
        """

        subject = 'Activate Your Account'
        body = f'''
            Activation link: {settings.HTTP_SCHEMA}://{settings.DOMAIN}{reverse('accounts:user_activate',
                                                                                args=(self.instance.username, ))}
        '''
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [self.instance.email],
            fail_silently=False,
        )
