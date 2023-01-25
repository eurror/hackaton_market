from django.core.mail import send_mail


def send_activation_code(email, activation_code):
    message = f'Congratulations! Вы зарегистрировались' \
              f' на нашем сайте. Активируйте аккаунт' \
              f'отправив нам этот код {activation_code}'
    send_mail('Активация аккаунта', message, 'edgarpo0401@gmail.com', [email])
