from openfisca_us.model_api import *


class md_aged_dependent_exemption(Variable):
    value_type = float
    entity = TaxUnit
    label = "MD aged dependent exemption"
    unit = USD
    definition_period = YEAR
    reference = "https://govt.westlaw.com/mdc/Document/NF59A76006EA511E8ABBEE50DE853DFF4?viewType=FullText&originationContext=documenttoc&transitionType=CategoryPageItem&contextData=(sc.Default)"

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.states.md.tax.income.exemptions.aged
        age_for_exemption = p.age

        # These apply to dependents over the age of 65
        person = tax_unit.members
        dependent = person("is_tax_unit_dependent", period)
        age = person("age", period)
        elderly = age >= age_for_exemption
        aged_dependents = tax_unit.sum(dependent & elderly)
        aged_dependent_exemption = aged_dependents * p.aged_dependent

        return aged_dependent_exemption
