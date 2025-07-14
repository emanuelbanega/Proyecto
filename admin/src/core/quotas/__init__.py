import json
from datetime import date, datetime
from dateutils import relativedelta

from src.core.quotas.quotaV2 import Quota, QuotaJson, get_detail_quota, create_Quota
from src.core import associates
from src.core.sports import delete_singup


def list_Quotas_Paged(associated_id, current_page, items):
    """Trae todos las cuotas de un asociado de la BD paginado, items es la cantidad de elementos a mostrar, current_page la pagina que devuelve"""
    return (
        Quota.query.filter_by(associated_id=associated_id)
        .order_by(Quota.id)
        .paginate(page=current_page, per_page=items, error_out=True)
    )


def list_Quotas_associatedID_by_range_date(
    associated_id: int, first_date: date, last_date: date
):
    """Trae todos las cuotas de un asociado segun el rango de fecha"""
    return (
        Quota.query.filter(Quota.end_date.between(first_date, last_date))
        .filter_by(associated_id=associated_id)
        .all()
    )


def find_quota_by_state(id_associated, state, current_page, items):
    """Trae de la BD las cuotas del asocciado paginados segun su estado. Current_page es la pagina actual, items los elementos a mostrar"""
    return (
        Quota.query.filter_by(associated_id=id_associated, state=state)
        .order_by(Quota.id)
        .paginate(page=current_page, per_page=items, error_out=True)
    )


def find_quota_by_id(id_quota):
    """Trae de la BD la cuota por su id"""
    return Quota.query.filter_by(id=id_quota).first()


def detail_quota(id_quota):
    """retorna los datos de las disciplinas de una cuota"""
    return get_detail_quota(id_quota)


def find_quota_by_idAssociated_and_endDate(associated_id, end_date):
    """retorna una cuota de un asociado segun su fecha de vencimiento"""
    return Quota.query.filter_by(associated_id=associated_id, end_date=end_date).first()


def there_is_a_quota(associated_id, end_date):
    """retorna si existe o no una cuota de un asociado para una fecha de vencimiento"""
    return find_quota_by_idAssociated_and_endDate(associated_id, end_date) is not None


def remove_sports_from_defaulter(associated):
    """Si el asociado es moroso le retira las suscripciones a disciplinas y lo pone como 'no-activo'"""
    if associates.is_defaulter(associated.id):
        for sport in associated.sports:
            delete_singup(sport, associated)
        associates.change_status_associated(associated)
    return True


def quota_generate(listAssociates):
    year = date.today().year
    if date.today().month + 1 < 13:
        month = date.today().month + 1
    else:
        month = 1
        year += 1
    end_date = datetime(year, month, 10, 23, 59, 59, 00000)
    missingAssociates = []
    for associated in listAssociates:
        if not there_is_a_quota(associated.id, end_date):
            missingAssociates.append(associated)
    for associated in missingAssociates:
        create_Quota(
            dataJSON=json.dumps(QuotaJson.fromObject(associated)),
            end_date=end_date,
            associates=associated,
        )
        remove_sports_from_defaulter(associated)
    return True


def list_year_quotas(year):
    """Retorna todas las cuotasa emitidas en el año indicado."""
    base_date = datetime(int(year), 1, 1)

    # La fecha maxima se crera de esta forma para que sea al final del ultimo
    # dia en lugar del principio.
    max_date = datetime(int(year) + 1, 1, 1)
    max_date = max_date - relativedelta(seconds=1)

    # Agrego 10 dias para usar los vencimientos de las cuotas como referencia.
    # Asi si empezamos a almacenar fechas de creacion para las cuotas a futuro
    # es mas facil de cambiar, solo hay que comentar/quitar estas dos linas.
    base_date = base_date + relativedelta(days=10)
    max_date = max_date + relativedelta(days=10)

    quotas = Quota.query.filter(base_date <= Quota.end_date, Quota.end_date <= max_date)

    return quotas
