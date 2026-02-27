import requests
from bs4 import BeautifulSoup
from app import app, db, Scholarship
from datetime import datetime, timedelta
import urllib.parse

def clean_url(raw_href):
    """DuckDuckGo  redirect link clear"""
    try:
        if "uddg=" in raw_href:
         
            actual_url = raw_href.split("uddg=")[1].split("&rut=")[0]
            return urllib.parse.unquote(actual_url)
        return raw_href
    except Exception:
        return raw_href

def scrape_scholarships():
    
    with app.app_context():
        fifteen_days_ago = datetime.utcnow() - timedelta(days=15)
        old_schemes = Scholarship.query.filter(Scholarship.date_added < fifteen_days_ago).delete()
        db.session.commit()
        if old_schemes:
            print(f"{old_schemes} old schemes are deleted..")

   
    queries = [
        "scholarship for all category students india 2026",
        "MahaDBT scholarship updates 2026",
        "private scholarships for education students India"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    added_count = 0
    skipped_count = 0

    for query in queries:
        print(f"Searching: {query}...")
        search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        
        try:
            response = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('a', class_='result__a')

            with app.app_context():
                for link in results:
                    title = link.text.strip()
                    raw_href = link['href']
                    
                     
                    href = clean_url(raw_href)

                    
                    exists = Scholarship.query.filter_by(link=href).first()
                    
                    if not exists:
                        new_scheme = Scholarship(
                            scheme_name=title,
                            link=href,
                            eligibility_criteria="OBC, Maharashtra Resident, UG/PG Student",
                            description="Latest update fetched via ScholarAI Scraper.",
                            date_added=datetime.utcnow() 
                        )
                        db.session.add(new_scheme)
                        added_count += 1
                        print(f"✅ Added: {title[:50]}...")
                    else:
                        skipped_count += 1
                
                db.session.commit()
        except Exception as e:
            print(f"❌ Error in query '{query}': {e}")

    print(f"\n🚀 FINAL REPORT:")
    print(f"🆕 New Schemes: {added_count}")
    print(f"⏭️ Duplicates Skipped: {skipped_count}")

if __name__ == "__main__":
    scrape_scholarships()
