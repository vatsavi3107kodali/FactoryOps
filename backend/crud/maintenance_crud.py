"""
maintenance_crud.py

Database operations for maintenance records.
"""

from sqlalchemy.orm import Session

from backend.models.maintenance import Maintenance
from backend.schemas.maintenance_schema import MaintenanceCreate


# ============================================================
# GET ALL MAINTENANCE RECORDS
# ============================================================

def get_all_maintenance(db: Session):

    return (
        db.query(Maintenance)
        .order_by(Maintenance.created_at.desc())
        .all()
    )


# ============================================================
# GET MAINTENANCE BY ID
# ============================================================

def get_maintenance_by_id(
    db: Session,
    maintenance_id: int
):

    return (
        db.query(Maintenance)
        .filter(
            Maintenance.id == maintenance_id
        )
        .first()
    )


# ============================================================
# GET MAINTENANCE FOR A MACHINE
# ============================================================

def get_maintenance_by_machine(
    db: Session,
    machine_id: int
):

    return (
        db.query(Maintenance)
        .filter(
            Maintenance.machine_id == machine_id
        )
        .order_by(
            Maintenance.created_at.desc()
        )
        .all()
    )


def create_maintenance(
    db: Session,
    maintenance_data: MaintenanceCreate
):

    maintenance = Maintenance(
        machine_id=maintenance_data.machine_id,
        maintenance_type=maintenance_data.maintenance_type,
        priority=maintenance_data.priority,
        engineer=maintenance_data.engineer,
        scheduled_date=maintenance_data.scheduled_date,
        completion_status=maintenance_data.completion_status,
        remarks=maintenance_data.remarks
    )

    db.add(maintenance)
    db.commit()
    db.refresh(maintenance)

    return maintenance