from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, FilePath
from pydantic_extra_types.color import Color

from ..validators import ensure_demoassets


class GroupUiSettings(BaseModel):
    """Personalize the booth's UI."""

    model_config = ConfigDict(title="Giao diện người dùng")

    PRIMARY_COLOR: Color = Field(
        default=Color("#196cb0"),
        description="Màu chủ đạo (ví dụ: nút bấm, thanh tiêu đề).",
    )

    SECONDARY_COLOR: Color = Field(
        default=Color("#4283b8"),
        description="Màu phụ (đếm ngược, điểm nhấn).",
    )

    theme: Literal["system", "light", "dark"] = Field(
        default="system",
        description="Chủ đề ứng dụng. Chọn system để tự động chuyển đổi theo cài đặt hệ thống/trình duyệt hoặc chọn cố định sáng/tối.",
    )

    show_gallery_on_frontpage: bool = Field(
        default=True,
        description="Hiển thị nút thư viện trên trang chủ.",
    )
    show_admin_on_frontpage: bool = Field(
        default=True,
        description="Hiển thị nút trung tâm quản trị, thường chỉ dùng trong quá trình cài đặt.",
    )
    admin_button_invisible: bool = Field(
        default=False,
        description="Nếu nút được hiển thị, nó vẫn có thể được làm ẩn đi. Nếu bật, nút sẽ trong suốt 100% và cần 5 lần click trong vòng 500ms để truy cập đăng nhập admin.",
    )

    show_frontpage_timeout: int = Field(
        default=5,
        ge=1,
        description="Thời gian chờ tính bằng phút sau đó ứng dụng sẽ quay lại trang chủ.",
    )
    enable_automatic_slideshow: bool = Field(
        default=True,
        description="Bật slideshow ngẫu nhiên sau một khoảng thời gian không có tương tác người dùng.",
    )
    show_automatic_slideshow_timeout: int = Field(
        default=300,
        ge=30,
        description="Thời gian chờ tính bằng giây sau đó slideshow sẽ bắt đầu.",
    )

    enable_livestream_when_idle: bool = Field(
        default=True,
        description="Khi nhàn rỗi, livestream từ camera sẽ hiển thị liên tục.",
    )
    enable_livestream_when_active: bool = Field(
        default=True,
        description="Khi đếm ngược hoặc chụp đang hoạt động, livestream từ camera sẽ hiển thị.",
    )
    livestream_mirror_effect: bool = Field(
        default=True,
        description="Lật livestream theo chiều ngang để tạo hiệu ứng gương, mang lại cảm giác tự nhiên hơn cho người dùng.",
    )
    livestream_blurredbackground: bool = Field(
        default=True,
        description="Hiển thị livestream mờ làm nền cho livestream chính phủ kín màn hình. Trông sẽ đẹp nếu độ phân giải livestream không khớp với tỷ lệ màn hình. Kiểm tra tải CPU trên thiết bị cấu hình thấp.",
    )
    livestream_blurredbackground_high_framerate: bool = Field(
        default=False,
        description="Để tiết kiệm CPU, nền mờ chỉ làm mới mỗi 300ms/3.3fps. Nếu ứng dụng chạy trên máy tính mạnh, bạn có thể bật tốc độ khung hình cao hơn, làm mới mỗi 50ms/20fps.",
    )
    enable_livestream_frameoverlay: bool = Field(
        default=True,
        description="Bật lớp phủ khung hình lên livestream.",
    )
    livestream_frameoverlay_image: Annotated[FilePath | None, BeforeValidator(ensure_demoassets)] = Field(
        default=Path("userdata/demoassets/frames/frame_image_photobooth-app.png"),
        description="Khi được bật, khung hình sẽ phủ lên livestream. Ảnh này không được sử dụng trong hậu kỳ. Nếu hiệu ứng gương bật, nó cũng sẽ bị lật. Chữ trong khung hình sẽ bị ngược nhưng ảnh cuối cùng sẽ đúng.",
        json_schema_extra={"list_api": "/api/admin/enumerate/userfiles"},
    )
    livestream_frameoverlay_mirror_effect: bool = Field(
        default=False,
        description="Lật khung hình phủ theo chiều ngang để tạo hiệu ứng gương. Hữu ích để lật video khi mọi người căn chỉnh theo khung hình. Nếu có chữ trong khung hình, nó cũng sẽ bị lật.",
    )

    FRONTPAGE_TEXT: str = Field(
        default='<div class="fixed-center text-h2 text-weight-bold text-center text-white" style="text-shadow: 4px 4px 4px #666;">Xin chào!<br>Hãy chụp vài bức ảnh nào! <br>📷</div>',
        description="Văn bản/HTML hiển thị trên trang chủ.",
    )

    TAKEPIC_MSG_TIME: float = Field(
        default=0.5,
        description="Thời gian hiển thị icon mặt cười tính bằng giây.",
    )
    TAKEPIC_MSG_TEXT: str = Field(
        default="😃",
        description="Thông điệp hiển thị ở cuối quá trình đếm ngược chụp ảnh.",
    )

    AUTOCLOSE_NEW_ITEM_ARRIVED: int = Field(
        default=30,
        description="Thời gian chờ tính bằng giây để popup ảnh mới tự động đóng.",
    )

    GALLERY_EMPTY_MSG: str = Field(
        default='<div class="fixed-center text-h2 text-weight-bold text-center text-white" style="text-shadow: 4px 4px 4px #666;">Trống rỗng! 🤷‍♂️<br>Hãy chụp vài bức ảnh nào! <br>📷💕</div>',
        description="Thông báo hiển thị nếu thư viện trống.",
    )
    gallery_show_qrcode: bool = Field(
        default=True,
        description="Hiển thị mã QR trong thư viện. Nếu dịch vụ chia sẻ được bật, URL sẽ được tạo tự động, nếu không hãy vào cấu hình chia sẻ và cung cấp URL.",
    )
    qrcode_text_above: str = Field(
        default="👋 Tải ảnh của bạn!",
        description="Hiển thị văn bản phía trên mã QR.",
    )
    qrcode_text_below: str = Field(
        default="Quét mã QR bằng điện thoại của bạn.",
        description="Hiển thị văn bản phía dưới mã QR.",
    )
    qrcode_link_codes: bool = Field(
        default=False,
        description="Link có thể click được thêm vào chính mã QR. Hữu ích để test nhưng nên tắt trên hệ thống production để tránh người dùng thoát khỏi ứng dụng.",
    )

    gallery_show_filter: bool = Field(
        default=True,
        description="Hiển thị bộ lọc được cung cấp bởi plugin. Bộ lọc Pilgram2 đã được bao gồm trong ứng dụng. Xem tài liệu để mở rộng và xây dựng plugin riêng của bạn.",
    )
    gallery_show_download: bool = Field(
        default=True,
        description="Hiển thị nút tải xuống trong thư viện.",
    )
    gallery_show_delete: bool = Field(
        default=True,
        description="Hiển thị nút xóa trong thư viện.",
    )
    gallery_show_shareprint: bool = Field(
        default=True,
        description="Hiển thị các nút chia sẻ/in trong thư viện.",
    )
