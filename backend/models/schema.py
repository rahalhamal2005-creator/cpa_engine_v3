from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
import datetime
from core.database import Base

class Niche(Base):
    __tablename__ = "niches"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    audience = Column(String)
    pain_points = Column(Text)
    status = Column(String, default="testing") # testing, scaling, killed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    videos = relationship("Video", back_populates="niche")
    offers = relationship("Offer", back_populates="niche")

class Offer(Base):
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True, index=True)
    niche_id = Column(Integer, ForeignKey("niches.id"))
    name = Column(String)
    payout = Column(Float)
    epc = Column(Float, default=0.0)
    conversions = Column(Integer, default=0)
    geo = Column(String)
    status = Column(String, default="active")
    
    niche = relationship("Niche", back_populates="offers")
    funnels = relationship("Funnel", back_populates="offer")

class Funnel(Base):
    __tablename__ = "funnels"
    id = Column(Integer, primary_key=True, index=True)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    landing_url = Column(String)
    type = Column(String) # top_apps, unlock_guide
    ctr = Column(Float, default=0.0)
    conversions = Column(Integer, default=0)
    
    offer = relationship("Offer", back_populates="funnels")
    videos = relationship("Video", back_populates="funnel")

class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True, index=True)
    niche_id = Column(Integer, ForeignKey("niches.id"))
    funnel_id = Column(Integer, ForeignKey("funnels.id"))
    hook = Column(String)
    angle = Column(String)
    script = Column(Text)
    platform = Column(String) # TikTok, YouTube, Pinterest
    views = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    status = Column(String, default="published") # published, killed, scaling
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    niche = relationship("Niche", back_populates="videos")
    funnel = relationship("Funnel", back_populates="videos")
