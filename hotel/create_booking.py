import django
django.setup()

from django.contrib.auth.models import User
from management.models import Rooms, Reservation  # 假设 Room 和 Reservation 在 management 应用中定义

# 确保已存在用户和房间
user = User.objects.get(username='test')  # 替换为实际的用户名
room = Rooms.objects.get(id=3)  # 替换为实际的房间ID

# 创建预订
new_reservation = Reservation(
    guest=user,
    room=room,
    check_in='2024-02-12',
    check_out='2024-02-15'
)
new_reservation.save()
