{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "MyCaptain_Web Scraping Recreation",
      "provenance": [],
      "collapsed_sections": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "metadata": {
        "id": "beSHabkvG3_q"
      },
      "source": [
        "# Project 2: Web Scraper using BeautifulSoup4 and requests"
      ],
      "execution_count"
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Fa70gnWfhUGO"
      },
      "source": [
        "# pip install db-sqlite3"
      ],
      "execution_count"
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "0XpqrlCAfU83"
      },
      "source": [
        "import sqlite3\n",
        "\n",
        "def connect(dbname) :\n",
        "\n",
        "  conn = sqlite3.connect(dbname)\n",
        "\n",
        "  conn.execute(\"CREATE TABLE IF NOT EXSITS OYO_HOTELS (NAME TEXT, ADDRESS TEXT, PRICE INT, AMENITIES TEXT, RATING TEXT)\")\n",
        "\n",
        "  print(\"Table created successfully!\")\n",
        "\n",
        "  conn.close()\n",
        "\n",
        "\n",
        "def insert_into_table(dbname, values):\n",
        "  conn = sqlite3.connect(dbname)\n",
        "  print(\"Inserted into table: \" + str(values))\n",
        "  insert_sql = \"INSERT INTO OYO_HOTELS (NAME, ADDRESS, PRICE, AMENITIES, RATING) VALUES (?, ?, ?, ?, ?)\" \n",
        "\n",
        "  conn.execute(insert_sql, values)\n",
        "\n",
        "  conn.commit()\n",
        "  conn.close()\n",
        "\n",
        "\n",
        "def get_hotel_info(dbname) :\n",
        "  conn = sqlite3.connect(dbname\n",
        "\n",
        "  cur = conn.cursor()\n",
        "\n",
        "  cur.execute(\"SELECT * FROM OYO_HOTELS\")\n",
        "\n",
        "  table_data = cur.fetchall()\n",
        "\n",
        "  for record in table_data:\n",
        "    print(record)\n",
        "\n",
        "  conn.close()"
      ],
      "execution_count"
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "SlDGz_HqHapI"
      },
      "source": [
        "import requests\n",
        "from bs4 import BeautifulSoup\n",
        "import pandas\n",
        "import argparse\n",
        "\n",
        "parser = argparse.ArgumentParser()\n",
        "parser.add_argument(\"--page_num_max\", help=\"Enter the number of pages to parse\", type=int)\n",
        "parser.add_argument(\"--dbname\", help=\"Enter the number of pages to parse\", type=int)\n",
        "args = parser.parse_args()\n",
        "\n",
        "oyo_url = \"https://www.oyorooms.com/hotels-in-bangalore/?page=\"\n",
        "page_num_MAX = args.page_num_max\n",
        "scraped_info_list = []\n",
        "connect(args.dbname)\n",
        "\n",
        "for page_num in range(1, page_num_MAX) :\n",
        "  url = oyo_url + str(page_num) \n",
        "  print(\"Get request for: \" + url)\n",
        "  req = requests.get(url)\n",
        "  content = req.content\n",
        "\n",
        "  soup = BeautifulSoup(content, \"html.parser\")\n",
        "\n",
        "  all_hotels = soup.find_all(\"div\", {\"class\": \"hotelCardListing\"})\n",
        "\n",
        "  for hotel in all_hotels:\n",
        "    hotel_dict = {}\n",
        "    hotel_dict[\"name\"] = hotel.find(\"h3\", {\"class\": \"listingHotelDescription__hotelName\"}).text\n",
        "    hotel_dict[\"address\"] = hotel.find(\"span\", {\"itemprop\": \"streetAddress\"}).text\n",
        "    hotel_dict[\"price\"] = hotel.find(\"span\", {\"class\": \"listingPrice_finalPrice\"}).text\n",
        "\n",
        "\n",
        "    try:\n",
        "      hotel_dict[\"rating\"] = hotel.find(\"span\", {\"class\": \"hotelRating__ratingSummary\"}).text\n",
        "    except AttributeError:\n",
        "      hotel_dict[\"rating\"] = None \n",
        "    \n",
        "    parent_amenities_element = hotel.find(\"div\", {\"class\": \"amenityWrapper\"})\n",
        "\n",
        "    amenities_list = []\n",
        "    for amenity in parent_amenities_element.find_all(\"div\", {\"class\": \"amenityWrapper__amenity\"}):\n",
        "      amenities_list.append(amenity.find(\"span\", {\"class\": \"d-body-sm\"}).text.strip())\n",
        "\n",
        "    hotel_dict[\"amenities\"] = ', '.join(amenities_list[:-1])\n",
        "\n",
        "    scraped_info_list.append(hotel_dict)\n",
        "    insert_into_table(args.dbname, tuple(hotel_dict.values()))\n",
        "\n",
        "\n",
        "dataFrame = pandas.DataFrame(scraped_info_list)\n",
        "print(\"Creating csv file...\")\n",
        "dataFrame.to_csv(\"Oyo.csv\") \n",
        "\n",
        "get_hotel_info(args.dbname)\n"
      ],
      "execution_count"
      "outputs": []
    }
  ]
}