# Importē nepieciešamās bibliotēkas
import sqlite3
import click
from flask import current_app, g


# Funkcija, kas savienojas ar datubāzi un izveido viegli izmantojamu pieeju tai
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


# Aizver savienojumu ar datubāzi
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# Ja datubāze neeksistē tad izveido to, izmantojot schema.sql aprakstīto datubāzes uzbūvi
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# Funkcija, kas atļauj viegli ierakstīt konsolē komandu, kas izveido vai pāraksta datubāzi pa jaunam
@click.command('init-db')
def init_db_command():
    init_db()
    # Parāda konsolē ziņojumu
    click.echo('Datubāze izveidota!')


# Padod Flask objektam zināšanas, kā izveidot un aizvērt datubāzi
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
