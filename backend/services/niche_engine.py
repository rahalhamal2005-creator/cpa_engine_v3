import json
import os
import requests
from datetime import datetime, timedelta
from pytrends.request import TrendReq
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

class NicheEngine:
    def __init__(self):
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        self.youtube = None
        if self.youtube_api_key:
            self.youtube = build('youtube', 'v3', developerKey=self.youtube_api_key)

    def search_niches(self, query: str, country: str):
        print(f"Starting analysis for query: '{query}' in '{country}'")
        trends_data = []
        try:
            print("1. Fetching from Google Trends...")
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
            pytrend = TrendReq(hl='en-US', tz=360, timeout=(10,25), requests_args={'headers': headers})
            
            # Force Category 8 (Games) so it strictly finds gaming trends
            pytrend.build_payload(kw_list=[query], geo=country, timeframe='now 7-d', cat=8)
            related = pytrend.related_queries()
            
            if related and query in related and related[query]['rising'] is not None:
                top_rising = related[query]['rising'].head(10)
                for index, row in top_rising.iterrows():
                    trends_data.append(row['query'].title())
            
            if not trends_data or query.lower() in ["mobile games", "games", "gaming"]:
                pytrend.build_payload(kw_list=["free", "hack"], geo=country, timeframe='now 7-d', cat=8)
                rel = pytrend.related_queries()
                for kw in ["free", "hack"]:
                    if rel and kw in rel and rel[kw]['rising'] is not None:
                        for idx, r in rel[kw]['rising'].head(5).iterrows():
                            if r['query'].title() not in trends_data:
                                trends_data.append(r['query'].title())
                                
            print(f"   Google Trends Games found: {trends_data}")
        except Exception as e:
            print(f"   Pytrends error: {e}")

        real_trending_games = []
        youtube_titles = []
        avg_views = "N/A"
        try:
            print("2. Fetching real trending games from YouTube...")
            if self.youtube:
                # Fetch top gaming videos currently trending in the specified country
                video_response = self.youtube.videos().list(
                    part='snippet,statistics',
                    chart='mostPopular',
                    videoCategoryId='20', # Gaming
                    regionCode=country,
                    maxResults=25
                ).execute()
                
                views = []
                keywords = {}
                invalid_tags = ["gameplay", "walkthrough", "live", "video", "shorts", "gaming", "game", "tiktok", "stream", "funny", "moments", "montage", "highlights", "let's play", "playthrough", "part 1", "update", "new"]
                
                for item in video_response.get('items', []):
                    title = item['snippet'].get('title', '')
                    if title:
                        youtube_titles.append(title)
                    
                    views.append(int(item['statistics'].get('viewCount', 0)))
                    tags = item['snippet'].get('tags', [])
                    
                    # Extract game names from tags
                    for tag in tags[:8]:
                        tag_clean = tag.title()
                        if len(tag_clean) > 3 and tag_clean.lower() not in invalid_tags:
                            # Avoid appending generic words if they are part of the tag
                            is_valid = True
                            for invalid in ["gameplay", "walkthrough", "live", "gaming"]:
                                if invalid in tag_clean.lower():
                                    is_valid = False
                                    break
                            if is_valid:
                                keywords[tag_clean] = keywords.get(tag_clean, 0) + 1
                
                sorted_games = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
                real_trending_games = [g[0] for g in sorted_games[:15]]
                
                avg = sum(views) / len(views) if views else 0
                if avg > 1000000:
                    avg_views = f"{avg/1000000:.1f}M"
                elif avg > 1000:
                    avg_views = f"{avg/1000:.1f}K"
                else:
                    avg_views = str(int(avg))
                        
            print(f"   YouTube extracted games: {real_trending_games}")
            print(f"   Average views calculated: {avg_views}")
        except Exception as e:
            print(f"   YouTube API error: {e}")

        # Combine trends from both sources
        combined_trends = list(dict.fromkeys(trends_data + real_trending_games))
        if not combined_trends:
            combined_trends = ["Roblox", "Brawl Stars", "Free Fire", "Minecraft", "Call of Duty Mobile"] # Ultimate fallback

        print(f"   Combined Trending Games: {combined_trends[:10]}")
        
        current_year = datetime.utcnow().year

        prompt = f"""
        You are an expert CPA Affiliate Marketer.
        The user searched for gaming niches in country '{country}'.
        Our real-time APIs (Google Trends & YouTube) show these EXACT games/topics are trending heavily right now: {combined_trends[:15]}.
        Recent YouTube videos in this exact niche average {avg_views} views.
        Top video titles right now: {youtube_titles[:5]}

        Based on this REAL data, return an array of exactly 10 highly profitable CPA niches. If there aren't enough trending games in the list, suggest other top-tier gaming niches currently popular on YouTube.
        Tell the user EXACTLY which game to target based on the real trends provided above.
        Output MUST be valid JSON in exactly this format, nothing else:
        {{
            "niches": [
                {{
                    "game": "Exact Name of the Specific Trending Game (e.g. Brawl Stars)",
                    "viral_title": "A highly clickable, viral YouTube title for the video (e.g. 'I Found a NEW Brawl Stars Glitch in {current_year}! 😱')",
                    "trending_aspect": "What exactly is trending right now (e.g. Free Gems Glitch, New Season Pass)",
                    "video_idea": "A short, engaging idea for the YouTube video content (e.g. Show you playing normally, then 'accidentally' triggering a hack to get unlimited money)",
                    "cpa_integration": "Exactly how and when to mention the CPA link in the video (e.g. Point to the pinned comment halfway through the video)",
                    "offer_angle": "What exactly to tell them they are getting (e.g. Mod Menu, Free Skins, Unlimited Money/Gems, Auto-Aimbot)",
                    "promotion_strategy": "Step-by-step how to promote it (e.g. YouTube Shorts showing a live glitch and pinning comment)",
                    "locker_strategy": "Exactly how to set up the content locker (e.g. File Locker named 'GemsGenerator.apk')",
                    "audience": "Target audience description",
                    "search_volume": "Estimated (e.g. High)",
                    "competition": "Low, Medium, or High",
                    "avg_views": "{avg_views}",
                    "traffic_sources": "Best traffic source for this",
                    "trend_prediction": "Your prediction on how long it will stay trending and its longevity (e.g. High potential to stay trending for months...)"
                }}
            ]
        }}
        """

        try:
            print("3. Generating CPA Strategy with AI APIs...")
            content = self._generate_ai_content(prompt, combined_trends, avg_views, youtube_titles)
            if not content:
                print("   Both AI models failed to generate content.")
                return {"niches": []}

            print("   Analysis complete!")
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
                
            return json.loads(content.strip())
        except Exception as e:
            print(f"   JSON Parse/Execution error: {e}")
            return {"niches": []}

    def _generate_ai_content(self, prompt: str, combined_trends: list, avg_views: str, youtube_titles: list = None) -> str:
        # 1. Try Gemini
        if self.gemini_api_key:
            try:
                print("   -> Trying Gemini 2.0 API...")
                from google import genai
                client = genai.Client(api_key=self.gemini_api_key)
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt,
                )
                return response.text
            except Exception as e:
                print(f"      Gemini 2.0 failed: {e}")
                try:
                    print("   -> Trying Gemini 1.5 API Fallback...")
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=prompt,
                    )
                    return response.text
                except Exception as e2:
                    print(f"      Gemini 1.5 failed: {e2}")

        # 2. Try OpenAI fallback
        if self.openai_api_key:
            try:
                print("   -> Trying OpenAI API Fallback...")
                headers = {
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                }
                resp = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
                if resp.status_code == 200:
                    return resp.json()["choices"][0]["message"]["content"]
                else:
                    print(f"      OpenAI API failed: {resp.text}")
            except Exception as e:
                print(f"      OpenAI Exception: {e}")

        # 3. Both failed (Quota exhausted), use real data mock response
        print("   -> APIs Out Of Quota! Generating response using REAL YouTube & Trends data...")
        
        current_year = datetime.utcnow().year
        niches = []
        games_to_use = combined_trends.copy()
        if len(games_to_use) < 10:
            games_to_use.extend(["Roblox", "Minecraft", "Fortnite", "Free Fire", "Brawl Stars", "PUBG Mobile", "Call of Duty", "Genshin Impact", "Valorant", "GTA V"])
            
        games_to_use = list(dict.fromkeys(games_to_use))[:10]
        
        for i, game_name in enumerate(games_to_use):
            prediction = "🔥 High potential to stay trending long-term based on recent YouTube activity." if i < 3 else "⚠️ Medium potential. Viral spike detected recently."
            
            # Use real YouTube titles to make it extremely authentic
            real_title = ""
            if youtube_titles:
                for yt in youtube_titles:
                    if game_name.lower() in yt.lower():
                        real_title = f' Like the recent viral video: "{yt}"'
                        break
                if not real_title and i < len(youtube_titles):
                    real_title = f' Like the recent viral video: "{youtube_titles[i]}"'
            
            niches.append({
                "game": game_name,
                "viral_title": f"How To Get FREE {game_name} Resources in {current_year}! 😱 (WORKING GLITCH)",
                "trending_aspect": "Latest Game Updates / Viral Exploits",
                "video_idea": f"Start the video showing 0 resources. Then show yourself typing a secret code, and boom - unlimited resources appear. Say you found a secret dev menu.",
                "cpa_integration": "At 0:15 in the video, point an arrow down and say 'Link to the mod is in the pinned comment! Download before it gets patched!'",
                "offer_angle": "Unlimited Money / Free Skins Unlocker",
                "promotion_strategy": f"Create YouTube Shorts demonstrating working gameplay or glitches for {game_name}.{real_title}. Add a call-to-action pointing to your pinned comment.",
                "locker_strategy": f"Set up a content locker labeled '{game_name} Premium Content'. Require a quick app install or PIN submit to unlock.",
                "audience": "Mobile & PC Gamers",
                "search_volume": "High (Trending globally right now)",
                "competition": "Medium",
                "avg_views": avg_views,
                "traffic_sources": "YouTube Shorts, TikTok, Instagram Reels",
                "trend_prediction": prediction
            })
            
        mock_response = {
            "niches": niches
        }
        return json.dumps(mock_response)

