# NHS Vaccination Booking Checker

This tool is made to check for earlier availability of vaccine slots on [NHS.uk](https://nhs.uk).

**Disclaimer**: I am not affiliated with the NHS, nor is this tool endorsed by them.

# Dependencies
- Python 3.8 and above
- An already existing vaccination booking

# Installation
Clone the project and run `pip3 install --user .`.
The installation may fail if your `pip` version is too old, YMMV.

# Configuration

Run `nhs-vaccination-checker` to create and set up a blank config.

```
[DEFAULT]
nhs_number = XXXXXXXXX
date_of_birth = YYYY-MM-DD
booking_reference = XXXXXXXX
pushbullet_token = o.XXXXXXXX
```

# Usage

```
Usage: nhs-vaccination-checker [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  appointment               Get your current appointment.
  check                     Checks for available appointments.
  notify                    Checks the NHS page every 6 hours for new...
  test-notification-system  Tests if notification system works.
  version                   Display application version.
```
