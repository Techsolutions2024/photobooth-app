"""
AppConfig class providing central config

"""

from pydantic import BaseModel, ConfigDict, Field


class GroupHardwareInputOutput(BaseModel):
    """
    Configure hardware GPIO, keyboard and more. Find integration information in the documentation.
    """

    model_config = ConfigDict(title="Phần cứng (GPIO/Printer)")

    # keyboard config
    keyboard_input_enabled: bool = Field(
        default=False,
        description="Bật nhập liệu bàn phím toàn cục. Phím bấm được bắt trên trình duyệt kết nối tới ứng dụng.",
    )

    # GpioService Config
    gpio_enabled: bool = Field(
        default=False,
        description="Bật tích hợp Raspberry Pi GPIOzero.",
    )
    gpio_pin_shutdown: int = Field(
        default=17,
        description="Chân GPIO để tắt máy sau khi giữ 2 giây.",
    )
    gpio_pin_reboot: int = Field(
        default=18,
        description="Chân GPIO để khởi động lại sau khi giữ 2 giây.",
    )

    gpio_pin_job_next: int = Field(
        default=27,
        description="Nếu job đang chạy, chân này dùng để xác nhận/tiếp tục quy trình nếu cần nhập thủ công (vd để duyệt ảnh).",
    )
    gpio_pin_job_reject: int = Field(
        default=22,
        description="Nếu job đang chạy, chân này dùng để từ chối ảnh khi duyệt.",
    )
    gpio_pin_job_abort: int = Field(
        default=20,
        description="Nếu job đang chạy, chân này dùng để hủy job.",
    )
