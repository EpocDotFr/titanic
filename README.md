# Titanic

A Python script that send emails when a specific French business is officially closed.

## Prerequisites

Python 3.

## Installation

Clone this repo, and then the usual `pip install -r requirements.txt`.

## Configuration

Copy the `.env.example` file to `.env` and fill in the configuration parameters.

Available configuration parameters are:

  - `TIMEZONE` Self-explanatory parameter
  - `SURVIVORS` A comma-separated list of emails that will receive the "Titanic sunk!" email
  - `SIREN` The [SIREN](https://en.wikipedia.org/wiki/SIREN_code) of the business to check for (no spaces)
  - `SMTP_*` Self-explanatory parameters

## Usage

```
python run.py [--drill]
```

`--drill` make the specified business randomly closed or not to test emails sending.

## How it works

This script use the [Firmapi](https://firmapi.com/) service to check if the specified business
(`SIREN` parameter) is unlisted from the [RCS](https://fr.wikipedia.org/wiki/Registre_du_commerce_et_des_sociétés_(France)).
If yes, emails are sent through SMTP (`SMTP_*` parameters) to the specified recipients (`SURVIVORS` parameter). A file
is then created (`{SIREN}.sank`) to prevent further useless calls to Firmapi.