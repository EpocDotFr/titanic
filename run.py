from envparse import env, Env
from envelopes import Envelope
import random
import arrow
import click
import requests
import os
import logging
import sys


ENDPOINT = 'https://firmapi.com/api/v1/'


def debug(message, err=False, terminate=False):
    """Log a regular or error message to the standard output, optionally terminating the script."""
    logging.getLogger().log(logging.ERROR if err else logging.INFO, message)

    if terminate:
        sys.exit(1)


def get_titanic(drill=False):
    titanic_status_response = requests.get(ENDPOINT+'companies/'+env('SIREN'))
    
    titanic_status_response_json = titanic_status_response.json()
    
    if 'status' not in titanic_status_response_json:
        raise Exception('Illegal Firmapi response')
    
    if titanic_status_response_json['status'] != 'success':
        raise Exception(titanic_status_response_json['message'])

    if drill:
        titanic_status_response_json['company']['radie'] = bool(random.getrandbits(1))

    return titanic_status_response_json['company']


@click.command()
@click.option('--drill', is_flag=True, default=False, help='Test mode')
def run(drill):
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
        stream=sys.stdout
    )

    logging.getLogger().setLevel(logging.INFO)

    Env.read_envfile('.env')

    survivors = env('SURVIVORS', cast=list, subcast=str)

    smtp_login = env('SMTP_LOGIN')
    smtp_password = env('SMTP_PASSWORD')
    smtp_host = env('SMTP_HOST')
    smtp_port = env('SMTP_PORT')
    smtp_tls = env.bool('SMTP_TLS', default=False)

    if drill:
        debug('[Drill mode]')

    try:
        sank_file = env('SIREN')+'.sank'
        
        if os.path.exists(sank_file):
            raise Exception('Titanic already sank, aborting')

        debug('Getting Titanic\'s status...')
        
        titanic = get_titanic(drill)
        
        debug('Checking Titanic\'s status...')

        if titanic['radie']:
            since = arrow.get(titanic['last_legal_update']).format('MMM, D YYYY')

            debug('Titanic sunk! {} isn\'t no more since {}!'.format(titanic['names']['best'], since))
            debug('There\'s {} survivors to contact.'.format(len(survivors)))
            
            debug('Sending telegrams to the survivors...')

            envelope = Envelope(
                from_addr=(smtp_login, 'The Titanic'),
                to_addr=survivors,
                subject='Titanic sunk!',
                html_body="""<h1>Ohmy, Titanic sunk!</h1>
                <p>There it is. {company} isn\'t, officially since <b>{since}</b>.</p>
                <p style="text-align: center"><img src="https://media.giphy.com/media/hmxZRW8mhs4ak/giphy.gif"></p>
                <p>Thank you all.</p>
                <hr>
                <p><small>This email was automatically sent by the <a href="https://github.com/EpocDotFr/titanic">Titanic</a>. Please don\'t reply.</small></p>""".format(company=titanic['names']['best'], since=since)
            )

            envelope.send(smtp_host, login=smtp_login, password=smtp_password, port=smtp_port, tls=smtp_tls)

            debug('Telegrams sent successfully!')

            open(sank_file, 'a').close()
        else:
            debug('Titanic still floating')
    except Exception as e:
        debug('  > {}'.format(e), err=True)

if __name__ == '__main__':
    run()
