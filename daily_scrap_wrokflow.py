from typing import List, Dict, Any
from typing_extensions import TypedDict
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, String, Text, Integer, DateTime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import sessionmaker, declarative_base
from prefect import flow, task
import requests
from datetime import datetime

# Define the database URL
DATABASE_URL = "postgresql+psycopg2://postgres:@localhost/postgres"

# Set up the database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class GameHTML(Base):
    __tablename__ = "gmt_availability_scrap_prefect_game_html"
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String, index=True)
    html_content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    stores = Column(JSON, nullable=False)


# Create the table
Base.metadata.create_all(bind=engine)


class Game(TypedDict):
    game_id: str
    game_name: str


@task
def fetch_game_page(game_id: str) -> str:
    url = f"https://bradspelspriser.se/item/show/{game_id}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch data from {url}, status code: {response.status_code}"
        )
    return response.content


@task
def save_html_to_postgres(
    game_id: str, html_content: str, stores: List[Dict[str, Any]]
):
    session = SessionLocal()
    game_html = GameHTML(game_id=game_id, html_content=html_content, stores=stores)
    session.merge(game_html)  # Use merge to handle both insert and update
    session.commit()
    session.close()


@flow(log_prints=True)
def track_availability(games: List[Game]):
    for game in games:
        html_content = fetch_game_page(game["game_id"])
        # Assuming you have logic to extract stores data from the HTML content
        stores = extract_stores_from_html(html_content)
        save_html_to_postgres(game["game_id"], html_content, stores)


def extract_stores_from_html(html_content: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html_content, "html.parser")

    images = soup.select(".storeimage")
    countries = soup.select(".vendorinfo-icon.flag-icon")
    stock = soup.select(".vendorstock")
    price = soup.select(".pricedetails")

    stores = []
    for image, country, stock, price in zip(images, countries, stock, price):
        store_name = image.get("alt", "Unknown Store")
        store_country = country.get("alt", "Unknown Country")
        store_stock = stock.text.strip()
        store_price = price.text.strip()
        stores.append(
            {
                "store_name": store_name,
                "country": store_country,
                "stock": store_stock,
                "price": store_price,
            }
        )
    return stores


# Run the flow
if __name__ == "__main__":
    games: List[Game] = [
        {
            "game_id": "18375",
            "game_name": "1846 Race for the Midwest",
        }
    ]
    track_availability(games)
