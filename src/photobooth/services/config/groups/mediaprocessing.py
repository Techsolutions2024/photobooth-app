"""
AppConfig class providing central config

"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

RembgModelType = Literal["modnet", "u2netp", "u2net"]


class GroupMediaprocessing(BaseModel):
    """Configure stages how to process images after capture."""

    model_config = ConfigDict(title="Xử lý hình ảnh (AI/Filter)")

    full_still_length: int = Field(
        default=1500,
        ge=800,
        le=5000,
        description="Kích thước tối thiểu cạnh dài dùng để scale ảnh chụp đầy đủ. Cạnh ngắn được tính toán theo tỷ lệ. Để hiệu năng tốt nhất hãy chọn thấp nhất có thể nhưng vẫn đảm bảo chất lượng in. Ví dụ: 1500/6inch=250dpi",
    )
    preview_still_length: int = Field(
        default=1200,
        ge=200,
        le=2500,
        description="Kích thước tối thiểu cạnh dài dùng để scale ảnh xem trước. Cạnh ngắn được tính toán theo tỷ lệ.",
    )
    thumbnail_still_length: int = Field(
        default=400,
        ge=100,
        le=1000,
        description="Kích thước tối thiểu cạnh dài dùng để scale ảnh thumbnail. Cạnh ngắn được tính toán theo tỷ lệ.",
    )

    video_bitrate: int = Field(
        default=3000,
        ge=1000,
        le=10000,
        description="Chất lượng bitrate video tính bằng k.",
    )

    video_compatibility_mode: bool = Field(
        default=True,
        description="Bật để cải thiện tương thích video trên thiết bị iOS và Firefox. Chất lượng có thể giảm nhẹ.",
    )

    remove_background_model: RembgModelType = Field(
        default="modnet",
        description="Chọn model có sẵn. Modnet và u2netp được tích hợp sẵn, các model khác sẽ tải về khi cần (cần internet). u2netp nhanh nhất, modnet chậm hơn chút nhưng kết quả tốt.",
    )

    fileformat_animations: Literal["webp", "avif", "gif"] = Field(
        default="webp",
        description="Định dạng lưu trữ ảnh động. WebP được khuyến nghị. GIF chất lượng thấp hơn nhưng tương thích tốt nhất (đã cũ).",
    )

    fileformat_multicamera: Literal["mp4", "webp", "avif", "gif"] = Field(
        default="mp4",
        description="Định dạng lưu trữ wigglegrams (đa góc). MP4 được khuyến nghị cho chất lượng và tương thích. GIF chất lượng thấp (đã cũ).",
    )
