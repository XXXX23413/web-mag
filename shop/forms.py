from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CartUpdateForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        max_value=99,
        label='Количество',
        error_messages={
            'min_value':'Количество меньше 1',
            'max_value':'Количество не может быть больше 99',
            'invalid':'Введите число',
        }
    )

class OrderForm(forms.Form):
    customer_name = forms.CharField(
        max_length=100,
        label='Имя',
        error_messages={'required':'Укажите имя'}
    )
    phone = forms.CharField(
        max_length=20,
        label='Телефон',
        error_messages={'required': 'Укажите телефон'}
    )
    email = forms.EmailField(
        label ='Email',
        error_messages={'invalid':'Введите корректный email'}
    )
    city = forms.CharField(max_length=100,required=False,label='Город')
    address = forms.CharField(
        widget=forms.Textarea,
        label='Адрес доставки',
        error_messages={'required':'Укажите адрес'}
    )
    comment = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label='Комментарий'
    )

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True,label='Email')

    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Повторите пароль'    