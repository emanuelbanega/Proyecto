from datetime import date


def array_last_months():
    """Retorna 2 arreglos, uno con los ultimos 12 meses (el ultimo mes es el actual) y otro con las posiciones de los meses en el arreglo"""
    arrMonth = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ]
    Current_month = date.today().month
    Current_year = date.today().year

    posMonth = [0 for i in range(12)]
    pos = 0
    newArrMonth = []

    # agrego primero los ultimos meses del año anterior
    for m in range(Current_month, 12):
        posMonth[m] = pos
        newArrMonth.append(arrMonth[m] + " " + str(Current_year - 1)[-2:])
        pos += 1
    # luego los de este año
    for m in range(0, Current_month):
        posMonth[m] = pos
        newArrMonth.append(arrMonth[m])
        pos += 1

    return newArrMonth, posMonth
