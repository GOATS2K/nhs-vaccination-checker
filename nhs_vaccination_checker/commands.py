import click
from nhs_vaccination_checker.checker import NHSChecker
from nhs_vaccination_checker import __version__


@click.group()
def cli():
    pass


@cli.command(help="Get your current appointment.")
@click.option("--nhs-number", type=click.INT, help="Your NHS number, without spaces.")
@click.option(
    "--dob", type=click.STRING, help="Your date of birth, formatted as YYYY-MM-DD."
)
@click.option("--booking-reference", type=click.INT, help="Your booking reference.")
def appointment(nhs_number: int, dob: str, booking_reference: int):
    n = NHSChecker()
    n.login(nhs_number=nhs_number, date_of_birth=dob, booking_ref=booking_reference)
    appointment = n.appointment

    click.secho(
        f"Appointment location: {appointment.location.name}", fg="yellow",
    )
    click.secho(
        f"{appointment.location.city} • {appointment.location.address} • {appointment.location.post_code}",  # noqa: E501
        fg="yellow",
    )
    click.secho(f"At {appointment.time.strftime('%Y-%m-%d %H:%M')}", fg="blue")


@cli.command(help="Display application version.")
def version():
    click.echo(__version__)
