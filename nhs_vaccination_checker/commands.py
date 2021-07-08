import time
import sys
from datetime import datetime
from nhs_vaccination_checker.notify import notify_user, test_notification
from typing import List
import click

from nhs_vaccination_checker import __version__
from nhs_vaccination_checker.checker import NHSChecker

from nhs_vaccination_checker import config


def get_early_appointments(n: NHSChecker) -> List[str]:
    current_appointment = n.appointment.time
    available_appointments = n.available_appointments

    if available_appointments:
        early_appointments = [
            booking
            for booking in available_appointments
            if booking < current_appointment
        ]

    return early_appointments


@click.group()
def cli():
    pass


@cli.command(help="Get your current appointment. Uses config variables by default.")
@click.option("--nhs-number", type=click.INT, help="Your NHS number, without spaces.")
@click.option(
    "--dob", type=click.STRING, help="Your date of birth, formatted as YYYY-MM-DD."
)
@click.option("--booking-reference", type=click.INT, help="Your booking reference.")
def appointment(nhs_number: int, dob: str, booking_reference: int):
    n = NHSChecker()

    if not nhs_number:
        nhs_number = config.get("DEFAULT", "nhs_number")

    if not dob:
        dob = config.get("DEFAULT", "date_of_birth")

    if not booking_reference:
        booking_reference = config.get("DEFAULT", "booking_reference")

    n.login(nhs_number=nhs_number, date_of_birth=dob, booking_ref=booking_reference)
    appointment = n.appointment

    click.secho(
        f"Appointment location: {appointment.location.name}",
        fg="yellow",
    )
    click.secho(
        f"{appointment.location.city} • {appointment.location.address} • {appointment.location.post_code}",  # noqa: E501
        fg="yellow",
    )
    click.secho(f"At {appointment.time.strftime('%Y-%m-%d %H:%M')}", fg="blue")


@cli.command(
    help="Checks for available appointments. Uses config variables by default."
)
@click.option("--nhs-number", type=click.INT, help="Your NHS number, without spaces.")
@click.option(
    "--dob", type=click.STRING, help="Your date of birth, formatted as YYYY-MM-DD."
)
@click.option("--booking-reference", type=click.INT, help="Your booking reference.")
def check(nhs_number: int, dob: str, booking_reference: int):
    n = NHSChecker()

    if not nhs_number:
        nhs_number = config.get("DEFAULT", "nhs_number")

    if not dob:
        dob = config.get("DEFAULT", "date_of_birth")

    if not booking_reference:
        booking_reference = config.get("DEFAULT", "booking_reference")

    n.login(nhs_number=nhs_number, date_of_birth=dob, booking_ref=booking_reference)
    early_appointments = get_early_appointments(n)

    if early_appointments:
        click.secho(
            f"You have {len(early_appointments)} earlier booking(s) to choose from: ",
            fg="green",
        )
        for appointment in early_appointments:
            click.echo(appointment.strftime("%Y-%m-%d"))
    else:
        click.secho("No earlier bookings are available.", fg="red")


@cli.command(help="Tests if notification system works.")
def test_notification_system():
    if not config.get("DEFAULT", "pushbullet_token"):
        click.secho(
            "You need to set the 'pushbullet_token' variable in your config to be able to use this function.",  # noqa: E501
            fg="red",
        )
        sys.exit(1)

    test_notification()
    click.secho("Sent test notification!", fg="green")


@cli.command(
    help="Checks the NHS page every 6 hours for new bookings and notifies if found."
)
@click.option("--nhs-number", type=click.INT, help="Your NHS number, without spaces.")
@click.option(
    "--dob", type=click.STRING, help="Your date of birth, formatted as YYYY-MM-DD."
)
@click.option("--booking-reference", type=click.INT, help="Your booking reference.")
def notify(nhs_number: int, dob: str, booking_reference: int):
    if not config.get("DEFAULT", "pushbullet_token"):
        click.secho(
            "You need to set the 'pushbullet_token' variable in your config to be able to use this function.",  # noqa: E501
            fg="red",
        )
        sys.exit(1)

    n = NHSChecker()

    if not nhs_number:
        nhs_number = config.get("DEFAULT", "nhs_number")

    if not dob:
        dob = config.get("DEFAULT", "date_of_birth")

    if not booking_reference:
        booking_reference = config.get("DEFAULT", "booking_reference")

    while True:
        n.login(nhs_number=nhs_number, date_of_birth=dob, booking_ref=booking_reference)
        early_appointments = get_early_appointments(n)

        if early_appointments:
            click.secho(
                f"[{datetime.now()}] Notifying user about an early appointment.",
                fg="green",
            )
            for apt in early_appointments:
                notify_user(apt)
        else:
            click.secho(f"[{datetime.now()}] No appointment found.", fg="red")

        click.secho(f"[{datetime.now()}] Sleeping for 6 hours.")
        time.sleep(21600)


@cli.command(help="Display application version.")
def version():
    click.echo(__version__)
