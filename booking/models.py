from django.db import models


### Fintess Booking Models and Cancelled Booking Model for Instructor/studio-side
class FitnessClass(models.Model):
    CLASS_TYPES = [
        ('Yoga', 'Yoga'),
        ('Zumba', 'Zumba'),
        ('HIIT', 'HIIT')
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(choices=CLASS_TYPES, max_length=20)
    date_time = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    total_slots = models.PositiveIntegerField()
    available_slots = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return f"{self.name} at {self.date_time} - {self.status}"

### Booking Model
class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()

    def __str__(self):
        return f"{self.client_name} - {self.fitness_class}"
    

### Cancelled Booking Model for Client side
class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled')
    ]

    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.client_name} - {self.fitness_class} - {self.status}"

