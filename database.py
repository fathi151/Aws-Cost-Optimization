"""
Database Module
Handles persistent storage of chatbot data and history
"""

import logging
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()


class CostRecord(Base):
    """Cost record model"""
    __tablename__ = "cost_records"

    id = Column(String, primary_key=True)
    service = Column(String, index=True)
    region = Column(String, index=True)
    cost = Column(Float)
    usage = Column(Float)
    date = Column(DateTime, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "service": self.service,
            "region": self.region,
            "cost": self.cost,
            "usage": self.usage,
            "date": self.date.isoformat() if self.date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class ResourceRecord(Base):
    """Resource record model"""
    __tablename__ = "resource_records"

    id = Column(String, primary_key=True)
    instance_id = Column(String, index=True)
    instance_type = Column(String)
    state = Column(String)
    region = Column(String, index=True)
    launch_time = Column(DateTime)
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "instance_id": self.instance_id,
            "instance_type": self.instance_type,
            "state": self.state,
            "region": self.region,
            "launch_time": self.launch_time.isoformat() if self.launch_time else None,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class OptimizationInsight(Base):
    """Optimization insight model"""
    __tablename__ = "optimization_insights"

    id = Column(String, primary_key=True)
    title = Column(String, index=True)
    description = Column(Text)
    category = Column(String, index=True)
    priority = Column(String)
    potential_savings = Column(Float)
    recommendation = Column(Text)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "potential_savings": self.potential_savings,
            "recommendation": self.recommendation,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ChatHistory(Base):
    """Chat history model"""
    __tablename__ = "chat_history"

    id = Column(String, primary_key=True)
    conversation_id = Column(String, index=True)
    user_message = Column(Text)
    bot_response = Column(Text)
    context = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "user_message": self.user_message,
            "bot_response": self.bot_response,
            "context": self.context,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class SyncHistory(Base):
    """Sync history model"""
    __tablename__ = "sync_history"

    id = Column(String, primary_key=True)
    status = Column(String)
    data_points = Column(Integer)
    insights_generated = Column(Integer)
    error_message = Column(Text)
    duration_seconds = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "status": self.status,
            "data_points": self.data_points,
            "insights_generated": self.insights_generated,
            "error_message": self.error_message,
            "duration_seconds": self.duration_seconds,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class DatabaseManager:
    """Manage database operations"""

    def __init__(self, database_url: str = None):
        """
        Initialize database manager
        
        Args:
            database_url: Database connection URL
        """
        self.database_url = database_url or config.DATABASE_URL
        self.engine = create_engine(
            self.database_url,
            echo=config.DATABASE_ECHO
        )
        self.SessionLocal = sessionmaker(bind=self.engine)
        self._init_db()
        logger.info(f"Database initialized: {self.database_url}")

    def _init_db(self) -> None:
        """Initialize database tables"""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Database tables created")
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")

    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()

    def add_cost_record(self, record: Dict[str, Any]) -> bool:
        """Add cost record"""
        try:
            session = self.get_session()
            cost_record = CostRecord(
                id=record.get("id"),
                service=record.get("service"),
                region=record.get("region"),
                cost=record.get("cost"),
                usage=record.get("usage"),
                date=datetime.fromisoformat(record.get("date")) if record.get("date") else None,
            )
            session.add(cost_record)
            session.commit()
            session.close()
            return True
        except Exception as e:
            logger.error(f"Error adding cost record: {str(e)}")
            return False

    def add_resource_record(self, record: Dict[str, Any]) -> bool:
        """Add resource record"""
        try:
            session = self.get_session()
            resource_record = ResourceRecord(
                id=record.get("id"),
                instance_id=record.get("instance_id"),
                instance_type=record.get("instance_type"),
                state=record.get("state"),
                region=record.get("region"),
                launch_time=datetime.fromisoformat(record.get("launch_time")) if record.get("launch_time") else None,
                tags=record.get("tags"),
            )
            session.add(resource_record)
            session.commit()
            session.close()
            return True
        except Exception as e:
            logger.error(f"Error adding resource record: {str(e)}")
            return False

    def add_optimization_insight(self, insight: Dict[str, Any]) -> bool:
        """Add optimization insight"""
        try:
            session = self.get_session()
            opt_insight = OptimizationInsight(
                id=insight.get("id"),
                title=insight.get("title"),
                description=insight.get("description"),
                category=insight.get("category"),
                priority=insight.get("priority"),
                potential_savings=insight.get("potential_savings"),
                recommendation=insight.get("recommendation"),
            )
            session.add(opt_insight)
            session.commit()
            session.close()
            return True
        except Exception as e:
            logger.error(f"Error adding optimization insight: {str(e)}")
            return False

    def add_chat_history(self, chat: Dict[str, Any]) -> bool:
        """Add chat history"""
        try:
            session = self.get_session()
            chat_record = ChatHistory(
                id=chat.get("id"),
                conversation_id=chat.get("conversation_id"),
                user_message=chat.get("user_message"),
                bot_response=chat.get("bot_response"),
                context=chat.get("context"),
            )
            session.add(chat_record)
            session.commit()
            session.close()
            return True
        except Exception as e:
            logger.error(f"Error adding chat history: {str(e)}")
            return False

    def add_sync_history(self, sync: Dict[str, Any]) -> bool:
        """Add sync history"""
        try:
            session = self.get_session()
            sync_record = SyncHistory(
                id=sync.get("id"),
                status=sync.get("status"),
                data_points=sync.get("data_points"),
                insights_generated=sync.get("insights_generated"),
                error_message=sync.get("error_message"),
                duration_seconds=sync.get("duration_seconds"),
            )
            session.add(sync_record)
            session.commit()
            session.close()
            return True
        except Exception as e:
            logger.error(f"Error adding sync history: {str(e)}")
            return False

    def get_cost_records(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get cost records"""
        try:
            session = self.get_session()
            records = session.query(CostRecord).limit(limit).offset(offset).all()
            result = [r.to_dict() for r in records]
            session.close()
            return result
        except Exception as e:
            logger.error(f"Error getting cost records: {str(e)}")
            return []

    def get_optimization_insights(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get optimization insights"""
        try:
            session = self.get_session()
            records = session.query(OptimizationInsight).filter_by(status="active").limit(limit).all()
            result = [r.to_dict() for r in records]
            session.close()
            return result
        except Exception as e:
            logger.error(f"Error getting optimization insights: {str(e)}")
            return []

    def get_chat_history(self, conversation_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get chat history for conversation"""
        try:
            session = self.get_session()
            records = session.query(ChatHistory).filter_by(
                conversation_id=conversation_id
            ).order_by(ChatHistory.created_at.desc()).limit(limit).all()
            result = [r.to_dict() for r in records]
            session.close()
            return result
        except Exception as e:
            logger.error(f"Error getting chat history: {str(e)}")
            return []

    def get_sync_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get sync history"""
        try:
            session = self.get_session()
            records = session.query(SyncHistory).order_by(
                SyncHistory.created_at.desc()
            ).limit(limit).all()
            result = [r.to_dict() for r in records]
            session.close()
            return result
        except Exception as e:
            logger.error(f"Error getting sync history: {str(e)}")
            return []

    def clear_old_records(self, days: int = 90) -> bool:
        """Clear records older than specified days"""
        try:
            session = self.get_session()
            cutoff_date = datetime.utcnow() - timedelta(days=days)

            session.query(CostRecord).filter(CostRecord.created_at < cutoff_date).delete()
            session.query(ChatHistory).filter(ChatHistory.created_at < cutoff_date).delete()
            session.query(SyncHistory).filter(SyncHistory.created_at < cutoff_date).delete()

            session.commit()
            session.close()
            logger.info(f"Cleared records older than {days} days")
            return True
        except Exception as e:
            logger.error(f"Error clearing old records: {str(e)}")
            return False
