"""
AppConfig class providing central config

"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, SecretStr, SerializationInfo, field_serializer

from ..serializer import contextual_serializer_password


class GroupCommon(BaseModel):
    """Common config for photobooth."""

    model_config = ConfigDict(title="Cài đặt chung")

    admin_password: SecretStr = Field(
        default=SecretStr("0000"),
        description="Mật khẩu truy cập trang quản trị.",
    )

    @field_serializer("admin_password")
    def contextual_serializer(self, value, info: SerializationInfo):
        return contextual_serializer_password(value, info)

    logging_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="DEBUG",
        description="Mức độ log. File được ghi vào đĩa, và log mới nhất cũng được hiển thị trên UI.",
    )

    ui_language: Literal["vi", "en", "de", "fr", "es"] = Field(
        default="vi",
        description="Ngôn ngữ giao diện người dùng. Mặc định là Tiếng Việt (vi). Các tùy chọn khác: Tiếng Anh (en), Tiếng Đức (de), Tiếng Pháp (fr), Tiếng Tây Ban Nha (es).",
    )

    users_delete_to_recycle_dir: bool = Field(
        default=True,
        description="Nếu bật, file chụp sẽ được chuyển vào thư mục thùng rác thay vì xóa vĩnh viễn. Ảnh đã xóa có thể được admin khôi phục thủ công. Vui lòng thông báo cho người dùng rằng không có ảnh nào bị xóa thực sự nếu bạn bật chức năng này!",
    )
