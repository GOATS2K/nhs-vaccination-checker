from nhs_vaccination_checker.exceptions import NotLoggedInError
from typing import Dict, Union
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from dataclasses import dataclass

from requests.models import Response


@dataclass
class Location:
    name: str
    address: str
    city: str
    post_code: str


@dataclass
class Appointment:
    location: Location
    time: datetime


class NHSChecker:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"  # noqa: E501
        }
        self.logged_in = False

    @property
    def appointment(self) -> Appointment:
        if self.logged_in:
            return self._get_current_booking()

        raise NotLoggedInError("You must be logged in to see your appointment!")

    def _extract_request_token(self, content: Response.content, token_name: str):
        soup = BeautifulSoup(content, "html.parser")
        request_token_field = soup.find("input", {"name": token_name})
        return request_token_field["value"]

    def _get_request_token_from_page(
        self, url: str, token_name: str = "__RequestVerificationToken"
    ) -> str:
        get = self.session.get(url, headers=self.header)
        return self._extract_request_token(get.content, token_name)

    def _post_data(self, url: str, data: Dict[str, Union[str, int]]) -> str:
        post = self.session.post(url, headers=self.header, data=data)
        return post.url

    def _select_nhs_option(self) -> str:
        url = "https://www.nhs.uk/book-a-coronavirus-vaccination/do-you-have-an-nhs-number"  # noqa: E501
        request_token = self._get_request_token_from_page(url)
        data = {"SelectedOption": "Yes", "__RequestVerificationToken": request_token}
        next_url = self._post_data(url, data)
        return next_url

    def _enter_nhs_number(self, url: str, nhs_number: int) -> str:
        request_token = self._get_request_token_from_page(url)
        data = {"NhsNumber": nhs_number, "__RequestVerificationToken": request_token}
        next_url = self._post_data(url, data)
        return next_url

    def _enter_date_of_birth(self, url: str, date_of_birth: str) -> str:
        request_token = self._get_request_token_from_page(url)
        correlation_token = self._get_request_token_from_page(
            url, token_name="CorrelationId"
        )
        date_obj = datetime.strptime(date_of_birth, "%Y-%m-%d")
        data = {
            "CorrelationId": correlation_token,
            "Date.Day": date_obj.day,
            "Date.Month": date_obj.month,
            "Date.Year": date_obj.year,
            "__RequestVerificationToken": request_token,
        }
        next_url = self._post_data(url, data)
        return next_url

    def _enter_booking_reference(self, url: str, booking_ref: int):
        request_token = self._get_request_token_from_page(url)
        data = {
            "BookingReference": booking_ref,
            "__RequestVerificationToken": request_token,
        }
        next_url = self._post_data(url, data=data)
        return next_url

    def login(self, nhs_number: int, date_of_birth: str, booking_ref: int) -> str:
        nhs_num_url = self._select_nhs_option()
        dob_url = self._enter_nhs_number(nhs_num_url, nhs_number)
        booking_ref_url = self._enter_date_of_birth(dob_url, date_of_birth)
        profile_url = self._enter_booking_reference(booking_ref_url, booking_ref)

        if (
            profile_url
            == "https://www.nhs.uk/book-a-coronavirus-vaccination/current-bookings"
        ):
            self.logged_in = True

    def _parse_appointment(self, content: Response.content) -> Appointment:
        soup = BeautifulSoup(content, "html.parser")
        appointment_card = soup.find(
            "div", {"class": "nhsuk-card nhsuk-u-margin-top-0"}
        )
        all_p_tags = appointment_card.find_all("p")
        location = all_p_tags[0].contents
        time = all_p_tags[-1].string

        # Clean line breaks and weird spaces from paragraph
        appointment_location = [
            str(detail).strip()
            for detail in location
            if not str(detail).strip() == "<br/>"
        ]

        location_data = Location(
            name=appointment_location[0],
            address=appointment_location[1],
            city=appointment_location[2],
            post_code=appointment_location[3],
        )

        formatted_date = datetime.strptime(time, "%d %B at %H:%M%p")

        # Since the NHS doesn't give us a year, we have to set it ourselves.
        formatted_date = formatted_date.replace(year=datetime.now().year)

        appointment = Appointment(location=location_data, time=formatted_date)

        return appointment

    def _get_current_booking(self) -> Dict[str, str]:
        r = self.session.get(
            "https://www.nhs.uk/book-a-coronavirus-vaccination/current-bookings"
        )
        return self._parse_appointment(r.content)

    def _store_future_booking(self):
        pass

    def check_availability(self):
        pass
