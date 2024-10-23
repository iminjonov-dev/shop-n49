from pip._internal.utils._jaraco_text import _
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(models.Model):
    title = models.CharField(max_length=50, unique=50)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'
        db_table = 'category'

    def __str__(self):
        return self.title

class Product(BaseModel):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5


    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='products',null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField(default=0)
    rating = models.PositiveSmallIntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value, null=True, blank=True)

    discount = models.PositiveSmallIntegerField(null=True, blank=True)

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return None

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

    def __str__(self):
        return self.name


    class Meta:
      db_table = 'product'

class Comment(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    is_private = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.name} - {self.created_at}'
    class Meta:
        db_table = 'comment'

class Order(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=13)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.phone}'


class AbstractUser(AbstractBaseUser, PermissionsMixin):

      username_validator  = UnicodeUsernameValidator()

      username = models.CharField(
          _("username"),
          max_length=150,
          unique=True,
          help_text=_(
              "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. "
          ),
          validators=[username_validator],
          error_messages={
              "unique": _("A user with that username already exists."),
          },
      )

      first_name = models.CharField( _("first name"), max_length=150, blank=True)
      last_name = models.CharField( _('last name'), max_length=150, blank=True)
      email = models.EmailField(_('email address'), blank=True)
      is_staff = models.BooleanField(
          _("staff status"),
          default=False,
          help_text=_("Designates whether the user can log into this admin site."),
      )
      is_active = models.BooleanField(
          _("active"),
          default=True,
          help_text=_(
              "Designates whether this user should be treated as active. "
              "Unselect this instead of deleting accounts."
          ),
      )

      date_joined = models.DateTimeField(_("date joined"), default=timezone.now())

      objects = UserManager()

      EMAIL_FIELD = 'email'
      USERNAME_FIELD = 'username'
      REQUIRED_FIELDS = ['email']


      class Meta:
          verbose_name = _("user")
          verbose_name_plural = _("users")
          abstract = True


      def clean(self):
          super().clean()
          self.email = self.__class__.objects.normalize_email(self.email)

