from django.db import models
from django.utils.translation import gettext as _


class WorkingHours(models.Model):
    WEEKDAYS = (
        (1, _("Monday")),
        (2, _("Tuesday")),
        (3, _("Wednesday")),
        (4, _("Thursday")),
        (5, _("Friday")),
        (6, _("Saturday")),
        (7, _("Sunday")),
    )

    weekday = models.IntegerField(choices=WEEKDAYS, unique=True)
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    class Meta:
        ordering = ('weekday', 'from_hour')
        unique_together = ('weekday', 'from_hour', 'to_hour')
        verbose_name = 'Working hours'
        verbose_name_plural = 'Working hours'

    def __unicode__(self):
        return u'%s: %s - %s' % (self.get_weekday_display(),
                                 self.from_hour, self.to_hour)

    def __str__(self):
        return self.__unicode__()


class Location(models.Model):
    location = models.CharField(max_length=255, primary_key=True, unique=True, null=False)
    work_hours = models.ManyToManyField(WorkingHours, verbose_name="Working hours")

    def __str__(self):
        return self.location


class Registration(models.Model):
    number = models.IntegerField(primary_key=True, unique=True, null=False, verbose_name="Registration number")
    timestamp = models.TimeField(verbose_name="Registration time")  # auto_now_add=True

    class Meta:
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'

    def __str__(self):
        return str(self.number)


class Subscription(models.Model):
    number = models.IntegerField(primary_key=True, null=False, verbose_name="Subscription number")
    type = models.CharField(max_length=1, choices=(('A', 'A'), ('B', 'B'), ('C', 'C')), verbose_name="Subscription type")

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self):
        return str(self.number)


class Payment(models.Model):
    transaction_number = models.CharField(primary_key=True, max_length=20, null=False, verbose_name="Transaction number")
    amount = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Amount")
    card_type = models.CharField(max_length=1, choices=(('V', 'Visa'), ('M', 'Mastercard'), ('U', 'Uzcard')), verbose_name="Card type")

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return str(self.transaction_number)


class Deposit(models.Model):
    number = models.IntegerField(primary_key=True, null=False, verbose_name="Deposit number")
    amount = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Amount")
    currency = models.CharField(max_length=3, choices=(('UZS', 'UZS'), ('USD', 'USD'), ('EUR', 'EUR')), verbose_name="Currency")
    subscription_number = models.ForeignKey(Subscription, on_delete=models.CASCADE, verbose_name="Subscription number")

    class Meta:
        verbose_name = 'Deposit'
        verbose_name_plural = 'Deposits'

    def __unicode__(self):
        return u'%s: %s %s' % (self.number, self.amount, self.currency)

    def __str__(self):
        return self.__unicode__()


class Person(models.Model):
    ssn = models.CharField("SSN", max_length=20, primary_key=True, unique=True, null=False)
    name = models.CharField(max_length=255)
    age = models.IntegerField("Age", default=0)
    GENDER_CHOICES = (
        (None, "Choose gender"),
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField("Gender", max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'All people'


class Manager(Person):
    id = models.CharField("Employee ID", max_length=20, primary_key=True, unique=True, null=False)
    salary = models.IntegerField("Salary per year in $", default=0)
    working_hours = models.ManyToManyField(WorkingHours, verbose_name="Working hours")
    SENIORITY_LEVEL_CHOICES = (
        (None, "Choose seniority level"),
        ('L1', 'Junior'),
        ('L2', 'Middle'),
        ('L3', 'Senior'),
        ('L4', 'Lead'),
    )
    seniority_level = models.CharField("Seniority Level", max_length=2, choices=SENIORITY_LEVEL_CHOICES)


class Supplier(models.Model):
    retailer_name = models.CharField("Retailer name", max_length=20, primary_key=True, unique=True, null=False)
    product_name = models.CharField("Product name", max_length=20)
    product_type = models.CharField("Product type", max_length=20)

    def __str__(self):
        return self.retailer_name


class Coach(Person):
    licence_number = models.CharField("Licence number", max_length=20, primary_key=True, unique=True, null=False)
    salary = models.IntegerField("Salary per year in $", default=0, null=True)
    specialization = models.CharField("Specialization", max_length=255, null=True)

    class Meta:
        verbose_name = 'Coach'
        verbose_name_plural = 'Coaches'


class Gym(models.Model):
    name = models.CharField("Gym name", max_length=255)
    capacity = models.IntegerField("Gym capacity", default=0)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=False)
    coaches = models.ManyToManyField(Coach, verbose_name="Coaches")
    location = models.OneToOneField(Location, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Gym'
        verbose_name_plural = 'Gyms'


class Client(Person):
    account_number = models.CharField("Account number", max_length=20, primary_key=True, unique=True, null=False)
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, null=True)
    subscription = models.OneToOneField(Subscription, on_delete=models.SET_NULL, null=True)
    payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True)
    gym = models.ForeignKey(Gym, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}, {self.account_number}"


class Equipment(models.Model):
    serial_number = models.CharField(max_length=20, primary_key=True, unique=True, null=False)
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    gym = models.ForeignKey(Gym, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Training(models.Model):
    exercise_name = models.CharField(max_length=255, primary_key=True, unique=True, null=False)
    work_hours = models.ManyToManyField(WorkingHours, verbose_name="Working hours")
    duration = models.IntegerField("Duration in minutes")
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.exercise_name


class Rank(models.Model):
    name = models.CharField(max_length=255)
    exercise_name = models.ManyToManyField(Training, verbose_name="Exercises")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name


class WorkoutPlan(models.Model):
    id = models.AutoField(primary_key=True)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, null=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False)
    training = models.ForeignKey(Training, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.coach}, {self.client}, {self.training}"


class SportsWear(models.Model):
    brand_name = models.CharField(max_length=20, unique=True, null=False)
    price = models.IntegerField(default=0)

    SIZES = (
        (None, "Choose size"),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra large'),
        ('XLL', '2X large'),
    )
    size = models.CharField("Size", max_length=3, choices=SIZES)
    type = models.CharField(max_length=255)
    sells = models.ForeignKey(Gym, on_delete=models.CASCADE, null=False)  # Sells at Gym
    provider = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.brand_name}, {self.price}, {self.size}, {self.type}"


class Nutrition(models.Model):
    product_id = models.CharField(max_length=20, primary_key=True, unique=True, null=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(default=0)
    deals = models.ForeignKey(Gym, on_delete=models.CASCADE, null=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.product_id}, {self.name}, {self.price}, {self.deals}"


class Purchase(models.Model):
    brand_name = models.ForeignKey(SportsWear, on_delete=models.CASCADE, null=False)
    deposit_number = models.ForeignKey(Deposit, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.brand_name}, {self.deposit_number}"


class Order(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=False)
    retailer_name = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.manager}, {self.retailer_name}"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
