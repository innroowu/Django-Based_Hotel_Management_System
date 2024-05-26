from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Hotels(models.Model):
    #h_id,h_name,owner ,location,rooms
    name = models.CharField(max_length=30,default="test")
    owner = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    state = models.CharField(max_length=50,default="Taipei")
    country = models.CharField(max_length=50,default="Taiwan")
    def __str__(self):
        return self.name


class Rooms(models.Model):
    ROOM_STATUS = ( 
    ("1", "available"), 
    ("2", "not available"),    
    ) 

    ROOM_TYPE = ( 
    ("1", "premium"), 
    ("2", "deluxe"),
    ("3","basic"),    
    ) 

    #type,no_of_rooms,capacity,prices,Hotel
    room_type = models.CharField(max_length=50,choices = ROOM_TYPE)
    capacity = models.IntegerField()
    price = models.IntegerField()
    size = models.IntegerField()
    hotel = models.ForeignKey(Hotels, on_delete = models.CASCADE)
    status = models.CharField(choices =ROOM_STATUS,max_length = 15)
    roomnumber = models.IntegerField()
    def __str__(self):
        return self.hotel.name

class Reservation(models.Model):

    check_in = models.DateField(auto_now =False)
    check_out = models.DateField()
    room = models.ForeignKey(Rooms, on_delete = models.CASCADE)
    guest = models.ForeignKey(User, on_delete= models.CASCADE)
    
    booking_id = models.CharField(max_length=100,default="null")
    rating = models.IntegerField(null=True, blank=True)  # 允許空值並在表單中可選

    # message = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.guest.username

class Chats(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f'{self.sender.username} - {self.timestamp}'


class SaleReport(models.Model):
    def __init__(self):
        self.__this_month = datetime.date.today().month
        self.__this_year = datetime.date.today().year
        self.__last_month = self.__get_last_mon()
        self.__last_year = self.__get_last_year()
        self.__this_sales = Reservation.objects.filter( check_in__month = self.__this_month ).filter( check_in__year = self.__this_year )
        self.__last_sales = Reservation.objects.filter( check_in__month = self.__last_month ).filter( check_in__year = self.__last_year )
        self.__hotels = Hotels.objects.all()
        self.__label = self.__get_label()
        self.__datapoints_1 = self.__get_datapoint()
        self.__this_total = self.__get_this_total()
        self.__last_total = self.__get_last_total()
        self.__this_rate = self.__get_this_rate()
        self.__last_rate = self.__get_last_rate()

    def __get_last_mon(self):
        last_month = self.__this_month-1
        if last_month < 1:
            last_month = 12
        return last_month

    def __get_last_year(self):
        last_year = self.__this_year
        if self.__this_month-1 < 1:
            last_year -= 1
        return last_year

    def __get_this_total(self):
        this_total = 0
        for sale in self.__this_sales:
            this_total += sale.room.price
        return this_total

    def __get_last_total(self):
        last_total = 0
        for sale in self.__last_sales:
            last_total += sale.room.price
        return last_total


    def __get_this_rate(self):
        this_count = 0
        this_rate_sum = 0
        for sale in self.__this_sales:
            if( sale.rating ):
                this_rate_sum += sale.rating
                this_count += 1
        this_rate = this_rate_sum / this_count
        return this_rate

    def __get_last_rate(self):
        last_count = 0
        last_rate_sum = 0
        for sale in self.__last_sales:
            if( sale.rating ):
                last_rate_sum += sale.rating
                last_count += 1
        last_rate = last_rate_sum / last_count
        return last_rate


    def __get_label(self):
        label = []
        for hotel in self.__hotels:
            label.append( hotel.location )
        return label

    def __get_datapoint(self):
        datapoints_1 = []
        for hotel in self.__hotels:
            data = {}
            sum_location = Reservation.objects.filter( room__hotel__location = hotel.location )
            sum  = 0
            for item in sum_location:
                sum += item.room.price
            data['y'] = sum 
            data['label'] = hotel.location 
            datapoints_1.append( data )
        return datapoints_1

    def get_context(self):
        context = {
            'this_total': self.__this_total,
            'last_total': self.__last_total,
            'this_sales': self.__this_sales,
            'last_sales': self.__last_sales,
            'this_rate': self.__this_rate,
            'last_rate': self.__last_rate,
            'hotels': self.__hotels,
            'label': self.__label,
            'datapoints_1': self.__datapoints_1,
        }
        return context