from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser, PermissionsMixin
)
import jwt
from datetime import datetime, timedelta
from django.conf import settings 
from .Manager import UserManager


class Author(AbstractBaseUser, PermissionsMixin):
    
    # Каждому пользователю нужен понятный человеку уникальный идентификатор,
    # который мы можем использовать для предоставления User в пользовательском
    # интерфейсе. Мы так же проиндексируем этот столбец в базе данных для
    # повышения скорости поиска в дальнейшем.
    email=models.EmailField(db_index=True,verbose_name='email', unique=True)


        
    # Когда пользователь более не желает пользоваться нашей системой, он может
    # захотеть удалить свой аккаунт. Для нас это проблема, так как собираемые
    # нами данные очень ценны, и мы не хотим их удалять :) Мы просто предложим
    # пользователям способ деактивировать учетку вместо ее полного удаления.
    # Таким образом, они не будут отображаться на сайте, но мы все еще сможем
    # далее анализировать информацию.
    is_active = models.BooleanField(default=True)

    # Этот флаг определяет, кто может войти в административную часть нашего
    # сайта. Для большинства пользователей это флаг будет ложным.
    is_staff = models.BooleanField(default=False,verbose_name='Personal')

    # Временная метка создания объекта.
    created_at = models.DateTimeField(auto_now_add=True)

    # Временная метка показывающая время последнего обновления объекта.
    updated_at = models.DateTimeField(auto_now=True)

    # Дополнительный поля, необходимые Django
    # при указании кастомной модели пользователя.

    # Свойство USERNAME_FIELD сообщает нам, какое поле мы будем использовать
    # для входа в систему. В данном случае мы хотим использовать почту.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Сообщает Django, что определенный выше класс UserManager
    # должен управлять объектами этого типа.
    objects = UserManager()
    
    
    
    class Meta:
        ordering = ['id']
        verbose_name='пользователь'
        verbose_name_plural='Пользователи'

    def __str__(self):
        return "{}".format(self.email)

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова Author.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        """
        return self.email

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        return self.email

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%S'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


class WeddingName(models.Model):
    name = models.CharField(max_length=255,verbose_name="Чей праздник?")
    description = models.TextField(verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата записи в базу данных')
    WeddingDate = models.DateTimeField(verbose_name='Дата праздника')

    class Meta:
        ordering = ['created_at']
        verbose_name='праздник'
        verbose_name_plural='Праздники'

    def __str__(self):
        return "{}".format(self.name)



class Wedding(models.Model):
    WeddingName = models.ForeignKey(WeddingName, verbose_name='Чей праздник', related_name='related_orders', on_delete=models.CASCADE)
    name = models.CharField(max_length=255,verbose_name="Полное имя")
    coming = models.BooleanField(default=False, verbose_name="я приду")
    spouse = models.BooleanField(default=False, verbose_name="я приду с женой")
    I_cant_come = models.BooleanField(default=False, verbose_name="К сожалению, я не могу прийти")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата заявкий')
    class Meta:
        ordering = ['created_at']
        verbose_name='приглашение'
        verbose_name_plural='приглашение'

    def __str__(self):
        return "{}".format(self.name)