"""
AppConfig class providing central config

"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ..models.trigger import GpioTrigger, KeyboardTrigger, Trigger, UiTrigger

ParameterUiType = Literal["input", "int"]


class ShareProcessingParameters(BaseModel):
    """Configure additional parameter for the share command to input by the user."""

    model_config = ConfigDict(title="Tham số bổ sung")

    key: str = Field(
        default="copies",
        min_length=4,
        pattern=r"^[a-zA-Z0-9]+$",
        description="Định nghĩa khóa tham số sẽ được thay thế trong lệnh. Ví dụ: Nếu đặt là 'copies', {copies} trong lệnh sẽ được thay thế bằng giá trị thực tế.",
    )
    label: str = Field(
        default="Copies",
        description="Nhãn hiển thị cho người dùng.",
    )
    ui_type: ParameterUiType = Field(
        default="int",
        description="Loại hiển thị của tham số trên giao diện. 'int' hiện nút tăng giảm ➕➖. 'input' hiện ô nhập liệu. Chỉ ảnh hưởng hiển thị, mọi tham số đều là chuỗi.",
    )
    default: str = Field(
        default="1",
        description="Giá trị mặc định nếu người dùng không thay đổi.",
    )
    valid_min: str = Field(default="1")
    valid_max: str = Field(default="3")


class ShareProcessing(BaseModel):
    """Configure options to share or print images."""

    model_config = ConfigDict(title="Hành động Chia sẻ/In")

    share_command: str = Field(
        default="echo {filename}",
        description="Lệnh thực thi để chia sẻ/in. Dùng {filename} thay cho file cần xử lý. Cũng hỗ trợ: {media_type}=[image,collage,video,animation] và {action_config_name} là tên hành động định nghĩa trong config.",
    )
    ask_user_for_parameter_input: bool = Field(
        default=False,
        description="Nếu bật, khi nút chia sẻ được kích hoạt, một hộp thoại sẽ hiện ra để nhập các tham số cấu hình bên dưới.",
    )
    parameters_dialog_caption: str = Field(
        default="Make your choice!",
        description="Tiêu đề hộp thoại hiển thị các tham số.",
    )
    parameters_dialog_action_icon: str = Field(
        default="print",
        description="Icon cho nút hành động (bất kỳ icon nào từ material icons, xem tài liệu).",
    )
    parameters_dialog_action_label: str = Field(
        default="GO",
        description="Văn bản làm nhãn cho nút hành động.",
    )

    parameters: list[ShareProcessingParameters] = Field(
        default=[],
        description="Định nghĩa các trường nhập liệu người dùng cần điền khi chia sẻ.",
    )

    share_blocked_time: int = Field(
        # default=10,
        description="Chặn hàng đợi in cho đến khi hết thời gian (giây).",
    )

    max_shares: int = Field(
        default=0,
        ge=0,
        description="Giới hạn số lần chia sẻ tối đa (0 = không giới hạn).",
    )


class ShareConfigurationSet(BaseModel):
    """Configure stages how to process mediaitem before printing on paper."""

    model_config = ConfigDict(title="Cấu hình xử lý trước khi in")

    name: str = Field(
        default="default print settings",
        description="Tên định danh, chỉ dùng hiển thị trong trang quản trị.",
    )

    handles_images_only: bool = Field(
        default=True,
        description="Bật nếu kiểu chia sẻ này chỉ xử lý ảnh tĩnh.",
    )

    processing: ShareProcessing
    trigger: Trigger


class GroupShare(BaseModel):
    """Configure share or print actions."""

    model_config = ConfigDict(title="Chia sẻ / In ấn")

    sharing_enabled: bool = Field(
        default=True,
        description="Bật dịch vụ chia sẻ nói chung.",
    )

    actions: list[ShareConfigurationSet] = Field(
        default=[
            ShareConfigurationSet(
                name="Printing",
                handles_images_only=True,
                processing=ShareProcessing(
                    share_command="echo {filename} media_type={media_type} action_config_name={action_config_name} copies={copies}",
                    ask_user_for_parameter_input=False,
                    share_blocked_time=3,
                    parameters=[ShareProcessingParameters()],
                ),
                trigger=Trigger(
                    ui_trigger=UiTrigger(show_button=True, title="In ngay", icon="print"),
                    gpio_trigger=GpioTrigger(pin="23", trigger_on="pressed"),
                    keyboard_trigger=KeyboardTrigger(keycode="p"),
                ),
            ),
            ShareConfigurationSet(
                name="Printing copies",
                handles_images_only=True,
                processing=ShareProcessing(
                    share_command="echo {filename} media_type={media_type} action_config_name={action_config_name} copies={copies}",
                    ask_user_for_parameter_input=True,
                    parameters_dialog_caption="How many copies?",
                    share_blocked_time=3,
                    parameters=[ShareProcessingParameters()],
                ),
                trigger=Trigger(
                    ui_trigger=UiTrigger(show_button=True, title="In nhiều bản", icon="print"),
                    gpio_trigger=GpioTrigger(pin="", trigger_on="pressed"),
                    keyboard_trigger=KeyboardTrigger(keycode=""),
                ),
            ),
            ShareConfigurationSet(
                name="Mailing action",
                handles_images_only=False,
                processing=ShareProcessing(
                    share_command="echo {filename} media_type={media_type} action_config_name={action_config_name} to mail {mail}",
                    ask_user_for_parameter_input=True,
                    parameters_dialog_caption="E-Mail your image...",
                    parameters_dialog_action_icon="mail",
                    parameters_dialog_action_label="Send",
                    share_blocked_time=3,
                    parameters=[
                        ShareProcessingParameters(
                            key="mail",
                            label="E-Mail address",
                            ui_type="input",
                            default="me@mgineer85.de",
                            valid_min="5",
                            valid_max="128",
                        ),
                    ],
                ),
                trigger=Trigger(
                    ui_trigger=UiTrigger(show_button=True, title="Gửi Mail", icon="mail"),
                    gpio_trigger=GpioTrigger(pin="", trigger_on="pressed"),
                    keyboard_trigger=KeyboardTrigger(keycode=""),
                ),
            ),
        ],
        description="Chia sẻ hoặc in các mục media.",
    )
