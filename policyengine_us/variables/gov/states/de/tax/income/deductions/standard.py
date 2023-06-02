from policyengine_us.model_api import *
import numpy as np


class de_standard_deduction(Variable):
    value_type = float
    entity = TaxUnit
    label = "Delaware standard deduction"
    unit = USD
    definition_period = YEAR
    reference = "https://revenuefiles.delaware.gov/2022/PIT-RES_TY22_2022-02_Instructions.pdf"
    defined_for = StateCode.DE

    def formula(tax_unit, period, parameters):
        filing_status = tax_unit("filing_status", period)
        p = parameters(period).gov.states.de.tax.income.deductions
        return p.standard[filing_status]
