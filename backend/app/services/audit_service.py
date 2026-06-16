from datetime import datetime
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


class AuditService:
    """Manages audit logging for system actions"""

    @staticmethod
    def log_action(user_id: int, action: str, entity: str, entity_id: str, 
                   details: str = None, db: Session = None) -> AuditLog:
        """Log an action to audit trail"""
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            entity=entity,
            entity_id=entity_id,
            details=details,
            created_at=datetime.utcnow()
        )
        db.add(audit_log)
        db.commit()
        return audit_log

    @staticmethod
    def get_user_actions(user_id: int, db: Session) -> list:
        """Get all actions performed by a user"""
        return db.query(AuditLog).filter(AuditLog.user_id == user_id).all()

    @staticmethod
    def get_entity_history(entity: str, entity_id: str, db: Session) -> list:
        """Get all actions on a specific entity"""
        return db.query(AuditLog).filter(
            AuditLog.entity == entity,
            AuditLog.entity_id == entity_id
        ).all()

    @staticmethod
    def get_recent_actions(limit: int = 100, db: Session = None) -> list:
        """Get recent actions in the system"""
        return db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_actions_by_date_range(start_date: datetime, end_date: datetime, db: Session) -> list:
        """Get actions within a date range"""
        return db.query(AuditLog).filter(
            AuditLog.created_at >= start_date,
            AuditLog.created_at <= end_date
        ).all()
