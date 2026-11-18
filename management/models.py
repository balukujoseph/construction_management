from django.db import models

class Client(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    
    first_name = models.CharField(max_length=20, verbose_name=" Client First Name") 
    last_name = models.CharField(max_length=20, verbose_name=" Client Last Name")
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True, default='')
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)

    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name    


class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    department = models.CharField(max_length=50)
    address = models.TextField(blank=True, default='')
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Material(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)   



    def __str__(self):
        return self.name    

class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name         
 
    


