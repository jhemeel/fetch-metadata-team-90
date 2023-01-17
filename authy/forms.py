from django import forms
from django.core.exceptions import ValidationError


from django_registration.forms import RegistrationForm
from .models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()





def ForbiddenUsers(value):
	forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
	'email', 'user', 'join', 'sql', 'static', 'python', 'delete']
	if value.lower() in forbidden_users:
		raise ValidationError('Invalid name for user, this is a reserverd word.')

def InvalidUser(value):
	if '@' in value or '+' in value or '-' in value:
		raise ValidationError('This is an Invalid user, Do not user these chars: @ , - , + ')

def UniqueEmail(value):
	if User.objects.filter(email__iexact=value).exists():
		raise ValidationError('User with this email already exists.')

def UniqueUser(value):
	if User.objects.filter(username__iexact=value).exists():
		raise ValidationError('User with this username already exists.')
class AuthyRegistrationForm(RegistrationForm):
	username = forms.CharField(widget=forms.TextInput(), max_length=30, required=True,)
	class Meta(RegistrationForm.Meta):
		model = User
		fields = ('username', 'email', 'password1')


	def __init__(self, *args, **kwargs):
		super(AuthyRegistrationForm, self).__init__(*args, **kwargs)
		self.fields['username'].validators.append(ForbiddenUsers)
		self.fields['username'].validators.append(InvalidUser)
		self.fields['username'].validators.append(UniqueUser)
	



# class SignupForm(forms.ModelForm):
# 	username = forms.CharField(widget=forms.TextInput(), max_length=30, required=True,)
# 	
# 	password = forms.CharField(widget=forms.PasswordInput())
# 	confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Confirm your password.")

# 	class Meta:

# 		model = User
# 		fields = ('username', 'email', 'password')

# 	def __init__(self, *args, **kwargs):
# 		super(SignupForm, self).__init__(*args, **kwargs)
# 		self.fields['username'].validators.append(ForbiddenUsers)
# 		self.fields['username'].validators.append(InvalidUser)
# 		self.fields['username'].validators.append(UniqueUser)
# 		self.fields['email'].validators.append(UniqueEmail)

# 	def clean(self):
# 		super(SignupForm, self).clean()
# 		password = self.cleaned_data.get('password')
# 		confirm_password = self.cleaned_data.get('confirm_password')

# 		if password != confirm_password:
# 			self._errors['password'] = self.error_class(['Passwords do not match. Try again'])
# 		return self.cleaned_data

class ChangePasswordForm(forms.ModelForm):
	id = forms.CharField(widget=forms.HiddenInput())
	old_password = forms.CharField(widget=forms.PasswordInput(), label="Old password", required=True)
	new_password = forms.CharField(widget=forms.PasswordInput(), label="New password", required=True)
	confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm new password", required=True)

	class Meta:
		model = User
		fields = ('id', 'old_password', 'new_password', 'confirm_password')

	def clean(self):
		super(ChangePasswordForm, self).clean()
		id = self.cleaned_data.get('id')
		old_password = self.cleaned_data.get('old_password')
		new_password = self.cleaned_data.get('new_password')
		confirm_password = self.cleaned_data.get('confirm_password')
		user = User.objects.get(pk=id)
		if not user.check_password(old_password):
			self._errors['old_password'] =self.error_class(['Old password do not match.'])
		if new_password != confirm_password:
			self._errors['new_password'] =self.error_class(['Passwords do not match.'])
		return self.cleaned_data
