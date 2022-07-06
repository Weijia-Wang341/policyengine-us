from openfisca_us.model_api import *


class wa_working_families_tax_credit(Variable):
    value_type = float
    entity = TaxUnit
    label = "Washington Working Families Tax Credit"
    unit = USD
    definition_period = YEAR
    reference = "https://app.leg.wa.gov/RCW/default.aspx?cite=82.08.0206"

    def formula(tax_unit, period, parameters):
        # Filers must claim EITC and be in Washington to be eligible.
        # TODO: Include ITIN children.
        in_wa = tax_unit.household("state_code_str", period) == "WA"
        claims_eitc = tax_unit("eitc", period) > 0
        eligible = in_wa & claims_eitc
        # Parameters are based on EITC-eligible children.
        p = parameters(
            period
        ).gov.states.wa.tax.income.credits.working_families_tax_credit
        eitc_child_count = tax_unit("eitc_child_count", period)
        max_amount = p.amount.calc(eitc_child_count)
        # WFTC phases out at a certain amount below the EITC maximum AGI.
        # NB: The Revised Code of Washington is ambiguous:
        # "below the federal phase-out income"
        # The legislative analysis clarifies that this refers to "federal maximum AGI"
        # https://lawfilesext.leg.wa.gov/biennium/2021-22/Pdf/Bill%20Reports/House/1297-S.E%20HBR%20FBR%2021.pdf?q=20220706071752
        # TODO: Use max AGI instead of phase-out start.
        eitc_phase_out_start = tax_unit("eitc_phase_out_start", period)
        phase_out_start_reduction = p.phase_out.start_below_eitc.calc(
            eitc_child_count
        )
        phase_out_start = eitc_phase_out_start - phase_out_start_reduction
        phase_out_rate = p.phase_out.rate.calc(eitc_child_count)
        earnings = tax_unit("filer_earned", period)
        excess = max_(0, earnings - phase_out_start)
        reduction = max_(0, excess * phase_out_rate)
        phased_out_amount = max_amount - reduction
        # Minimum benefit applies if calculated amount exceeds zero.
        amount_if_eligible = where(
            phased_out_amount > 0, max_(p.min_amount, phased_out_amount), 0
        )
        return amount_if_eligible * eligible
