# Hệ Thống Photobooth Thương Mại (Phiên Bản Việt Hóa)

Chào mừng bạn đến với hệ thống Photobooth chuyên nghiệp, được xây dựng trên nền tảng Python và Vue.js, đã được Việt hóa toàn diện để phục vụ thị trường Việt Nam.

![Photobooth Banner](https://raw.githubusercontent.com/photobooth-app/photobooth-app/main/assets/logo/logo-text-blue-transparent.png)

## 🚀 Tính Năng Nổi Bật

*   **Chụp ảnh đa dạng**: Hỗ trợ chụp ảnh đơn (Single), ảnh ghép (Collage), ảnh động (Animation/GIF), Video lặp (Boomerang) và ảnh 3D (Wigglegrams).
*   **Hỗ trợ nhiều loại Camera**: Tương thích với Webcam (USB), DSLR (Canon/Nikon qua Gphoto2), và Raspberry Pi Camera.
*   **Giao diện tiếng Việt**: Toàn bộ giao diện người dùng và trang cấu hình quản trị đã được dịch sang tiếng Việt, thân thiện và dễ sử dụng.
*   **Hiệu ứng & Bộ lọc**: Tích hợp sẵn các bộ lọc màu (Instagram-like) và khả năng xóa phông nền bằng AI.
*   **In ấn & Chia sẻ**: Hỗ trợ in ảnh trực tiếp và chia sẻ qua mã QR.
*   **Điều khiển đèn LED**: Tích hợp điều khiển đèn WLED hoặc GPIO để tạo hiệu ứng ánh sáng.

## 🛠️ Yêu Cầu Hệ Thống

*   **Hệ điều hành**: Windows 10/11, Linux (Debian/Ubuntu), hoặc Raspberry Pi OS.
*   **Python**: Phiên bản 3.11 trở lên.
*   **Node.js**: (Chỉ cần nếu bạn muốn build lại frontend) v16+.

## ⚙️ Cài Đặt & Khởi Chạy

### 1. Chuẩn bị môi trường
```bash
# Di chuyển vào thư mục dự án
cd d:\photobooth-app

# Tạo môi trường ảo (nếu chưa có)
python -m venv .venv

# Kích hoạt môi trường ảo (Windows)
.\.venv\Scripts\activate
```

### 2. Cài đặt thư viện
```bash
pip install -e .
```

### 3. Khởi chạy hệ thống (Backend)
```bash
python -m photobooth
```
Server sẽ khởi động tại địa chỉ: `http://127.0.0.1:8000`

### 4. Khởi chạy Frontend (Tùy chọn cho Dev)
Nếu bạn đang phát triển giao diện:
```bash
cd photobooth-frontend
npm install
npm run dev
```

## 📖 Hướng Dẫn Sử Dụng

### 1. Giao Diện Khách Hàng (Frontpage)
Truy cập: `http://127.0.0.1:8000/`
Đây là giao diện chính dành cho khách hàng sử dụng để chụp ảnh.
*   **Màn hình chờ**: Hiển thị slideshow ảnh hoặc nút bắt đầu.
*   **Chụp ảnh**: Khách hàng chọn chế độ chụp (Ảnh đơn, Ghép, Động...) và hệ thống sẽ đếm ngược.
*   **Thư viện**: Xem lại ảnh vừa chụp, in hoặc quét mã QR để tải về.

### 2. Giao Diện Quản Trị (Admin Dashboard)
Truy cập: `http://127.0.0.1:8000/#/admin`
*   **Đăng nhập**:
    *   Mật khẩu mặc định: `0000`
*   **Chức năng chính**:
    *   **Cấu hình**: Điều chỉnh mọi thông số của hệ thống.
    *   **Thư viện**: Quản lý tất cả ảnh/video đã chụp (xóa, in lại).
    *   **Trạng thái**: Xem log hệ thống và trạng thái các dịch vụ.

## 🔧 Hướng Dẫn Cấu Hình (Đã Việt Hóa)

Trong trang quản trị (`/admin/config`), các tab cấu hình đã được dịch sang tiếng Việt:

*   **Chung (Common)**:
    *   Đổi mật khẩu admin.
    *   Cài đặt ngôn ngữ giao diện (Chọn **Tiếng Việt**).
    *   Quản lý thùng rác (ảnh xóa).
*   **Camera**:
    *   Chọn loại camera (Webcam, DSLR, Camera ảo).
    *   Cấu hình độ phân giải, hướng xoay (ngang/dọc), ISO, tốc độ màn trập.
*   **Hành động (Actions)**:
    *   Cấu hình các quy trình chụp: Ảnh đơn, Ảnh ghép, Video.
    *   Chỉnh thời gian đếm ngược.
    *   Cài đặt bộ lọc màu và khung ảnh (Frame) mặc định.
*   **Giao diện người dùng (UI Settings)**:
    *   Chỉnh màu sắc chủ đạo, hình nền.
    *   Thay đổi văn bản hiển thị trên màn hình chào ("Xin chào! Hãy chụp vài bức ảnh nào!").
*   **Phần cứng (Hardware)**:
    *   Cấu hình in ấn (chọn máy in, số lượng bản in).
    *   Cấu hình đèn LED và các nút bấm vật lý (GPIO).

## 🆘 Khắc Phục Sự Cố

*   **Không vào được trang quản trị**: Kiểm tra xem server backend có đang chạy không (cửa sổ terminal/cmd). Đảm bảo port 8000 không bị chặn.
*   **Camera không hiển thị**: Đảm bảo camera đã kết nối USB. Vào tab **Camera** trong admin để kiểm tra xem thiết bị có được nhận diện không.
*   **Lỗi in ấn**: Kiểm tra kết nối máy in và driver. Đảm bảo máy in được chọn đúng trong tab **Phần cứng**.

---
*Hệ thống được phát triển và tùy biến lại cho thị trường Việt Nam. © 2025*
