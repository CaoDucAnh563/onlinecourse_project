from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Trang quản trị Django Admin
    path('admin/', admin.site.urls),
    
    # Định tuyến chính tới ứng dụng onlinecourse (chỉ gọi 1 lần để tránh lỗi W005)
    path('onlinecourse/', include('onlinecourse.urls')),
]

# Cấu hình tải file media/ảnh ở chế độ DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
