# Hướng Dẫn Thay Đổi UI Sang Tiếng Việt

## ✅ Đã Hoàn Thành

### 1. Thêm Language Setting
**File**: `src/photobooth/services/config/groups/common.py`

Đã thêm field `ui_language` với default là `"vi"` (tiếng Việt):
```python
ui_language: Literal["vi", "en", "de", "fr", "es"] = Field(
    default="vi",
    description="User interface language. Default is Vietnamese (vi).",
)
```

### 2. Thay Đổi Text Mặc Định Sang Tiếng Việt
**File**: `src/photobooth/services/config/groups/uisettings.py`

Đã thay đổi các text sau:

#### Trang Chủ (Frontpage)
- **Trước**: `Hey!<br>Let's take some pictures! <br>📷`
- **Sau**: `Xin chào!<br>Hãy chụp vài bức ảnh nào! <br>📷`

#### Gallery Trống
- **Trước**: `Empty, Zero, Nada! 🤷‍♂️<br>Let's take some pictures! <br>📷💕`
- **Sau**: `Trống rỗng! 🤷‍♂️<br>Hãy chụp vài bức ảnh nào! <br>📷💕`

#### QR Code Text
- **Trước**: `👋 Download your photo!`
- **Sau**: `👋 Tải ảnh của bạn!`

- **Trước**: `Scan above code with your phone.`
- **Sau**: `Quét mã QR bằng điện thoại của bạn.`

### 3. Kết Quả
✅ **Đã thay đổi thành công** - Text chính trên trang chủ hiện là tiếng Việt!

![Screenshot](C:/Users/Admin/.gemini/antigravity/brain/0d149ebd-0940-4711-90c2-d9ecf0d98835/main_page_vietnamese_1767063605176.png)

---

## ⚠️ Còn Thiếu - Cần Thay Đổi Frontend

### Các Label Còn Tiếng Anh
Các nút bấm và label sau vẫn còn tiếng Anh:
- `Gallery` → Cần đổi thành "Bộ sưu tập"
- `Admin` → Cần đổi thành "Quản trị"
- `Image` → Cần đổi thành "Ảnh đơn"
- `Collage` → Cần đổi thành "Ảnh ghép"
- `Animation` → Cần đổi thành "Ảnh động"
- `Boomerang` → Giữ nguyên hoặc "Video lặp"
- `Wigglegram` → Giữ nguyên hoặc "Ảnh 3D"
- `Back` → Cần đổi thành "Quay lại"

### Nguyên Nhân
Frontend được build sẵn từ repository riêng: https://github.com/photobooth-app/photobooth-frontend

Frontend sử dụng **Vue 3 + Quasar Framework** và có hệ thống i18n (internationalization) riêng.

---

## 🔧 Cách Thay Đổi Frontend Labels

### Option 1: Sử dụng Crowdin (Khuyến Nghị)
Photobooth-app sử dụng Crowdin cho translation:
1. Truy cập: https://crowdin.com/project/photobooth-app
2. Chọn ngôn ngữ Vietnamese
3. Dịch các strings còn thiếu
4. Sau khi đạt 100%, sẽ được merge vào release tiếp theo

### Option 2: Clone Frontend Repository và Build
Nếu muốn custom ngay:

```bash
# Clone frontend repo
git clone https://github.com/photobooth-app/photobooth-frontend.git
cd photobooth-frontend

# Install dependencies
npm install

# Tìm translation files
# Thường ở: src/i18n/locales/vi.json hoặc tương tự

# Edit translation files
# Thêm/sửa các key-value pairs

# Build frontend
npm run build

# Copy build output vào photobooth-app
cp -r dist/* ../photobooth-app/src/web/frontend/
```

### Option 3: Hack Nhanh (Temporary)
Nếu chỉ muốn test nhanh, có thể edit trực tiếp file JS đã build:

⚠️ **Lưu ý**: Cách này không khuyến khích vì sẽ bị mất khi update app.

```bash
# Tìm file chứa text
grep -r "Gallery" src/web/frontend/assets/

# Edit file JS (rất khó đọc vì đã minified)
# Thay "Gallery" thành "Bộ sưu tập"
```

---

## 📝 Translation Mapping Đề Xuất

Đây là bản dịch đề xuất cho các UI elements:

### Main Actions
| English | Tiếng Việt |
|---------|------------|
| Gallery | Bộ sưu tập |
| Admin | Quản trị |
| Settings | Cài đặt |
| Back | Quay lại |
| Close | Đóng |
| Save | Lưu |
| Cancel | Hủy |
| Delete | Xóa |
| Download | Tải xuống |
| Share | Chia sẻ |
| Print | In ảnh |

### Capture Modes
| English | Tiếng Việt |
|---------|------------|
| Image | Ảnh đơn |
| Collage | Ảnh ghép |
| Animation | Ảnh động |
| Video | Video |
| Boomerang | Video lặp |
| Wigglegram | Ảnh 3D |

### Gallery
| English | Tiếng Việt |
|---------|------------|
| Filter | Bộ lọc |
| All | Tất cả |
| Images | Ảnh |
| Videos | Video |
| Animations | Ảnh động |
| Empty gallery | Bộ sưu tập trống |

### Messages
| English | Tiếng Việt |
|---------|------------|
| Smile! | Cười lên! |
| Get ready! | Chuẩn bị! |
| Processing... | Đang xử lý... |
| Saved! | Đã lưu! |
| Error | Lỗi |
| Success | Thành công |

---

## 🎯 Kế Hoạch Tiếp Theo

### Bước 1: Xác Định Phương Án
Chọn một trong các option trên:
- [ ] Option 1: Contribute vào Crowdin (lâu dài, chính thống)
- [ ] Option 2: Clone và build frontend (control hoàn toàn)
- [ ] Option 3: Hack nhanh (test only)

### Bước 2: Implement
Tùy theo option đã chọn, thực hiện các bước tương ứng.

### Bước 3: Test
- [ ] Kiểm tra tất cả các trang
- [ ] Kiểm tra tất cả các nút bấm
- [ ] Kiểm tra messages và notifications
- [ ] Kiểm tra admin panel

### Bước 4: Deploy
- [ ] Copy frontend đã build vào `src/web/frontend/`
- [ ] Restart server
- [ ] Verify trên browser

---

## 💡 Tips

### 1. Tìm Translation Keys
Để tìm key của một text cụ thể trong frontend:
```bash
# Search trong frontend source code
grep -r "Gallery" photobooth-frontend/src/
```

### 2. Test Nhanh
Sau khi thay đổi config (Python files), chỉ cần restart server:
```bash
# Stop server (Ctrl+C)
# Start lại
uv run photobooth --host 127.0.0.1 --port 8000
```

### 3. Clear Browser Cache
Nếu thay đổi frontend nhưng không thấy update:
- Hard refresh: `Ctrl + Shift + R`
- Hoặc clear cache trong DevTools

---

## 📚 Tài Liệu Tham Khảo

- **Frontend Repository**: https://github.com/photobooth-app/photobooth-frontend
- **Crowdin Project**: https://crowdin.com/project/photobooth-app
- **Quasar i18n**: https://quasar.dev/options/app-internationalization
- **Vue i18n**: https://vue-i18n.intlify.dev/

---

## ✅ Summary

**Đã làm được**:
- ✅ Thêm language setting vào config
- ✅ Thay đổi text mặc định sang tiếng Việt (frontpage, gallery, QR code)
- ✅ Text chính đã hiển thị tiếng Việt trên UI

**Cần làm tiếp**:
- ⏳ Dịch frontend labels (buttons, menus, messages)
- ⏳ Build và deploy frontend mới
- ⏳ Test toàn bộ UI

**Khuyến nghị**: 
Sử dụng Option 2 (Clone frontend repo) để có control hoàn toàn và có thể custom thêm nhiều thứ khác ngoài ngôn ngữ.

---

**Ngày cập nhật**: 2025-12-30  
**Status**: ✅ Backend text đã Việt hóa, Frontend cần tiếp tục
