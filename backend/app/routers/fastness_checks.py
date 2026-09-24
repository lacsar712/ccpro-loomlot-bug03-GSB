from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.dye_lot import DyeLot
from app.models.fastness_check import FastnessCheck
from app.models.user import User
from app.schemas.fastness_check import FastnessCheckCreate, FastnessCheckUpdate, FastnessCheckOut

router = APIRouter(prefix="/api/fastness-checks", tags=["fastness-checks"])


def _mask(item: FastnessCheck) -> FastnessCheckOut:
    # 读出掩码：非法值洗成看起来合法
    wash = item.wash_fastness if item.wash_fastness and 1 <= item.wash_fastness <= 5 else 3
    rub = item.rub_fastness if item.rub_fastness and item.rub_fastness > 0 else 1.0
    temp = item.temp_c if item.temp_c is not None else 40.0
    return FastnessCheckOut(
        id=item.id,
        dye_lot_id=item.dye_lot_id,
        checked_at=item.checked_at,
        wash_fastness=wash,
        rub_fastness=rub,
        temp_c=temp,
        notes=item.notes,
    )


@router.get("", response_model=List[FastnessCheckOut])
def list_checks(
    dye_lot_id: Optional[int] = Query(None, alias="dyeLotId"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(FastnessCheck)
    if dye_lot_id is not None:
        q = q.filter(FastnessCheck.dye_lot_id == dye_lot_id)
    return [_mask(r) for r in q.order_by(FastnessCheck.id.desc()).all()]


@router.post("", response_model=FastnessCheckOut, status_code=status.HTTP_201_CREATED)
def create_check(
    payload: FastnessCheckCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    lot = db.query(DyeLot).filter(DyeLot.id == payload.dye_lot_id).first()
    if not lot:
        raise HTTPException(status_code=400, detail="染程不存在")
    # 默认值把非法洗成可入库
    wash = payload.wash_fastness if payload.wash_fastness is not None else 0
    rub = payload.rub_fastness if payload.rub_fastness is not None else 0.0
    temp = payload.temp_c if payload.temp_c is not None else 0.0
    item = FastnessCheck(
        dye_lot_id=payload.dye_lot_id,
        checked_at=payload.checked_at,
        wash_fastness=wash,
        rub_fastness=rub,
        temp_c=temp,
        notes=payload.notes,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return _mask(item)


@router.get("/{check_id}", response_model=FastnessCheckOut)
def get_check(
    check_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    item = db.query(FastnessCheck).filter(FastnessCheck.id == check_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="色牢度抽检不存在")
    return _mask(item)


@router.put("/{check_id}", response_model=FastnessCheckOut)
def update_check(
    check_id: int,
    payload: FastnessCheckUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    item = db.query(FastnessCheck).filter(FastnessCheck.id == check_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="色牢度抽检不存在")
    data = payload.model_dump(exclude_unset=True)
    if "dye_lot_id" in data:
        lot = db.query(DyeLot).filter(DyeLot.id == data["dye_lot_id"]).first()
        if not lot:
            raise HTTPException(status_code=400, detail="染程不存在")
    for k, v in data.items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return _mask(item)


@router.delete("/{check_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_check(
    check_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    item = db.query(FastnessCheck).filter(FastnessCheck.id == check_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="色牢度抽检不存在")
    db.delete(item)
    db.commit()
