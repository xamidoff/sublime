from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Kategoriya')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Rasm')
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='subcategory', verbose_name='Kategoriya')


    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' --> '.join(full_path[::-1])

    def __repr__(self):
        return f"Kategoriya: pk={self.pk} - title={self.title}"

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Tovar nomi')

    brand = models.CharField(max_length=255, verbose_name='Brandi')
    performance = models.TextField(default='Hozircha ma\'lumot mavjud emas!', verbose_name='Tehnik tavsifi')
    colour = models.CharField(max_length=255, verbose_name='Rangi')
    memory = models.CharField(max_length=255, verbose_name='Xotirasi')
    camera = models.CharField(max_length=255, verbose_name='Kamera')
    battery = models.CharField(max_length=255, verbose_name='Batareya hajmi')

    manufacture_date = models.IntegerField(verbose_name='Ishlab chiqarilgan yili')
    price = models.FloatField(verbose_name='Sotiladigan Narxi')
    discount = models.FloatField(verbose_name='Chegirma', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Kiritilgan vaqti')
    quantity = models.IntegerField(default=0, verbose_name='Soni')
    description = models.TextField(default='Hozircha ma\'lumot mavjud emas!', verbose_name='Malumot')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='products',
                                 verbose_name='Kategoriya')
    slug = models.SlugField(unique=True, null=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_first_photo(self):
        if self.images:
            try:
                return self.images.all()[0].image.url
            except:
                return 'https://us.123rf.com/450wm/yehorlisnyi/yehorlisnyi2104/yehorlisnyi210400016/167492439-no-photo-or-blank-image-icon-loading-images-or-missing-image-mark-image-not-available-or-image-comin.jpg?ver=6'
        else:
            return 'https://us.123rf.com/450wm/yehorlisnyi/yehorlisnyi2104/yehorlisnyi210400016/167492439-no-photo-or-blank-image-icon-loading-images-or-missing-image-mark-image-not-available-or-image-comin.jpg?ver=6'


    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Tovar: pk={self.pk}, title={self.title}, price={self.price}"

    class Meta:
        verbose_name = 'Tovar'
        verbose_name_plural = 'Tovarlar'

class Gallery(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Rasm')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Rasm'
        verbose_name_plural = 'Rasmlar'

class Review(models.Model):
    text = models.TextField(verbose_name='Sharhlar')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Avtor')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Chop etilgan vaqti')
    publish = models.BooleanField(default=True, verbose_name='Chop etish')

    def __str__(self):
        return self.text[:20]

    class Meta:
        verbose_name = 'Sharh'
        verbose_name_plural = 'Sharhlar'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Xaridor'
        verbose_name_plural = 'Xaridorlar'

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    shipping = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'

    @property
    def get_cart_total_price(self):
        order_product = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_product])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_product = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_product])
        return total_quantity


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    addet_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Buyurtma berilgan mahsulot'
        verbose_name_plural = 'Buyurtma berilgan mahsulotlar'

    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price

class ShippinAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Yetkazib berish manzili'
        verbose_name_plural = 'Yetkazib berish manzillari'