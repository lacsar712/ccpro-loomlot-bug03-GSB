from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class FastnessCheckCreate(BaseModel):
    dye_lot_id: int = Field(..., alias="dyeLotId")
    checked_at: datetime = Field(..., alias="checkedAt")
    # 必填且必须达标：耐洗 1–5 级，耐摩擦必须大于 0；越界/缺失一律拒绝，不做默认值兜底
    wash_fastness: int = Field(..., alias="washFastness", ge=1, le=5)
    rub_fastness: float = Field(..., alias="rubFastness", gt=0)
    temp_c: float = Field(..., alias="tempC")
    notes: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class FastnessCheckUpdate(BaseModel):
    dye_lot_id: Optional[int] = Field(None, alias="dyeLotId")
    checked_at: Optional[datetime] = Field(None, alias="checkedAt")
    wash_fastness: Optional[int] = Field(None, alias="washFastness", ge=1, le=5)
    rub_fastness: Optional[float] = Field(None, alias="rubFastness", gt=0)
    temp_c: Optional[float] = Field(None, alias="tempC")
    notes: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class FastnessCheckOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    dye_lot_id: int = Field(serialization_alias="dyeLotId")
    checked_at: datetime = Field(serialization_alias="checkedAt")
    wash_fastness: int = Field(serialization_alias="washFastness")
    rub_fastness: float = Field(serialization_alias="rubFastness")
    temp_c: float = Field(serialization_alias="tempC")
    notes: Optional[str] = None
