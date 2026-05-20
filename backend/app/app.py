from flask import Flask

from routes.menu import combos
from routes.menu import combo_detalle
from routes.menu import combo_version
from routes.menu import productos
from routes.reservas import reservas
from routes.resenias import resenias
from routes.servicios_extras import servicios_extra

app = Flask(__name__)

app.register_blueprint(combos)
app.register_blueprint(combo_detalle)
app.register_blueprint(combo_version)
app.register_blueprint(productos)
app.register_blueprint(reservas)
app.register_blueprint(resenias)
app.register_blueprint(servicios_extra)

if __name__ == '__main__':
    app.run(debug=True, port=5000)