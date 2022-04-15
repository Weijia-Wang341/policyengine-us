from openfisca_us.model_api import *


class c07180(Variable):
    value_type = float
    entity = TaxUnit
    definition_period = YEAR
    label = "Child/dependent care credit"
    unit = USD
    documentation = "Nonrefundable credit for child and dependent care expenses from Form 2441"

    def formula(tax_unit, period, parameters):
        cdcc = parameters(period).irs.credits.cdcc
        if cdcc.refundable or cdcc.abolition:
            return 0
        else:
            c05800 = tax_unit("c05800", period)
            e07300 = tax_unit("e07300", period)
            c33200 = tax_unit("c33200", period)
            c05800_minus_e07300_capped = max_(c05800 - e07300, 0)
            return min_(c05800_minus_e07300_capped, c33200)


cdcc = variable_alias("cdcc", c07180)
