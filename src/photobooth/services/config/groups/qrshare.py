"""
AppConfig class providing central config

"""

from platform import node

from pydantic import BaseModel, ConfigDict, Field

hostname = node() if node() != "" else "localhost"


class GroupQrShare(BaseModel):
    """Settings about shareing media"""

    model_config = ConfigDict(title="Chia sẻ qua mã QR")

    enabled: bool = Field(
        default=False,
        description="(ĐÃ CŨ trong v8) Bật dịch vụ chia sẻ QR. Để bật, URL cần được cấu hình và script dl.php phải được thiết lập đúng.",
        # json_schema_extra={"deprecated": "v8"},
    )
    shareservice_url: str = Field(
        default="https://photobooth-app.org/extras/shareservice-landing/",
        description="(ĐÃ CŨ trong v8) URL của script php dùng để phục vụ file và chia sẻ qua mã QR. Mặc định là trang đích với hướng dẫn cài đặt.",
        # json_schema_extra={"deprecated": "v8"},
    )
    shareservice_apikey: str = Field(
        default="changedefault!",
        description="(ĐÃ CŨ trong v8) Key bảo mật script php download. Đặt key trong dl.php giống với giá trị này. Dịch vụ chỉ hoạt động nếu key đúng.",
        # json_schema_extra={"deprecated": "v8"},
    )

    enabled_custom: bool = Field(
        default=False,
        description="Bật dịch vụ chia sẻ QR. Để bật, URL cần được cấu hình và script dl.php phải được thiết lập đúng.",
    )
    share_custom_qr_url: str = Field(
        default=f"http://{hostname}:8000/download/#?url=http://{hostname}:8000/media/full/{{identifier}}",
        description="URL hiển thị dạng mã QR để tải ảnh. Bạn cần tự đồng bộ file hoặc cho phép người dùng truy cập qua hotspot. {identifier} được thay thế bằng ID mục, {filename} được thay thế bằng tên file thực tế.",
    )
