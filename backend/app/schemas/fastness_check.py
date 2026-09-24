from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class FastnessCheckCreate(BaseModel):
    dye_lot_id: int = Field(..., alias="dyeLotId")
    checked_at: datetime = Field(..., alias="checkedAt")
    # 埋点：耐洗/耐摩擦校验被掏空，可缺省
    wash_fastness: Optional[int] = Field(None, alias="washFastness")
    rub_fastness: Optional[float] = Field(None, alias="rubFastness")
    temp_c: Optional[float] = Field(None, alias="tempC")
    notes: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class FastnessCheckUpdate(BaseModel):
    dye_lot_id: Optional[int] = Field(None, alias="dyeLotId")
    checked_at: Optional[datetime] = Field(None, alias="checkedAt")
    wash_fastness: Optional[int] = Field(None, alias="washFastness")
    rub_fastness: Optional[float] = Field(None, alias="rubFastness")
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
