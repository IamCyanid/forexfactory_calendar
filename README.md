This Python bot is designed to automate the process of fetching and notifying you about high-impact economic events from ForexFactory.com. It leverages Selenium for web scraping and `BeautifulSoup` for parsing the HTML content.

Key Features:
* **High-Impact Event Filtering**: The bot specifically identifies and extracts events marked with a "red" impact icon on the ForexFactory calendar, indicating their potential to significantly influence the market.
* **Desktop Notifications**: Upon finding high-impact events, the bot provides a desktop notification summarizing the findings.
* **Detailed Event Saving**: All identified high-impact events for the day are saved to a `High_Impact_Events.txt` file on your desktop, providing a convenient record.
* **Scheduled Runs**: The bot is scheduled to run daily at 07:30 AM New York time, ensuring you receive timely updates before the trading day typically begins.
* **Headless Browser Operation**: It uses a headless Chrome browser, meaning the web scraping occurs in the background without opening a visible browser window.

This tool is ideal for forex traders and financial enthusiasts who want to stay informed about critical economic announcements with minimal manual effort.
