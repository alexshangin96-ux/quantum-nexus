from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String(255))
    
    # Currencies
    coins = Column(Float, default=0.0)
    quanhash = Column(Float, default=0.0)
    
    # Energy
    energy = Column(Integer, default=1000)
    max_energy = Column(Integer, default=1000)
    # Regen
    energy_regen_rate = Column(Float, default=1.0)
    
    # Statistics
    total_taps = Column(Integer, default=0)
    total_earned = Column(Float, default=0.0)
    total_mined = Column(Float, default=0.0)
    
    # Referral
    referral_code = Column(String(50), unique=True)
    referred_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    referral_income = Column(Float, default=0.0)
    referrals_count = Column(Integer, default=0)
    
    # Active boosts
    active_multiplier = Column(Float, default=1.0)
    multiplier_expires_at = Column(DateTime, nullable=True)
    
    # Offline income
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # Settings
    sound_enabled = Column(Boolean, default=True)  # Sound effects enabled/disabled
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    machines = relationship("MiningMachine", back_populates="user")
    cards = relationship("UserCard", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")


class MiningMachine(Base):
    __tablename__ = 'mining_machines'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Machine details
    level = Column(Integer, default=1)
    name = Column(String(255))
    hash_rate = Column(Float, default=0.01)
    power_consumption = Column(Float, default=0.0)
    efficiency = Column(Float, default=1.0)
    
    # Mining status
    is_active = Column(Boolean, default=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    last_mined_at = Column(DateTime, default=datetime.utcnow)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="machines")


class UserCard(Base):
    __tablename__ = 'user_cards'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Card details
    card_type = Column(String(50))  # common, rare, epic, legendary
    income_per_minute = Column(Float)
    card_level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    experience_to_next_level = Column(Integer, default=100)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="cards")


class UserAchievement(Base):
    __tablename__ = 'user_achievements'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    achievement_type = Column(String(100))
    unlocked_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="achievements")


class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    transaction_type = Column(String(50))  # tap, mining, purchase, referral, etc.
    amount = Column(Float)
    currency = Column(String(20))  # coins or quanhash
    
    created_at = Column(DateTime, default=datetime.utcnow)






