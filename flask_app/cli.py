# flask_app/cli.py
import click, csv
from shared.db import SessionLocal, engine, Base
import shared.models as models

@click.group()
def cli():
    pass

@cli.command('init-db')
def init_db():
    Base.metadata.create_all(bind=engine)
    click.echo('Created tables.')

@cli.command('import-participants')
@click.argument('csvfile')
def import_participants(csvfile):
    db = SessionLocal()
    created = 0
    with open(csvfile, encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            p = models.Participant(name=row['name'], phone=row.get('phone'))
            db.add(p)
            created += 1
        db.commit()
    click.echo(f'Imported {created} participants')

if __name__ == '__main__':
    cli()
