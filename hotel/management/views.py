from django.shortcuts import render ,redirect, get_object_or_404
from django.http import HttpResponse , HttpResponseRedirect
from .models import Hotels,Rooms,Reservation, Chats
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime
from django.utils import timezone
# Create your views here.

@login_required(login_url='/user')
def rate_booking(request, booking_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        #booking_id = request.POST.get('booking_id')
        try:
            booking = Reservation.objects.get(id=booking_id)
            # 確保評分在合理範圍內並且訂單尚未評分
            if 1 <= int(rating) <= 5 and booking.rating is None:
                booking.rating = rating
                booking.save()
                messages.success(request, "Thank you for your rating!")
            else:
                messages.warning(request, "Invalid rating or booking already rated.")
        except Reservation.DoesNotExist:
            messages.error(request, "Booking does not exist.")
        return redirect('dashboard')
    return HttpResponse("Invalid request", status=400)


#homepage
def homepage(request):
    all_location = Hotels.objects.values_list('location','id').distinct().order_by()
    if request.method =="POST":
        try:
            print(request.POST)
            hotel = Hotels.objects.all().get(id=int(request.POST['search_location']))
            rr = []
            
            #for finding the reserved rooms on this time period for excluding from the query set
            for each_reservation in Reservation.objects.all():
                if str(each_reservation.check_in) < str(request.POST['cin']) and str(each_reservation.check_out) < str(request.POST['cout']):
                    pass
                elif str(each_reservation.check_in) > str(request.POST['cin']) and str(each_reservation.check_out) > str(request.POST['cout']):
                    pass
                else:
                    rr.append(each_reservation.room.id)
                
            room = Rooms.objects.all().filter(hotel=hotel,capacity__gte = int(request.POST['capacity'])).exclude(id__in=rr)
            if len(room) == 0:
                messages.warning(request,"Sorry No Rooms Are Available on this time period")
            data = {'rooms':room,'all_location':all_location,'flag':True}
            response = render(request,'index.html',data)
        except Exception as e:
            messages.error(request,e)
            response = render(request,'index.html',{'all_location':all_location})


    else:
        
        
        data = {'all_location':all_location}
        response = render(request,'index.html',data)
    return HttpResponse(response)

#about
def aboutpage(request):
    return HttpResponse(render(request,'about.html'))

#contact page
def contactpage(request):
    return HttpResponse(render(request,'contact.html'))

#user sign up
def user_sign_up(request):
    if request.method =="POST":
        user_name = request.POST['username']
        
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.warning(request,"Password didn't matched")
            return redirect('userloginpage')
        
        try:
            if User.objects.all().get(username=user_name):
                messages.warning(request,"Username Not Available")
                return redirect('userloginpage')
        except:
            pass
            

        new_user = User.objects.create_user(username=user_name,password=password1)
        new_user.is_superuser=False
        new_user.is_staff=False
        new_user.save()
        messages.success(request,"Registration Successfull")
        return redirect("userloginpage")
    return HttpResponse('Access Denied')
#staff sign up
def staff_sign_up(request):
    if request.method =="POST":
        user_name = request.POST['username']
        
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.success(request,"Password didn't Matched")
            return redirect('staffloginpage')
        try:
            if User.objects.all().get(username=user_name):
                messages.warning(request,"Username Already Exist")
                return redirect("staffloginpage")
        except:
            pass
        
        new_user = User.objects.create_user(username=user_name,password=password1)
        new_user.is_superuser=False
        new_user.is_staff=True
        new_user.save()
        messages.success(request," Staff Registration Successfull")
        return redirect("staffloginpage")
    else:

        return HttpResponse('Access Denied')
#user login and signup page
def user_log_sign_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pswd']

        user = authenticate(username=email,password=password)
        try:
            if user.is_staff:
                
                messages.error(request,"Incorrect username or Password")
                return redirect('staffloginpage')
        except:
            pass
        
        if user is not None:
            login(request,user)
            messages.success(request,"successful logged in")
            print("Login successfull")
            return redirect('homepage')
        else:
            messages.warning(request,"Incorrect username or password")
            return redirect('userloginpage')

    response = render(request,'user/userlogsign.html')
    return HttpResponse(response)

#logout for admin and user 
def logoutuser(request):
    if request.method =='GET':
        logout(request)
        messages.success(request,"Logged out successfully")
        print("Logged out successfully")
        return redirect('homepage')
    else:
        print("logout unsuccessfull")
        return redirect('userloginpage')

#staff login and signup page
def staff_log_sign_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)
        
        if user.is_staff:
            login(request,user)
            return redirect('staffpanel')
        
        else:
            messages.success(request,"Incorrect username or password")
            return redirect('staffloginpage')
    response = render(request,'staff/stafflogsign.html')
    return HttpResponse(response)

#staff panel page
@login_required(login_url='/staff')
def panel(request):
    
    if request.user.is_staff == False:
        return HttpResponse('Access Denied')
    
    rooms = Rooms.objects.all()
    total_rooms = len(rooms)
    available_rooms = len(Rooms.objects.all().filter(status='1'))
    unavailable_rooms = len(Rooms.objects.all().filter(status='2'))
    reserved = len(Reservation.objects.all())

    hotel = Hotels.objects.values_list('location','id').distinct().order_by()

    response = render(request,'staff/panel.html',{'location':hotel,'reserved':reserved,'rooms':rooms,'total_rooms':total_rooms,'available':available_rooms,'unavailable':unavailable_rooms})
    return HttpResponse(response)

#for editing room information
@login_required(login_url='/staff')
def edit_room(request):
    if request.user.is_staff == False:   
        return HttpResponse('Access Denied')
    if request.method == 'POST' and request.user.is_staff:
        print(request.POST)
        old_room = Rooms.objects.all().get(id= int(request.POST['roomid']))
        hotel = Hotels.objects.all().get(id=int(request.POST['hotel']))
        old_room.room_type  = request.POST['roomtype']
        old_room.capacity   =int(request.POST['capacity'])
        old_room.price      = int(request.POST['price'])
        old_room.size       = int(request.POST['size'])
        old_room.hotel      = hotel
        old_room.status     = request.POST['status']
        old_room.room_number=int(request.POST['roomnumber'])

        old_room.save()
        messages.success(request,"Room Details Updated Successfully")
        return redirect('staffpanel')
    else:
    
        room_id = request.GET['roomid']
        room = Rooms.objects.all().get(id=room_id)
        response = render(request,'staff/editroom.html',{'room':room})
        return HttpResponse(response)

#for adding room
@login_required(login_url='/staff')
def add_new_room(request):
    if request.user.is_staff == False:
        return HttpResponse('Access Denied')
    if request.method == "POST":
        total_rooms = len(Rooms.objects.all())
        new_room = Rooms()
        hotel = Hotels.objects.all().get(id = int(request.POST['hotel']))
        print(f"id={hotel.id}")
        print(f"name={hotel.name}")


        new_room.roomnumber = total_rooms + 1
        new_room.room_type  = request.POST['roomtype']
        new_room.capacity   = int(request.POST['capacity'])
        new_room.size       = int(request.POST['size'])
        new_room.capacity   = int(request.POST['capacity'])
        new_room.hotel      = hotel
        new_room.status     = request.POST['status']
        new_room.price      = request.POST['price']

        new_room.save()
        messages.success(request,"New Room Added Successfully")
    
    return redirect('staffpanel')

#booking room page
@login_required(login_url='/user')
def book_room_page(request):
    room = Rooms.objects.all().get(id=int(request.GET['roomid']))
    return HttpResponse(render(request,'user/bookroom.html',{'room':room}))

#For booking the room
@login_required(login_url='/user')
def book_room(request):
    
    if request.method =="POST":

        room_id = request.POST['room_id']
        
        room = Rooms.objects.all().get(id=room_id)
        #for finding the reserved rooms on this time period for excluding from the query set
        for each_reservation in Reservation.objects.all().filter(room = room):
            if str(each_reservation.check_in) < str(request.POST['check_in']) and str(each_reservation.check_out) < str(request.POST['check_out']):
                pass
            elif str(each_reservation.check_in) > str(request.POST['check_in']) and str(each_reservation.check_out) > str(request.POST['check_out']):
                pass
            else:
                messages.warning(request,"Sorry This Room is unavailable for Booking")
                return redirect("homepage")
            
        current_user = request.user
        total_person = int( request.POST['person'])
        booking_id = str(room_id) + str(datetime.datetime.now())

        reservation = Reservation()
        room_object = Rooms.objects.all().get(id=room_id)
        room_object.status = '2'
        
        user_object = User.objects.all().get(username=current_user)

        reservation.guest = user_object
        reservation.room = room_object
        person = total_person
        reservation.check_in = request.POST['check_in']
        reservation.check_out = request.POST['check_out']

        reservation.save()

        messages.success(request,"Congratulations! Booking Successfull")

        return redirect("homepage")
    else:
        return HttpResponse('Access Denied')

def handler404(request):
    return render(request, '404.html', status=404)

@login_required(login_url='/staff')   
def view_room(request):
    room_id = request.GET['roomid']
    room = Rooms.objects.all().get(id=room_id)

    reservation = Reservation.objects.all().filter(room=room)
    return HttpResponse(render(request,'staff/viewroom.html',{'room':room,'reservations':reservation}))

@login_required(login_url='/user')
def user_bookings(request):
    if request.user.is_authenticated == False:
        return redirect('userloginpage')
    user = User.objects.all().get(id=request.user.id)
    print(f"request user id ={request.user.id}")
    bookings = Reservation.objects.all().filter(guest=user)
    if not bookings:
        messages.warning(request,"No Bookings Found")
    return HttpResponse(render(request,'user/mybookings.html',{'bookings':bookings}))

@login_required(login_url='/staff')
def add_new_location(request):
    if request.method == "POST" and request.user.is_staff:
        owner = request.POST['new_owner']
        location = request.POST['new_city']
        state = request.POST['new_state']
        country = request.POST['new_country']
        
        hotels = Hotels.objects.all().filter(location = location , state = state)
        if hotels:
            messages.warning(request,"Sorry City at this Location already exist")
            return redirect("staffpanel")
        else:
            new_hotel = Hotels()
            new_hotel.owner = owner
            new_hotel.location = location
            new_hotel.state = state
            new_hotel.country = country
            new_hotel.save()
            messages.success(request,"New Location Has been Added Successfully")
            return redirect("staffpanel")

    else:
        return HttpResponse("Not Allowed")

@login_required(login_url='/user')
def delete_booking(request, booking_id):
    if request.method == 'POST':
        try:
            booking = Reservation.objects.get(id=booking_id)
            # Add any permission checks here to ensure the user can delete this booking
            booking.delete()
            messages.success(request, "Booking has been successfully deleted.")
        except Reservation.DoesNotExist:
            messages.error(request, "Booking does not exist.")
        except Exception as e:
            messages.error(request, f"An error occurred while deleting the booking: {str(e)}")
    return redirect('dashboard')   

#for showing all bookings to staff
@login_required(login_url='/staff')
def all_bookings(request):
   
    bookings = Reservation.objects.all()
    if not bookings:
        messages.warning(request,"No Bookings Found")
    return HttpResponse(render(request,'staff/allbookings.html',{'bookings':bookings}))
    

def sales(request, this_total = 0, last_total = 0, this_rate = 0, last_rate = 0, context = {}):
    this_month = datetime.date.today().month
    this_year = datetime.date.today().year
    last_month = this_month - 1
    last_year = this_year
    if last_month < 1:
        last_month = 12
        last_year -= 1
    
    
    try:
        this_sales = Reservation.objects.filter( check_in__month = this_month ).filter( check_in__year = this_year )
        last_sales = Reservation.objects.filter( check_in__month = last_month ).filter( check_in__year = last_year )
        
        for sale in this_sales:
            this_total += sale.room.price

        for sale in last_sales:
            last_total += sale.room.price

        this_count = 0
        this_rate_sum = 0
        for sale in this_sales:
            if( sale.rating ):
                this_rate_sum += sale.rating
                this_count += 1
        this_rate = this_rate_sum / this_count

        last_count = 0
        last_rate_sum = 0
        for sale in last_sales:
            if( sale.rating ):
                last_rate_sum += sale.rating
                last_count += 1
        last_rate = last_rate_sum / last_count

        hotels = Hotels.objects.all()
        label = []
        datapoints_1 = []
        for hotel in hotels:
            label.append( hotel.location )
            data = {}
            sum_location = Reservation.objects.filter( room__hotel__location = hotel.location )
            sum  = 0
            for item in sum_location:
                sum += item.room.price
            data['y'] = sum 
            data['label'] = hotel.location 
            datapoints_1.append( data )

        context = {
            'this_total': this_total,
            'last_total': last_total,
            'this_sales':this_sales,
            'last_sales':last_sales,
            'this_rate':this_rate,
            'last_rate':last_rate,
            'hotels': hotels,
            'label': label,
            'datapoints_1': datapoints_1,
        }

    except:
        pass

    return render(request,'staff/sales.html',context)

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Reservation


def chat_box(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == 'POST':
        msg_content = request.POST.get('msg_content')
        if msg_content:
            new_msg = Chats(
                content=msg_content,
                reservation=reservation,
                sender=request.user,
                timestamp=timezone.now()
            )
            new_msg.save()
            messages.success(request, 'Message submitted successfully!')
        return redirect('chat_box', reservation_id=reservation_id)  # Redirect back to the chat box

    chats_list = reservation.messages.all()
    return render(request, 'user/chat.html', {'reservation': reservation, 'chats': chats_list})


@login_required(login_url='/staff')
def staff_chat_box(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == 'POST':
        msg_content = request.POST.get('msg_content')
        if msg_content:
            new_msg = Chats(
                content=msg_content,
                reservation=reservation,
                sender=request.user,
                timestamp=timezone.now()
            )
            new_msg.save()
            messages.success(request, 'Message submitted successfully!')
        return redirect('staff_chat_box', reservation_id=reservation_id)

    chats_list = reservation.messages.all()
    return render(request, 'staff/chat.html', {'reservation': reservation, 'chats': chats_list})
