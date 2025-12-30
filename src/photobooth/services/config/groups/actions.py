from pathlib import Path
from typing import Annotated, Generic, TypeVar

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, FilePath, NonNegativeInt
from pydantic_extra_types.color import Color

from ..models.models import AnimationMergeDefinition, CollageMergeDefinition, PluginFilters, TextsConfig
from ..models.trigger import GpioTrigger, KeyboardTrigger, Trigger, UiTrigger
from ..validators import ensure_demoassets


class SingleImageJobControl(BaseModel):
    """Configure job control affecting the procedure."""

    model_config = ConfigDict(title="Điều khiển chụp ảnh đơn")

    countdown_capture: float = Field(
        default=2.0,
        multiple_of=0.1,
        ge=0,
        le=20,
        description="Thời gian đếm ngược (giây) khi người dùng bắt đầu chụp.",
    )


class MultiImageJobControl(BaseModel):
    """Configure job control affecting the procedure."""

    model_config = ConfigDict(title="Điều khiển chụp nhiều ảnh")

    countdown_capture: float = Field(
        default=2.0,
        multiple_of=0.1,
        ge=0,
        le=20,
        description="Thời gian đếm ngược (giây) khi người dùng bắt đầu chụp",
    )
    countdown_capture_second_following: float = Field(
        default=1.0,
        multiple_of=0.1,
        ge=0,
        le=20,
        description="Thời gian đếm ngược (giây) cho các lần chụp tiếp theo trong ảnh ghép",
    )

    ask_approval_each_capture: bool = Field(
        default=False,
        description="Dừng lại sau mỗi lần chụp để hỏi người dùng có muốn tiếp tục hay chụp lại không. Nếu tắt, ảnh luôn được coi là chấp nhận.",
    )
    approve_autoconfirm_timeout: float = Field(
        default=15.0,
        description="Nếu yêu cầu người dùng duyệt ảnh ghép, sau thời gian này (giây), quy trình sẽ tiếp tục và coi như người dùng đã xác nhận.",
    )

    show_individual_captures_in_gallery: bool = Field(
        default=False,
        description="Hiển thị từng ảnh chụp lẻ trong thư viện. Ảnh bị ẩn vẫn được lưu trong thư mục dữ liệu. (Lưu ý: thay đổi cài đặt này không ảnh hưởng đến khả năng hiển thị của ảnh đã chụp).",
    )


class VideoJobControl(BaseModel):
    """Configure job control affecting the procedure."""

    model_config = ConfigDict(title="Điều khiển quay video")

    countdown_capture: float = Field(
        default=2.0,
        multiple_of=0.1,
        ge=0,
        le=20,
        description="Thời gian đếm ngược (giây) khi người dùng bắt đầu chụp.",
    )


class MulticameraJobControl(BaseModel):
    """Configure job control affecting the procedure."""

    model_config = ConfigDict(title="Điều khiển chụp đa góc (3D)")

    countdown_capture: float = Field(
        default=2.0,
        multiple_of=0.1,
        ge=0,
        le=20,
        description="Thời gian đếm ngược (giây) khi người dùng bắt đầu chụp.",
    )

    show_individual_captures_in_gallery: bool = Field(
        default=False,
        description="Hiển thị từng ảnh chụp lẻ trong thư viện. Ảnh bị ẩn vẫn được lưu trong thư mục dữ liệu. (Lưu ý: thay đổi cài đặt này không ảnh hưởng đến khả năng hiển thị của ảnh đã chụp).",
    )


class SingleImageProcessing(BaseModel):
    """Configure stages how to process images after capture."""

    model_config = ConfigDict(title="Xử lý ảnh đơn sau khi chụp")

    remove_background: bool = Field(
        default=False,
        description="Sử dụng AI để xóa phông nền khỏi ảnh đã chụp. Kết quả có thể khác nhau. Có nhiều model khác nhau trong phần xử lý media.",
    )

    fill_background_enable: bool = Field(
        default=False,
        description="Áp dụng màu nền đồng nhất cho ảnh đã chụp (chỉ hữu ích nếu ảnh được mở rộng hoặc xóa phông nền)",
    )
    fill_background_color: Color = Field(
        default=Color("blue"),
        description="Màu đồng nhất dùng để tô nền.",
    )
    img_background_enable: bool = Field(
        default=False,
        description="Thêm ảnh từ file vào nền (chỉ hữu ích nếu ảnh được mở rộng hoặc xóa phông nền)",
    )
    img_background_file: Annotated[FilePath | None, BeforeValidator(ensure_demoassets)] = Field(
        default=None,
        description="File ảnh dùng làm nền lấp đầy vùng trong suốt. File cần nằm trong thư mục làm việc/userdata/*",
        json_schema_extra={"list_api": "/api/admin/enumerate/userfiles"},
    )

    image_filter: PluginFilters = Field(default=PluginFilters("original"))

    img_frame_enable: bool = Field(
        default=False,
        description="Gắn ảnh đã chụp vào khung.",
    )
    img_frame_file: Annotated[FilePath | None, BeforeValidator(ensure_demoassets)] = Field(
        default=None,
        description="File ảnh khung để gắn ảnh chụp vào. Khung quyết định kích thước ảnh đầu ra! Ảnh chụp hiển thị qua các phần trong suốt. Ảnh khung cần phải trong suốt (PNG). File cần nằm trong userdata/*",
        json_schema_extra={"list_api": "/api/admin/enumerate/userfiles"},
    )
    texts_enable: bool = Field(
        default=False,
        description="Bật chung tính năng chèn văn bản bên dưới.",
    )
    texts: list[TextsConfig] = Field(
        default=[],
        description="Văn bản phủ lên ảnh sau khi chụp. Pos_x/Pos_y tính bằng pixel bắt đầu từ 0/0 ở góc trên bên trái ảnh. Font chữ được sử dụng trong các bước văn bản. File cần nằm trong thư mục làm việc/userdata/*",
    )


class CollageProcessing(BaseModel):
    """Configure stages how to process collage after capture."""

    model_config = ConfigDict(title="Xử lý ảnh ghép")

    ## phase 1 per capture application on collage also. settings taken from PipelineImage if needed

    capture_remove_background: bool = Field(
        default=False,
        description="Sử dụng AI để xóa phông nền khỏi ảnh đã chụp. Kết quả có thể khác nhau. Có nhiều model khác nhau trong phần xử lý media.",
    )

    capture_fill_background_enable: bool = Field(
        default=False,
        description="Áp dụng màu nền đồng nhất cho ảnh đã chụp (chỉ hữu ích nếu ảnh được mở rộng hoặc xóa phông nền)",
    )
    capture_fill_background_color: Color = Field(
        default=Color("blue"),
        description="Màu đồng nhất dùng để tô nền.",
    )
    capture_img_background_enable: bool = Field(
        default=False,
        description="Thêm ảnh từ file vào nền (chỉ hữu ích nếu ảnh được mở rộng hoặc xóa phông nền)",
    )
    capture_img_background_file: Annotated[FilePath | None, BeforeValidator(ensure_demoassets)] = Field(
        default=None,
        description="File ảnh dùng làm nền lấp đầy vùng trong suốt. File cần nằm trong thư mục làm việc/userdata/*",
        json_schema_extra={"list_api": "/api/admin/enumerate/userfiles"},
    )

    ## phase 2 per collage settings.

    canvas_width: int = Field(
        default=1920,
        description="Chiều rộng (X) tính bằng pixel của ảnh ghép. Càng cao thì chất lượng càng tốt nhưng thời gian xử lý càng lâu. Mọi quy trình đều giữ nguyên tỷ lệ khung hình.",
    )
    canvas_height: int = Field(
        default=1280,
        description="Chiều cao (Y) tính bằng pixel của ảnh ghép. Càng cao thì chất lượng càng tốt nhưng thời gian xử lý càng lâu. Mọi quy trình đều giữ nguyên tỷ lệ khung hình.",
    )
    merge_definition: list[CollageMergeDefinition] = Field(
        description="Cách sắp xếp các ảnh đơn trong ảnh ghép. Pos_x/Pos_y tính bằng pixel bắt đầu từ 0/0 ở góc trên bên trái ảnh. Chiều rộng/Chiều cao tính bằng pixel. Luôn giữ nguyên tỷ lệ khung hình. Ảnh định sẵn được dùng thay vì ảnh chụp từ camera. File cần nằm trong thư mục làm việc/userdata/*",
    )
    canvas_fill_background_enable: bool = Field(
        default=False,
        description="Áp dụng màu nền đồng nhất cho ảnh ghép",
    )
    canvas_fill_background_color: Color = Field(
        default=Color("green"),
        description="Màu đồng nhất dùng để tô nền.",
    )
    canvas_img_background_enable: bool = Field(
        default=False,
        description="Thêm ảnh từ file vào nền.",
    )
    canvas_img_background_file: Annotated[FilePath | None, BeforeValidator(ensure_demoassets)] = Field(
        default=None,
        description="File ảnh dùng làm nền lấp đầy vùng trong suốt. File cần nằm trong userdata/*",
        json_schema_extra={"list_api": "/api/admin/enumerate/userfiles"},
    )
    canvas_img_front_enable: bool = Field(
        default=False,
        description="Phủ ảnh lên trên ảnh ghép.",
    )
    canvas_img_front_file: Annotated[FilePath | None, BeforeValidator(ensure_demoassets)] = Field(
        default=None,
        description="File ảnh để dán chồng lên trên ảnh chụp và hình nền. Ảnh chụp chỉ hiển thị quá các phần trong suốt. Ảnh cần phải trong suốt (PNG). File cần nằm trong thư mục làm việc/userdata/*",
        json_schema_extra={"list_api": "/api/admin/enumerate/userfiles"},
    )
    canvas_texts_enable: bool = Field(
        default=False,
        description="Bật chung tính năng chèn văn bản bên dưới.",
    )
    canvas_texts: list[TextsConfig] = Field(
        default=[],
        description="Văn bản phủ lên ảnh ghép cuối cùng. Pos_x/Pos_y tính bằng pixel bắt đầu từ 0/0 ở góc trên bên trái ảnh. Font chữ đợc sử dụng trong các bước văn bản. File cần nằm trong thư mục làm việc/userdata/*",
    )


class AnimationProcessing(BaseModel):
    """Configure stages how to process collage after capture."""

    model_config = ConfigDict(title="Xử lý ảnh động sau khi chụp")

    ## phase 2 per collage settings.

    canvas_width: int = Field(
        default=1500,
        description="Chiều rộng (X) tính bằng pixel cho ảnh động kết quả. Càng cao chất lượng càng tốt nhưng thời gian xử lý càng lâu. Mọi quy trình đều giữ nguyên tỷ lệ khung hình.",
    )
    canvas_height: int = Field(
        default=900,
        description="Chiều cao (Y) tính bằng pixel cho ảnh động kết quả. Càng cao chất lượng càng tốt nhưng thời gian xử lý càng lâu. Mọi quy trình đều giữ nguyên tỷ lệ khung hình.",
    )
    merge_definition: list[AnimationMergeDefinition] = Field(
        default=[],
        description="Chuỗi ảnh chụp và ảnh định sẵn để xếp hàng trong ảnh động kết quả. Ảnh định sẵn được dùng thay vì ảnh chụp từ camera. File cần nằm trong thư mục làm việc/userdata/*",
    )


class VideoProcessing(BaseModel):
    """Configure stages how to process collage after capture."""

    model_config = ConfigDict(title="Xử lý video")

    video_duration: int = Field(
        default=5,
        description="Thời lượng tối đa của video. Người dùng có thể dừng sớm hơn hoặc việc quay sẽ tự động dừng sau thời gian đã thiết lập.",
    )
    boomerang: bool = Field(
        default=False,
        description="Tạo video boomerang, video sẽ được phát ngược lại sau khi phát xuôi.",
    )
    boomerang_speed: float = Field(
        default=1,
        ge=0.5,
        le=2,
        description="Tăng tốc video boomerang kết quả. 1 là tốc độ bình thường, 2 là gấp đôi.",
    )
    video_framerate: int = Field(
        default=25,
        ge=1,
        le=30,
        description="Tốc độ khung hình video (khung hình trên giây).",
    )


class MulticameraProcessing(BaseModel):
    """Configure stages how to process collage after capture."""

    model_config = ConfigDict(title="Xử lý ảnh đa góc (3D)")

    duration: NonNegativeInt = Field(
        default=125,
        ge=100,
        le=500,
        description="Thời lượng của mỗi khung hình tính bằng mili giây. Wigglegrams thường trông đẹp nhất với thời lượng từ 100-200ms.",
    )
    image_filter: PluginFilters = Field(
        default=PluginFilters("original"),
    )


t_JOBCONTROL = TypeVar("t_JOBCONTROL")
t_PROCESSING = TypeVar("t_PROCESSING")


class BaseConfigurationSet(BaseModel, Generic[t_JOBCONTROL, t_PROCESSING]):
    name: str = Field(
        default="default action",
        description="Tên định danh, chỉ dùng để hiển thị trong trung tâm quản trị.",
    )

    jobcontrol: t_JOBCONTROL
    processing: t_PROCESSING
    trigger: Trigger


class SingleImageConfigurationSet(BaseConfigurationSet[SingleImageJobControl, SingleImageProcessing]):
    """Configure stages how to process images after capture."""

    model_config = ConfigDict(title="Hậu kỳ ảnh đơn")


class CollageConfigurationSet(BaseConfigurationSet[MultiImageJobControl, CollageProcessing]):
    """Configure stages how to process images after capture."""

    model_config = ConfigDict(title="Hậu kỳ ảnh ghép")


class AnimationConfigurationSet(BaseConfigurationSet[MultiImageJobControl, AnimationProcessing]):
    """Configure stages how to process images after capture."""

    model_config = ConfigDict(title="Hậu kỳ ảnh động")


class VideoConfigurationSet(BaseConfigurationSet[VideoJobControl, VideoProcessing]):
    """Configure stages how to process images after capture."""

    model_config = ConfigDict(title="Hậu kỳ video")


class MulticameraConfigurationSet(BaseConfigurationSet[MulticameraJobControl, MulticameraProcessing]):
    """Configure stages how to process images after capture."""

    model_config = ConfigDict(title="Hậu kỳ ảnh đa góc")


class GroupActions(BaseModel):
    """
    Configure actions like capture photo, video, collage and animations.
    """

    model_config = ConfigDict(title="Cấu hình hành động")

    image: list[SingleImageConfigurationSet] = Field(
        default=[
            SingleImageConfigurationSet(
                jobcontrol=SingleImageJobControl(),
                processing=SingleImageProcessing(
                    remove_background=True,
                    img_background_enable=True,
                    img_background_file=Path("userdata/demoassets/backgrounds/background.jpg"),
                    img_frame_enable=True,
                    img_frame_file=Path("userdata/demoassets/frames/frame_image_photobooth-app.png"),
                    texts_enable=True,
                    texts=[
                        TextsConfig(
                            text="Visit photobooth-app.org and build yours!",  # use {date} and {time} to add dynamic texts; cannot use in default because tests will fail that compare images
                            pos_x=1300,
                            pos_y=1250,
                            rotate=0,
                            font_size=30,
                            color=Color("#333"),
                        )
                    ],
                ),
                trigger=Trigger(
                    ui_trigger=UiTrigger(title="Ảnh đơn", icon="photo_camera"),
                    gpio_trigger=GpioTrigger(pin="27"),
                    keyboard_trigger=KeyboardTrigger(keycode="i"),
                ),
            ),
        ],
        description="Chụp ảnh đơn.",
    )

    collage: list[CollageConfigurationSet] = Field(
        default=[
            CollageConfigurationSet(
                jobcontrol=MultiImageJobControl(
                    ask_approval_each_capture=True,
                    show_individual_captures_in_gallery=True,
                ),
                processing=CollageProcessing(
                    capture_remove_background=True,
                    capture_fill_background_enable=True,
                    capture_fill_background_color=Color("white"),
                    canvas_width=1920,
                    canvas_height=1280,
                    merge_definition=[
                        CollageMergeDefinition(
                            description="left",
                            pos_x=160,
                            pos_y=220,
                            width=510,
                            height=725,
                            rotate=0,
                            image_filter=PluginFilters("FilterPilgram2.earlybird"),
                        ),
                        CollageMergeDefinition(
                            description="middle predefined",
                            pos_x=705,
                            pos_y=66,
                            width=510,
                            height=725,
                            rotate=0,
                            predefined_image=Path("userdata/demoassets/predefined_images/photobooth-collage-predefined-image.png"),
                            image_filter=PluginFilters("original"),
                        ),
                        CollageMergeDefinition(
                            description="right",
                            pos_x=1245,
                            pos_y=220,
                            width=510,
                            height=725,
                            rotate=0,
                            image_filter=PluginFilters("FilterPilgram2.reyes"),
                        ),
                    ],
                    canvas_img_front_enable=True,
                    canvas_img_front_file=Path("userdata/demoassets/frames/pixabay-poster-2871536_1920.png"),
                    canvas_texts_enable=True,
                    canvas_texts=[
                        TextsConfig(
                            text="Have a nice day :)",
                            pos_x=200,
                            pos_y=1100,
                            rotate=1,
                            color=Color("#333"),
                        )
                    ],
                ),
                trigger=Trigger(
                    ui_trigger=UiTrigger(title="Ảnh ghép", icon="auto_awesome_mosaic"),
                    gpio_trigger=GpioTrigger(pin="22"),
                    keyboard_trigger=KeyboardTrigger(keycode="c"),
                ),
            )
        ],
        description="Chụp ảnh ghép bao gồm một hoặc nhiều ảnh tĩnh.",
    )

    animation: list[AnimationConfigurationSet] = Field(
        default=[
            AnimationConfigurationSet(
                jobcontrol=MultiImageJobControl(
                    ask_approval_each_capture=False,
                    show_individual_captures_in_gallery=False,
                    countdown_capture_second_following=0.5,
                ),
                processing=AnimationProcessing(
                    canvas_width=1500,
                    canvas_height=900,
                    merge_definition=[
                        AnimationMergeDefinition(image_filter=PluginFilters("FilterPilgram2.crema")),
                        AnimationMergeDefinition(image_filter=PluginFilters("FilterPilgram2.inkwell")),
                        AnimationMergeDefinition(),
                        AnimationMergeDefinition(),
                        AnimationMergeDefinition(
                            duration=4000,
                            image_filter=PluginFilters("original"),
                            predefined_image=Path("userdata/demoassets/predefined_images/photobooth-gif-animation-predefined-image.png"),
                        ),
                    ],
                ),
                trigger=Trigger(
                    ui_trigger=UiTrigger(title="Ảnh động", icon="animated_images"),
                    gpio_trigger=GpioTrigger(pin="24"),
                    keyboard_trigger=KeyboardTrigger(keycode="g"),
                ),
            ),
        ],
        description="Chụp ảnh động bao gồm một hoặc nhiều ảnh tĩnh. Không phải video mà là chuỗi ảnh tĩnh (GIF).",
    )

    video: list[VideoConfigurationSet] = Field(
        default=[
            VideoConfigurationSet(
                jobcontrol=VideoJobControl(),
                processing=VideoProcessing(
                    video_duration=5,
                    boomerang=True,
                    boomerang_speed=2,
                    video_framerate=15,
                ),
                trigger=Trigger(
                    ui_trigger=UiTrigger(title="Video lặp", icon="movie"),
                    gpio_trigger=GpioTrigger(pin="25"),
                    keyboard_trigger=KeyboardTrigger(keycode="v"),
                ),
            ),
        ],
        description="Quay video từ backend livestream.",
    )

    multicamera: list[MulticameraConfigurationSet] = Field(
        default=[
            MulticameraConfigurationSet(
                jobcontrol=MulticameraJobControl(),
                processing=MulticameraProcessing(),
                trigger=Trigger(
                    ui_trigger=UiTrigger(title="Ảnh 3D", icon="3d"),
                    gpio_trigger=GpioTrigger(pin="12"),
                    keyboard_trigger=KeyboardTrigger(keycode="w"),
                ),
            ),
        ],
        description="Chụp ảnh đa góc (wigglegrams) từ hệ thống nhiều camera.",
    )
