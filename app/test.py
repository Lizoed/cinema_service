import requests
import uuid
from datetime import datetime, time, timedelta

BASE_URL = "http://localhost:8000"


def print_response(response):
    print(f"Status Code: {response.status_code}")
    print("Response:")
    try:
        print(response.json())
    except ValueError:
        print(response.text)
    print("-" * 50)


def test_cinema_hall_endpoints():
    print("\n=== Testing Cinema Hall Endpoints ===")

    print("\nTest 1: Create cinema hall with invalid data")
    invalid_data = {
        "address": "",
        "capacity": -10,
        "opening_time": "25:00:00",
        "closing_time": "09:00:00"
    }
    response = requests.post(f"{BASE_URL}/cinema_hall/", json=invalid_data)
    print_response(response)

    print("\nTest 2: Create valid cinema hall")
    cinema_hall_data = {
        "address": "Пушкина 123",
        "capacity": 100,
        "opening_time": "09:00:00",
        "closing_time": "23:00:00"
    }
    response = requests.post(f"{BASE_URL}/cinema_hall/", json=cinema_hall_data)
    print_response(response)

    if response.status_code != 200:
        print("Failed to create cinema hall, skipping further tests")
        return

    cinema_hall_id = response.json().get("id")
    if not cinema_hall_id:
        print("No cinema hall ID in response, skipping further tests")
        return

    print("\nTest 3: Get all cinema halls")
    response = requests.get(f"{BASE_URL}/cinema_hall/")
    print_response(response)

    if response.status_code == 200:
        halls = response.json()
        if halls and isinstance(halls, list):
            hall = halls[0]
            required_fields = {'id', 'address', 'capacity'}
            if not all(field in hall for field in required_fields):
                print("Error: Missing required fields in cinema hall response")

    print("\nTest 4: Get non-existent cinema hall")
    fake_id = uuid.uuid4()
    response = requests.get(f"{BASE_URL}/cinema_hall/{fake_id}")
    print_response(response)

    print("\nTest 5: Get cinema hall details")
    response = requests.get(f"{BASE_URL}/cinema_hall/{cinema_hall_id}")
    print_response(response)

    if response.status_code == 200:
        hall_details = response.json()
        required_fields = {'id', 'address', 'capacity', 'opening_time', 'closing_time', 'seats'}
        if not all(field in hall_details for field in required_fields):
            print("Error: Missing required fields in cinema hall details")
        if not isinstance(hall_details.get('seats'), list):
            print("Error: Seats should be a list")


def test_film_endpoints():
    print("\n=== Testing Film Endpoints ===")

    print("\nTest 1: Create film with invalid data")
    invalid_data = {
        "name": 23,
        "duration": 10
    }
    response = requests.post(f"{BASE_URL}/film/", json=invalid_data)
    print_response(response)

    print("\nTest 2: Create valid film")
    film_data = {
        "name": "Криминальное чтиво",
        "duration": 148
    }
    response = requests.post(f"{BASE_URL}/film/", json=film_data)
    print_response(response)

    if response.status_code != 200:
        print("Failed to create film, skipping further tests")
        return

    film_id = response.json().get("id")
    if not film_id:
        print("No film ID in response, skipping further tests")
        return

    print("\nTest 3: Get all films")
    response = requests.get(f"{BASE_URL}/film/")
    print_response(response)

    if response.status_code == 200:
        films = response.json()
        if films and isinstance(films, list):
            film = films[0]
            required_fields = {'id', 'name', 'duration', 'is_active'}
            if not all(field in film for field in required_fields):
                print("Error: Missing required fields in films response")

    print("\nTest 4: Get active films")
    response = requests.get(f"{BASE_URL}/film/?is_active=true")
    print_response(response)


def test_screening_endpoints():
    print("\n=== Testing Screening Endpoints ===")

    cinema_hall_data = {
        "address": "Площадь Победы 1",
        "capacity": 50,
        "opening_time": "10:00:00",
        "closing_time": "22:00:00"
    }
    cinema_hall_response = requests.post(f"{BASE_URL}/cinema_hall/", json=cinema_hall_data)
    if cinema_hall_response.status_code != 200:
        print("Failed to create cinema hall, skipping screening tests")
        return

    cinema_hall_id = cinema_hall_response.json().get("id")
    if not cinema_hall_id:
        print("No cinema hall ID in response, skipping screening tests")
        return

    film_data = {
        "name": "Матрица",
        "duration": 136
    }
    film_response = requests.post(f"{BASE_URL}/film/", json=film_data)
    if film_response.status_code != 200:
        print("Failed to create film, skipping screening tests")
        return

    film_id = film_response.json().get("id")
    if not film_id:
        print("No film ID in response, skipping screening tests")
        return

    print("\nTest 1: Create screening with invalid data")
    invalid_data = {
        "start_time": "invalid_datetime",
        "price": -100,
        "film_id": "invalid_uuid",
        "cinema_hall_id": "invalid_uuid"
    }
    response = requests.post(f"{BASE_URL}/screening/", json=invalid_data)
    print_response(response)


    print("\nTest 2: Create valid screening")
    screening_time = datetime.now() + timedelta(hours=2)
    screening_data = {
        "start_time": screening_time.isoformat(),
        "price": 250.50,
        "film_id": film_id,
        "cinema_hall_id": cinema_hall_id
    }
    response = requests.post(f"{BASE_URL}/screening/", json=screening_data)
    print_response(response)

    if response.status_code != 200:
        print("Failed to create screening, skipping further tests")
        return

    screening_id = response.json().get("id")
    if not screening_id:
        print("No screening ID in response, skipping further tests")
        return

    print("\nTest 3: Create overlapping screening")
    overlapping_time = screening_time + timedelta(minutes=30)
    screening_data = {
        "start_time": overlapping_time.isoformat(),
        "price": 300.00,
        "film_id": film_id,
        "cinema_hall_id": cinema_hall_id
    }
    response = requests.post(f"{BASE_URL}/screening/", json=screening_data)
    print_response(response)

    print("\nTest 4: Get all screenings")
    response = requests.get(f"{BASE_URL}/screening/")
    print_response(response)

    if response.status_code == 200:
        screenings = response.json()
        if screenings and isinstance(screenings, list):
            screening = screenings[0]
            required_fields = {'id', 'start_time', 'price'}
            if not all(field in screening for field in required_fields):
                print("Error: Missing required fields in screenings response")

    print("\nTest 5: Get screenings by cinema hall ID")
    response = requests.get(f"{BASE_URL}/screening/?cinema_hall_id={cinema_hall_id}")
    print_response(response)

    print("\nTest 6: Get screenings by film ID")
    response = requests.get(f"{BASE_URL}/screening/?film_id={film_id}")
    print_response(response)

    print("\nTest 7: Get non-existent screening")
    fake_id = uuid.uuid4()
    response = requests.get(f"{BASE_URL}/screening/{fake_id}")
    print_response(response)

    print("\nTest 8: Get screening details")
    response = requests.get(f"{BASE_URL}/screening/{screening_id}")
    print_response(response)

    if response.status_code == 200:
        screening_details = response.json()
        required_fields = {'id', 'start_time', 'end_time', 'price', 'film', 'cinema_hall', 'free_seats'}
        if not all(field in screening_details for field in required_fields):
            print("Error: Missing required fields in screening details")
        if not isinstance(screening_details.get('free_seats'), list):
            print("Error: Free seats should be a list")


def test_booking_endpoints():
    print("\n=== Testing Booking Endpoints ===")

    cinema_hall_data = {
        "address": "Неизвестная 8",
        "capacity": 30,
        "opening_time": "10:00:00",
        "closing_time": "23:00:00"
    }
    cinema_hall_response = requests.post(f"{BASE_URL}/cinema_hall/", json=cinema_hall_data)
    if cinema_hall_response.status_code != 200:
        print("Failed to create cinema hall, skipping booking tests")
        return

    cinema_hall_id = str(cinema_hall_response.json().get("id"))
    if not cinema_hall_id:
        print("No cinema hall ID in response, skipping booking tests")
        return

    film_data = {
        "name": "Интерстеллар",
        "duration": 169
    }
    film_response = requests.post(f"{BASE_URL}/film/", json=film_data)
    if film_response.status_code != 200:
        print("Failed to create film, skipping booking tests")
        return

    film_id = str(film_response.json().get("id"))
    if not film_id:
        print("No film ID in response, skipping booking tests")
        return

    screening_time = datetime.now() + timedelta(hours=3)
    screening_data = {
        "start_time": screening_time.isoformat(),
        "price": 500.00,
        "film_id": film_id,
        "cinema_hall_id": cinema_hall_id
    }
    screening_response = requests.post(f"{BASE_URL}/screening/", json=screening_data)
    if screening_response.status_code != 200:
        print("Failed to create screening, skipping booking tests")
        return

    screening_id = str(screening_response.json().get("id"))
    if not screening_id:
        print("No screening ID in response, skipping booking tests")
        return

    screening_details = requests.get(f"{BASE_URL}/screening/{screening_id}")
    if screening_details.status_code != 200:
        print("Failed to get screening details, skipping booking tests")
        return

    try:
        free_seats = screening_details.json().get("free_seats", [])
        if not free_seats:
            print("No free seats available, skipping booking tests")
            return

        seat_id = str(free_seats[0].get("id"))
        if not seat_id:
            print("No seat ID in response, skipping booking tests")
            return
    except (ValueError, AttributeError):
        print("Invalid response format, skipping booking tests")
        return

    print("\nTest 1: Book non-existent screening")
    fake_screening_id = str(uuid.uuid4())
    booking_data = {
        "screening_id": fake_screening_id,
        "seat_id": seat_id,
        "client_name": "Джон Дое"
    }
    response = requests.post(f"{BASE_URL}/booking/", json=booking_data)
    print_response(response)

    print("\nTest 2: Book non-existent seat")
    fake_seat_id = str(uuid.uuid4())
    booking_data = {
        "screening_id": screening_id,
        "seat_id": fake_seat_id,
        "client_name": "Джон Дое"
    }
    response = requests.post(f"{BASE_URL}/booking/", json=booking_data)
    print_response(response)

    print("\nTest 3: Create valid booking")
    booking_data = {
        "screening_id": screening_id,
        "seat_id": seat_id,
        "client_name": "Джон Дое"
    }
    response = requests.post(f"{BASE_URL}/booking/", json=booking_data)
    print_response(response)

    if response.status_code != 200:
        print("Failed to create booking, skipping cancel test")
        return

    booking_id = str(response.json().get("id"))
    if not booking_id:
        print("No booking ID in response, skipping cancel test")
        return

    print("\nTest 4: Book already booked seat")
    response = requests.post(f"{BASE_URL}/booking/", json=booking_data)
    print_response(response)

    print("\nTest 5: Cancel non-existent booking")
    fake_booking_id = str(uuid.uuid4())
    response = requests.delete(f"{BASE_URL}/booking/{fake_booking_id}")
    print_response(response)

    print("\nTest 6: Cancel valid booking")
    response = requests.delete(f"{BASE_URL}/booking/{booking_id}")
    print_response(response)

    print("\nTest 7: Cancel already cancelled booking")
    response = requests.delete(f"{BASE_URL}/booking/{booking_id}")
    print_response(response)



if __name__ == "__main__":
    test_cinema_hall_endpoints()
    test_film_endpoints()
    test_screening_endpoints()
    test_booking_endpoints()
    print("\nAll tests completed!")