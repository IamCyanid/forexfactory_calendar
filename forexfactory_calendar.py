import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pkg_resources")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup, NavigableString
from plyer import notification
from datetime import datetime
import pytz
import time
import schedule
import random
import os

def save_events_to_desktop(events, filename="High_Impact_Events.txt"):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    filepath = os.path.join(desktop, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("High Impact Economic Events for Today:\n\n")
        for event in events:
            f.write(event + "\n")
    print(f"Events saved to {filepath}")

def fetch_high_impact_events():
    url = "https://www.forexfactory.com/calendar.php"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "icon--ff-impact-red"))
        )
        time.sleep(random.uniform(2, 5))
    except Exception as e:
        print("Timeout waiting for calendar to load:", e)
        driver.quit()
        return []

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    rows = soup.find_all("tr", class_="calendar__row")
    print("Number of event rows found:", len(rows))

    events = []
    for row in rows:
        # Impact cell: must contain the red icon
        impact_cell = row.find("td", class_="calendar__cell calendar__impact")
        if impact_cell is None:
            continue

        is_high_impact = False
        for span in impact_cell.find_all("span"):
            classes = span.get("class", [])
            if "icon--ff-impact-red" in classes:
                is_high_impact = True
                break
        if not is_high_impact:
            continue

        # Time
        time_cell = row.find("td", class_="calendar__cell calendar__time")
        event_time = ""
        if time_cell:
            span = time_cell.find("span")
            event_time = span.text.strip() if span else time_cell.get_text(strip=True)
        # Currency
        currency_cell = row.find("td", class_="calendar__cell calendar__currency")
        currency = ""
        if currency_cell:
            span = currency_cell.find("span")
            currency = span.text.strip() if span else currency_cell.get_text(strip=True)
        # Event name (robust selector: any td with both 'calendar__cell' and 'calendar__event')
        event_cell = row.find(lambda tag: tag.name == "td" and "calendar__cell" in tag.get("class", []) and "calendar__event" in tag.get("class", []))
        event_name = ""
        if event_cell:
            event_title_span = event_cell.find("span", class_="calendar__event-title")
            if event_title_span and event_title_span.text.strip():
                event_name = event_title_span.text.strip()
            else:
                event_name = event_cell.get_text(strip=True)
        print(f"High Impact Event Detected: {event_time} | {currency} | {event_name}")
        if event_name:
            events.append(f"{event_time} | {currency} | {event_name} | High Impact")
    return events

def show_notification(events):
    if not events:
        message = "No HIGH IMPACT economic events found for today."
        notification.notify(
            title="ForexFactory High Impact News",
            message=message,
            timeout=15
        )
        print("Notification message:\n", message)
    else:
        # Save all events to desktop
        save_events_to_desktop(events)
        # Show a short notification
        message = f"{len(events)} high impact events found! See 'High_Impact_Events.txt' on your Desktop."
        notification.notify(
            title="ForexFactory High Impact News",
            message=message,
            timeout=15
        )
        print("Notification message:\n", message)

def job():
    events = fetch_high_impact_events()
    show_notification(events)

def run_scheduler():
    eastern = pytz.timezone("America/New_York")
    now = datetime.now(eastern)
    print(f"Scheduler started. Current NY time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    schedule.every().day.at("07:30").do(job)

    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    # For debugging, you can run job() once:
    # job()
    # For daily scheduling at 07:30 AM NY time:
    run_scheduler()