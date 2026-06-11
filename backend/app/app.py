from dotenv import load_dotenv
load_dotenv()
from flask import Flask

from routes.combos import combos
from routes.combo_detalle import combo_detalle
from routes.combo_version import combo_version
from routes.productos import productos
from routes.reservas import reservas
from routes.resenias import resenias
from routes.servicios_extra import servicios_extra
from routes.reportes import reportes
from routes.auth import auth         
from routes.usuarios import usuarios 

app = Flask(__name__)

app.register_blueprint(combos)
app.register_blueprint(combo_detalle)
app.register_blueprint(combo_version)
app.register_blueprint(productos)
app.register_blueprint(reservas)
app.register_blueprint(resenias)
app.register_blueprint(servicios_extra)
app.register_blueprint(reportes)
app.register_blueprint(auth)
app.register_blueprint(usuarios)

if __name__ == '__main__':
    app.run(debug=True, port=5000)