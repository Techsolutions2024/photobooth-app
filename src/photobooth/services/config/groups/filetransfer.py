"""
AppConfig class providing central config

"""

from pydantic import BaseModel, ConfigDict, Field


class GroupFileTransfer(BaseModel):
    """Configuration for USB File Transfer Service."""

    model_config = ConfigDict(title="Cấu hình chuyển file USB (đã cũ)")

    enabled: bool = Field(
        default=False,
        description="(ĐÃ CŨ trong v8) Bật dịch vụ tự động chuyển file sang USB. File sẽ được copy khi cắm USB.",
        # json_schema_extra={"deprecated": "v8"},
    )
    target_folder_name: str = Field(
        default="photobooth",
        description="(ĐÃ CŨ trong v8) Tên thư mục gốc trên USB nơi file sẽ được copy vào.",
        # json_schema_extra={"deprecated": "v8"},
    )
