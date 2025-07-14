from src.core.database import db
from src.core.licenses.license import License


def create_license(**kwargs):
    """agrega la configuracion de la app a la BD. recibe 'cant_elements_page', 'enable_pay_table', 'contact_info', 'voucher_title', 'price_month', 'percent_increase_debtors', 'currency_type'."""
    license = License(**kwargs)
    db.session.add(license)
    db.session.commit()
    return license

def get_license_by_id(id):
    """Busca y retorna un asociado por id."""
    carnet = License.query.get_or_404(id )
    return carnet