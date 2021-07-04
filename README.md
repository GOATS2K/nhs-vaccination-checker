# NHS Vaccination Booking Checker

This tool is made to check for earlier availability of vaccine slots on [NHS.uk](https://nhs.uk).

# Dependencies
- Python 3.8 and above
- An already existing vaccination booking

# Installation
Clone the project and run `pip3 install --user`.

# Usage
```
Usage: nhs-vaccination-checker [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  appointment  Get your current appointment.
  check        Checks for available appointments.
  version      Display application version.
```

Check for available appointments:

`nhs-vaccination-checker check --nhs-number XXXXXXXXXX --dob XXXX-XX-XX --booking-reference XXXXXXXX`