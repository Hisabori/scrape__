from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient


def fetch_html_content(url):
    """Fetch HTML content from the specified URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get ( url, headers=headers )
    response.raise_for_status ()
    return response.text


def parse_html_to_extract_doctor_details(html):
    """Parse HTML to extract doctor details."""
    soup = BeautifulSoup(html, 'html.parser' )
    doctors = []
    team_container = soup.find('div', class_='medical_team_introduction')
    if not team_container:
        print ( "Team container not found." )
        return doctors

    for item in team_container.find_all ('li'):
        name = item.find('span', class_='mtip_name')
        name = name.get_text ( strip=True ) if name else 'Unknown'

        areas = 'Not Available'
        career = 'Not Available'
        activities = 'Not Available'

        for detail in item.find_all ( 'div', class_='mti_list' ):
            for info in detail.find_all ( 'li' ):
                title = info.find ( 'span', class_='mtil_title' )
                description = info.find ( 'p', class_='mtil_descript' )

                if title and description:
                    title_text = title.get_text ( strip=True )
                    description_text = description.get_text ( strip=True )

                    if '진료분야' in title_text:
                        areas = description_text
                    elif '주요경력' in title_text:
                        career = description_text
                    elif '학회활동' in title_text:
                        activities = description_text

        doctors.append ( {
            'name': name,
            'areas': areas,
            'career': career,
            'activities': activities
        } )

    return doctors


def save_to_mongodb(data):
    """Save data to MongoDB."""
    client = MongoClient ( 'localhost', 27017 )  # Connect to MongoDB
    db = client['hospital']  # Database name
    collection = db['doctors']  # Collection name
    collection.insert_many ( data )  # Insert data


def main():
    url = 'https://ncmh.go.kr/medical/board/deptMemberList.do?part_cate=A&menu_cd=01_03_00_01'
    try:
        html_content = fetch_html_content ( url )
        doctor_details = parse_html_to_extract_doctor_details ( html_content )
        if doctor_details:
            save_to_mongodb ( doctor_details )
            print ( "Doctor details have been successfully saved to MongoDB." )
        else:
            print ( "No doctor details found." )
    except Exception as e:
        print ( "An error occurred:", e )


if __name__ == "__main__":
    main ()
