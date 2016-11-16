# Titanic

A Python script that send emails when a specific French business is officially closed.

## Prerequisites

Python 3.

## Installation

Clone this repo, and then the usual `pip install -r requirements.txt`.

## Configuration

Copy the `.env.example` file to `.env` and fill in the configuration parameters.

Available configuration parameters are:

  - `SURVIVORS` A comma-separated list of emails that will receive the "Titanic sunk!" email
  - `SIREN` The [SIREN](https://en.wikipedia.org/wiki/SIREN_code) of the business to check for (no spaces)
  - `SMTP_*` Self-explanatory parameters

## Usage

```
python run.py [--drill]
```

`--drill` make the specified business randomly closed or not to test emails sending.

Best usage is to create a CRON job that launch Titanic once a day (more is useless):

```
# Every day at 6PM
0 18 * * * cd /path/to/titanic && python run.py 2>&1
```

## How it works

This script use the [Firmapi](https://firmapi.com/) service to check if the specified business
(`SIREN` parameter) is unlisted from the [RCS](https://en.wikipedia.org/wiki/List_of_company_registers#France).
If yes, emails are sent through SMTP (`SMTP_*` parameters) to the specified recipients (`SURVIVORS` parameter). A file
is then created in the same directory (`{SIREN}.sank`) to prevent further useless calls to Firmapi.
