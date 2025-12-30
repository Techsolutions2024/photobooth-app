"""
AppConfig class providing central config

"""

from pydantic import BaseModel, ConfigDict, Field


class GroupMisc(BaseModel):
    """
    Quite advanced or experimental, usually not necessary to touch. Can change any time.
    """

    model_config = ConfigDict(title="Cài đặt khác")

    secret_key: str = Field(
        default="ThisIsTheDefaultSecret",
        min_length=8,
        max_length=64,
        description="Mã bí mật để mã hóa dữ liệu xác thực. Nếu thay đổi, phiên đăng nhập sẽ bị vô hiệu hóa.",
    )

    cmd_shutdown: str = Field(
        default="shutdown now",
        description="Lệnh tắt máy khi được yêu cầu bởi ứng dụng. Thay đổi nếu bạn có giải pháp UPS tùy chỉnh.",
    )

    cmd_reboot: str = Field(
        default="reboot",
        description="Lệnh khởi động lại khi được yêu cầu bởi ứng dụng. Thay đổi nếu bạn có giải pháp UPS tùy chỉnh.",
    )
