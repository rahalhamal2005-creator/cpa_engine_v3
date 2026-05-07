from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
import os

from core.database import engine, Base, get_db
from models import schema
from services.niche_engine import NicheEngine
from services.offer_engine import OfferEngine
from services.content_engine import ContentEngine
from services.analytics_engine import AnalyticsEngine
from services.scaling_engine import ScalingEngine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CPA Gaming Profit Engine v3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MODULE 32: DECISION ENGINE (Scheduler)
scheduler = BackgroundScheduler()

def autonomous_execution_loop():
    """
    Main loop that runs daily to execute the 32 modules.
    """
    print("Executing Autonomous Cycle...")
    # Initialize engines with mock clients for now
    niche_engine = NicheEngine(youtube_client=None, openai_client=None)
    offer_engine = OfferEngine()
    content_engine = ContentEngine(openai_client=None, gemini_client=None)
    scaling_engine = ScalingEngine()
    
    # 1. Finds Micro Niches
    niches = niche_engine.detect_micro_niches(["mobile games", "desktop games"])
    
    for niche_data in niches:
        niche = niche_data['niche']
        
        # 6. Offer Intelligence
        offer_info = offer_engine.match_niche(niche)
        
        # 7. Traffic Match
        traffic_source = offer_engine.choose_traffic_source(offer_info['offer'])
        
        # 8, 9, 10. Generate Content
        hooks = content_engine.generate_hooks(niche, count=3)
        for hook in hooks:
            script = content_engine.generate_script(hook, "curiosity")
            # 12. Distribution - would go here
            # print(f"Published: {script}")

        # 29. Time-to-decision & 25. Scaling
        # Checked async per video

scheduler.add_job(autonomous_execution_loop, "interval", hours=24)
scheduler.start()

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Engine is running successfully"}

@app.get("/api/dashboard")
def get_dashboard_metrics(db: Session = Depends(get_db)):
    analytics = AnalyticsEngine(db)
    return analytics.aggregate_dashboard_metrics()

@app.post("/api/force_run")
def force_run_cycle(background_tasks: BackgroundTasks):
    background_tasks.add_task(autonomous_execution_loop)
    return {"message": "Execution loop started in background"}

@app.get("/api/niche/search")
def search_niches_manual(query: str, country: str = "US"):
    niche_engine = NicheEngine()
    result = niche_engine.search_niches(query, country)
    return result
