from bisect import bisect
from collections import namedtuple

from status import Status

from . import params


def get_variable_pay(base_pay, total_pay):  # variable = total - base
    VariablePay = namedtuple("VariablePay", ["dni", "name", "pay"])
    variable_pay = {}
    for dni in base_pay:
        pay = total_pay[dni].pay - base_pay[dni].pay
        name = base_pay[dni].name
        variable_pay[dni] = VariablePay(dni, name, pay)
    return variable_pay


def get_taxes(_, total_pay, base_pay, variable_pay):  # get taxes from brackets
    Taxes = namedtuple(
        "Taxes",
        ["dni", "name", "pay", "base", "variable", "projection", "taxable", "tax"],
    )
    taxes = {}
    for dni in total_pay:
        flag = True
        try:
            pay = total_pay[dni].pay
            base = base_pay[dni].pay
            variable = variable_pay[dni].pay
            name = total_pay[dni].name
        except KeyError:
            _.warning(f"ALERTA: No esta presente algún dato para el DNI {dni}")
            _.status = Status.WARNING
            flag = False
        if flag and pay > 2500:
            base_projection = pay * 12
            # Add gratification of 2 months + 9%
            grat_projection = pay * 2
            projection = base_projection + grat_projection + (grat_projection * 0.09)
            taxable = projection - (7 * params.UIT)
            total_tax = tax(taxable) / 12  # For given month
            taxes[dni] = Taxes(
                dni, name, pay, base, variable, projection, taxable, total_tax
            )
    return taxes


def tax(income):

    rates = [8, 14, 17, 20, 30]  # 10%  20%  30%

    brackets = [22000, 88000, 154000, 198000]  # first 22,000  # next  66,000

    base_tax = [1760, 11000, 22220, 31020]  # Base tax for bracket
    i = bisect(brackets, income)
    if not i:
        return (income * rates[0]) / 100
    rate = rates[i]
    bracket = brackets[i - 1]
    income_in_bracket = income - bracket
    tax_in_bracket = income_in_bracket * rate / 100
    total_tax = base_tax[i - 1] + tax_in_bracket
    return total_tax


def format_taxes(taxes):  # Format for write function
    header = [
        "DNI",
        "Nombre y Apellido",
        "Ingresos",
        "Ingresos Fijos",
        "Ingresos Variables",
        "Proyección Ingresos",
        "Ingreso Afecto",
        "Impuesto (Mensual)",
    ]
    formatted = []
    for dni in taxes:
        t = taxes[dni]
        line = [
            dni,
            t.name,
            round(t.pay, 2),
            round(t.base, 2),
            round(t.variable, 2),
            round(t.projection, 2),
            round(t.taxable, 2),
            round(t.tax, 2),
        ]
        formatted.append(line)

    return header, formatted


if __name__ == "__main__":
    pass
    # get_variable_pay()
