from django.shortcuts import render, redirect  
from myapp.forms import EmployeeForm  
# from myapp.models import Employee, User  
from myapp.models import Employee, User 
# from django.contrib.auth.models import User
from django.db import connection

def complex_query():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM my_table WHERE condition = %s", [value])
        results = cursor.fetchall()
    return results

# Create your views here.  
# code cũ 
# def addnew(request):  
#     # print(request)  # In ra thông tin của request
#     # print(request.method)  # In ra phương thức của request (POST, GET, ...)
#     # print(request.POST)  # In ra các dữ liệu gửi lên từ phương thức POST
#     # print(request.GET)  # In ra các dữ liệu truyền qua URL từ phương thức GET
#     print(request.POST.get('name'))  # In ra giá trị của tham số 'name'
#     print(request.POST.get('email'))  # In ra giá trị của tham số 'email'
#     print(request.POST.get('contact'))  # In ra giá trị của tham số 'contact'

#     if request.method == "POST":  
#         form = EmployeeForm(request.POST)  
#         if form.is_valid():  
#             try:  
#                 form.save()  
#                 return redirect('/')  
#             except:  
#                 pass
#     else:  
#         form = EmployeeForm()  
#     return render(request,'index.html',{'form':form})  

# code mới dùng query mysql 

from django.contrib.auth.decorators import login_required
@login_required
def addnew(request):
    # user_id = request.session.get('user_id')
    # if user_id:
        # Người dùng đã đăng nhập
        # Thực hiện các hành động sau khi đăng nhập thành công
        
        # trang index 
    if request.method == "POST":
        form = EmployeeForm(request.POST) # (1)
        if form.is_valid(): # (2) , 2 dòng này chỉ dùng form để kiểm tra dữ liệu gửi lên có ok hay không thôi 
            # => vậy là ta cũng khai báo form , nhưng chỉ dùng nó để kiểm tra dữ liệu là chủ yếu 
            # còn lại vẫn có thể tùy biến bằng câu lệnh query mysql 
            try:
                with connection.cursor() as cursor:
                    # Thực hiện lệnh INSERT
                    cursor.execute("INSERT INTO tblemployee (name, email, contact) VALUES (%s, %s, %s)",
                                [request.POST.get('name'), request.POST.get('email'), request.POST.get('contact')])
                return redirect('/')
            except:
                pass
    else:
        form = EmployeeForm()

    user = User.objects.get(id=user_id)
    return render(request, 'index.html', {'form': form,'user': user})
        # trang index 

    # else:
        # Người dùng chưa đăng nhập
        # Thực hiện các hành động khi chưa đăng nhập
    # return redirect('login')
 
def index(request):  
    print ('day la show')
    employees = Employee.objects.all()  
    return render(request,"show.html",{'employees':employees})  
 
#  code cũ 
# def edit(request, id):  
#     employee = Employee.objects.get(id=id)
#     print ('Day la id cua result',id);  
#     return render(request,'edit.html', {'employee':employee})  


def edit(request, id):
    print('Đây là id của result:', id)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tblemployee WHERE id = %s", [id])
        columns = [col[0] for col in cursor.description]  # Lấy tên các cột . Code như thế này để cho employee chứa key để khi xuống html in ra được
        employee = dict(zip(columns, cursor.fetchone()))  # Tạo từ điển từ kết quả truy vấn .  
        print(employee)
    return render(request, 'edit.html', {'employee': employee}) # đi đến edit.html và truyền biến employee với tên là employee ('employee') 

# code cũ 
# def update(request, id):  
#     employee = Employee.objects.get(id=id)  
#     form = EmployeeForm(request.POST, instance = employee)  
#     if form.is_valid():  
#         form.save()  
#         return redirect("/")  
#     return render(request, 'edit.html', {'employee': employee})  

def update(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tblemployee WHERE id = %s", [id])
        employee = cursor.fetchone()
        form = EmployeeForm(request.POST, initial=dict(zip(cursor.description, employee)))
        if form.is_valid():
            # Lấy dữ liệu từ form sau khi đã kiểm tra hợp lệ
            data = form.cleaned_data
            # Thực hiện câu lệnh UPDATE
            cursor.execute("UPDATE tblemployee SET name = %s, email = %s, contact = %s WHERE id = %s",
                           [data['name'], data['email'], data['contact'], id])
            return redirect("/")
    return render(request, 'edit.html', {'employee': employee, 'form': form})

# code cũ 
# def destroy(request, id):  
    # employee = Employee.objects.get(id=id)  
    # employee.delete()  
    # return redirect("/")  

def destroy(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM tblemployee WHERE id = %s", [id])
        return redirect("/")

def test_ajax2(request,id):
    print ('test ajax')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tblemployee WHERE id = %s", [id])
        columns = [col[0] for col in cursor.description] 
        employee = dict(zip(columns, cursor.fetchone()))  
        print(employee)
    return render(request, 'test_ajax.html',{'employee': employee})

from django.http import JsonResponse
def test_ajax(request):
    if request.method == "POST":
        id = request.POST.get('id')
        print (id)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tblemployee WHERE id = %s", [id])
            print (id)
            columns = [col[0] for col in cursor.description]
            employee = dict(zip(columns, cursor.fetchone()))
            return JsonResponse(employee)  # Trả về dữ liệu nhân viên dưới dạng JSON
    return render(request, 'test_ajax.html')


# user 
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as user_login
import bcrypt

# register 
from django.contrib.auth.hashers import make_password # mã hóa mật khẩu 
def register(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Kiểm tra các giá trị bắt buộc
        if not fullname or not email or not password:
            error_message = "Vui lòng điền đầy đủ thông tin."
            return render(request, 'user/register.html', {'error_message': error_message})

        # Kiểm tra email đã tồn tại
        if User.objects.filter(email=email).exists():
            error_message = "Email đã được sử dụng."
            return render(request, 'user/register.html', {'error_message': error_message})

        try:
             # Mã hóa mật khẩu
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO tbuser (fullname, email, password) VALUES (%s, %s, %s)",
                               [fullname, email, hashed_password])
            success_message = "Đăng kí thành công !"
            return render(request, 'user/register.html', {'success_message': success_message})
        
        except:
            error_message = "Đã xảy ra lỗi khi đăng ký."
            return render(request, 'user/register.html', {'error_message': error_message})
    else:
        return render(request, 'user/register.html')
    
# login 
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        print (email)
        password = request.POST['password']
        user = None 
        # Kiểm tra xem email có tồn tại trong database không
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'user/login.html', {'error_message': 'Email không tồn tại'})
        # Kiểm tra mật khẩu
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # Đăng nhập thành công, tạo session
            # request.session['user_id'] = user.id
            print ('ok')
            user_login(request, user)
            print (user.id)
            return redirect('/')
        else:
            return render(request, 'user/login.html', {'error_message': 'Sai mật khẩu'})
    else:
        return render(request, 'user/login.html')

# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request, user)
#             # Đăng nhập thành công, chuyển hướng đến trang khác
#         else:
#             # Sai email hoặc mật khẩu, hiển thị thông báo lỗi
#     else:
#         # Hiển thị form đăng nhập


# logout 
from django.contrib.auth import logout as user_logout
def logout(request):
    # # Xóa session của người dùng
    # # request.session.clear()
    # auth_logout(request) # đổi lại tên vì nếu vẫn giữ là logout thì sẽ trùng tới tên hàm của mình => dẫn đến đệ quy 
    # # => đổi 1 trong 2, hoặc là tên hàm của mình hoặc là tên hàm của thư viện 
    # # request.session.flush() # xóa cả cookie lẫn session 
    # # Hoặc sử dụng request.session.flush() để xóa session và xóa cookie của session
    # # Chuyển hướng người dùng về trang đăng nhập

    user_logout(request)
    return redirect('login')