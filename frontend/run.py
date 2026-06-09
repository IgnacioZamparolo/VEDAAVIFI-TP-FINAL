import logging
import os
from flask import Flask, render_template
#from app.routes import frontend_bp
from app.parrilla_argentina_admin.routes.auth import auth_bp
from app.parrilla_argentina_admin.routes.combos_bp import combos_bp
from app.parrilla_argentina_admin.routes.combo_version_bp import combo_version_bp
from app.parrilla_argentina_admin.routes.combo_detalle_bp import combo_detalle_bp
from app.parrilla_argentina_admin.routes.resenias_bp import resenias_bp
from app.parrilla_argentina_admin.routes.reservas_bp import reservas_bp
from app.parrilla_argentina_admin.routes.servicios_extra_bp import servicios_bp
from app.parrilla_argentina_admin.routes.productos_bp import productos_bp
from app.parrilla_argentina_admin.routes.menu_bp import menu_bp
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(name)s - %(message)s')

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)
app.json.sort_keys = False
app.secret_key = os.getenv('SECRET_KEY', 'change-me-please-frontend')

#app.register_blueprint(frontend_bp)
app.register_blueprint(auth_bp, url_prefix='/admin')
app.register_blueprint(productos_bp)
app.register_blueprint(combos_bp)
app.register_blueprint(combo_version_bp)
app.register_blueprint(combo_detalle_bp)
app.register_blueprint(resenias_bp)
app.register_blueprint(reservas_bp)
app.register_blueprint(servicios_bp)
app.register_blueprint(menu_bp)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error), 404

if __name__ == "__main__":
    app.run(debug=True, port=8080)