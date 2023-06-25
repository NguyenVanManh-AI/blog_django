from django.contrib import admin
from django.urls import path
from myapp import views  
 
urlpatterns = [
    # quản lý nhân viên 
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  
    path('addnew',views.addnew, name='addnew'),  
    path('edit/<int:id>', views.edit, name='edit'),  
    path('update/<int:id>', views.update, name='update'),  
    path('delete/<int:id>', views.destroy, name='destroy'),  
    path('test-ajax2/<int:id>', views.test_ajax2, name='test_ajax2'),  
    path('test-ajax', views.test_ajax, name='test_ajax'),  
    # chú ý : phải là path('test-ajax', chứ không được : path('test-ajax/', . Thêm dấu / ở cuối là mấy cái dùng thư viện 

    # user 
    path('register', views.register, name='register'),  
    path('login', views.login, name='login'),  
    path('logout', views.logout, name='logout'),
]