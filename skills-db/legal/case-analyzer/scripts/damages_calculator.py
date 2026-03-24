#!/usr/bin/env python3
"""
Damages Calculator for Civil Rights and Tort Cases

Estimates potential damages based on case facts, injuries, and jurisdiction.
Provides low/mid/high range estimates for settlement and trial preparation.

Usage:
    python damages_calculator.py --state CA --age 35 --medical-expenses 50000 \\
        --lost-wages 25000 --injury-severity moderate --claim-type 1983

Version: 1.0.0
Last Updated: 2026-01-01
"""

import argparse
import sys
from dataclasses import dataclass
from typing import Optional, Tuple, List
from enum import Enum


class ClaimType(Enum):
    """Legal claim types"""
    SECTION_1983 = "1983"
    ADA = "ada"
    STATE_TORT = "state-tort"
    WRONGFUL_DEATH = "wrongful-death"


class InjurySeverity(Enum):
    """Injury severity levels"""
    MINOR = "minor"              # Bruises, minor cuts, temporary pain
    MODERATE = "moderate"        # Fractures, significant pain, short-term disability
    SERIOUS = "serious"          # Permanent injury, long-term disability
    CATASTROPHIC = "catastrophic"  # Paralysis, brain injury, loss of limb
    DEATH = "death"              # Wrongful death


@dataclass
class DamagesEstimate:
    """Estimated damages range"""
    economic_low: float
    economic_mid: float
    economic_high: float
    non_economic_low: float
    non_economic_mid: float
    non_economic_high: float
    punitive_low: float
    punitive_mid: float
    punitive_high: float
    total_low: float
    total_mid: float
    total_high: float
    attorney_fees_estimate: float
    notes: List[str]
    limitations: List[str]


# State-specific non-economic damages caps
NON_ECONOMIC_CAPS = {
    "CA": ("medical_malpractice", 250000, "MICRA cap ($250K for medical malpractice only)"),
    "CO": ("non_economic", 500000, "$500K cap (adjusted for inflation)"),
    "FL": ("medical_malpractice", 500000, "$500K cap for medical malpractice"),
    "GA": ("non_economic", 350000, "$350K cap (multiple defendants: $350K per defendant)"),
    "ID": ("non_economic", 250000, "$250K cap"),
    "IL": ("medical_malpractice", 500000, "$500K cap for medical malpractice (physicians)"),
    "IN": ("medical_malpractice", 1800000, "$1.8M cap for medical malpractice"),
    "KS": ("non_economic", 300000, "$300K cap"),
    "MD": ("non_economic", 800000, "$800K cap (adjusted for inflation)"),
    "MI": ("medical_malpractice", 500000, "$500K cap for medical malpractice"),
    "MO": ("non_economic", 400000, "$400K cap for non-catastrophic injuries"),
    "MT": ("non_economic", 250000, "$250K cap"),
    "NE": ("medical_malpractice", 2250000, "$2.25M cap for medical malpractice"),
    "NM": ("medical_malpractice", 600000, "$600K cap for medical malpractice"),
    "NC": ("punitive", 3, "Punitive damages capped at 3x compensatory or $250K"),
    "OH": ("non_economic", 250000, "$250K or 3x economic damages (whichever greater)"),
    "OK": ("non_economic", 350000, "$350K cap"),
    "OR": ("non_economic", 500000, "$500K cap"),
    "SC": ("non_economic", 350000, "$350K cap"),
    "TN": ("non_economic", 750000, "$750K cap ($1M for catastrophic injury)"),
    "TX": ("non_economic", 250000, "$250K cap per defendant"),
    "UT": ("non_economic", 450000, "$450K cap"),
    "VA": ("medical_malpractice", 2300000, "$2.3M cap for medical malpractice"),
    "WV": ("non_economic", 500000, "$500K cap ($1M for wrongful death)"),
    "WI": ("non_economic", 750000, "$750K cap for medical malpractice"),
}


def calculate_economic_damages(
    medical_expenses: float,
    future_medical: float,
    lost_wages: float,
    future_lost_earnings: float,
    property_damage: float
) -> Tuple[float, float, float]:
    """
    Calculate economic damages (objectively verifiable losses)

    Returns: (low, mid, high) estimates
    """
    # Economic damages are relatively certain if documented
    total_economic = (
        medical_expenses +
        future_medical +
        lost_wages +
        future_lost_earnings +
        property_damage
    )

    # Conservative (80%), Mid (100%), Aggressive (120%)
    # Aggressive accounts for potential additional medical needs
    low = total_economic * 0.8
    mid = total_economic
    high = total_economic * 1.2

    return (low, mid, high)


def calculate_non_economic_damages(
    injury_severity: InjurySeverity,
    age: int,
    economic_damages: float,
    state: str
) -> Tuple[float, float, float, List[str]]:
    """
    Calculate non-economic damages (pain/suffering, emotional distress)

    Returns: (low, mid, high, notes)
    """
    notes = []

    # Base multipliers by injury severity
    multipliers = {
        InjurySeverity.MINOR: (0.5, 1.0, 2.0),        # 0.5x-2x economic
        InjurySeverity.MODERATE: (1.5, 2.5, 4.0),     # 1.5x-4x economic
        InjurySeverity.SERIOUS: (3.0, 5.0, 8.0),      # 3x-8x economic
        InjurySeverity.CATASTROPHIC: (5.0, 10.0, 15.0),  # 5x-15x economic
        InjurySeverity.DEATH: (3.0, 5.0, 10.0),       # Varies widely
    }

    low_mult, mid_mult, high_mult = multipliers[injury_severity]

    # Age adjustment (younger plaintiffs = higher damages for long-term suffering)
    if age < 18:
        age_factor = 1.3  # Minor - lifetime of suffering ahead
        notes.append("Minor plaintiff - increased non-economic damages")
    elif age < 40:
        age_factor = 1.2
    elif age < 60:
        age_factor = 1.0
    else:
        age_factor = 0.9

    low = economic_damages * low_mult * age_factor
    mid = economic_damages * mid_mult * age_factor
    high = economic_damages * high_mult * age_factor

    # Apply state caps if applicable
    if state.upper() in NON_ECONOMIC_CAPS:
        cap_type, cap_amount, cap_description = NON_ECONOMIC_CAPS[state.upper()]
        if cap_type in ["non_economic", "medical_malpractice"]:
            if high > cap_amount:
                notes.append(f"⚠️ {state} has {cap_description}")
                notes.append(f"High estimate capped at ${cap_amount:,.0f}")
                high = min(high, cap_amount)
                mid = min(mid, cap_amount)
                low = min(low, cap_amount)

    return (low, mid, high, notes)


def calculate_punitive_damages(
    compensatory_total: float,
    conduct_severity: str,
    state: str,
    claim_type: ClaimType
) -> Tuple[float, float, float, List[str]]:
    """
    Calculate potential punitive damages

    Punitive damages for malicious, willful, or reckless conduct
    NOT available against municipalities (§ 1983)

    Returns: (low, mid, high, notes)
    """
    notes = []

    # Punitive not available in all cases
    if claim_type == ClaimType.SECTION_1983:
        notes.append("Punitive damages available against individual officers only (not municipality)")
    elif claim_type == ClaimType.ADA:
        notes.append("⚠️ Punitive damages NOT available in ADA cases")
        return (0, 0, 0, notes)

    # Conduct severity determines likelihood and amount
    conduct_multipliers = {
        "negligent": (0, 0, 0),           # No punitives
        "reckless": (0.5, 1.0, 2.0),      # Possible
        "malicious": (1.0, 2.0, 4.0),     # Likely
        "egregious": (2.0, 4.0, 9.0),     # Very likely
    }

    if conduct_severity not in conduct_multipliers:
        conduct_severity = "reckless"  # Default

    low_mult, mid_mult, high_mult = conduct_multipliers[conduct_severity]

    low = compensatory_total * low_mult
    mid = compensatory_total * mid_mult
    high = compensatory_total * high_mult

    # Constitutional limits (BMW v. Gore, State Farm v. Campbell)
    # Single-digit ratios generally constitutional (1:1 to 9:1)
    # Ratios > 10:1 likely unconstitutional

    if high / compensatory_total > 9 and compensatory_total > 10000:
        notes.append("⚠️ Ratio exceeds 9:1 - constitutional limits may apply")
        notes.append("Consider 4:1 ratio as conservative estimate")
        high = compensatory_total * 9  # Cap at 9:1
        mid = min(mid, compensatory_total * 4)  # Conservative 4:1

    # State-specific punitive caps
    state_upper = state.upper()
    if state_upper == "CO":
        # Colorado: Punitive capped at compensatory
        notes.append("Colorado caps punitive damages at compensatory damages amount")
        high = min(high, compensatory_total)
        mid = min(mid, compensatory_total)
        low = min(low, compensatory_total)
    elif state_upper == "FL":
        # Florida: 3x compensatory or $500K
        cap = max(compensatory_total * 3, 500000)
        notes.append(f"Florida caps punitive at 3x compensatory or $500K (whichever greater)")
        high = min(high, cap)
        mid = min(mid, cap)
    elif state_upper == "GA":
        # Georgia: $250K cap (except DUI, intentional harm, financial gain)
        notes.append("Georgia has $250K cap on punitive damages")
        high = min(high, 250000)
        mid = min(mid, 250000)
        low = min(low, 250000)
    elif state_upper == "NC":
        # North Carolina: 3x compensatory or $250K (whichever greater)
        cap = max(compensatory_total * 3, 250000)
        notes.append(f"North Carolina caps punitive at 3x compensatory or $250K")
        high = min(high, cap)
        mid = min(mid, cap)
    elif state_upper == "VA":
        # Virginia: $350K cap
        notes.append("Virginia has $350K cap on punitive damages")
        high = min(high, 350000)
        mid = min(mid, 350000)
        low = min(low, 350000)

    return (low, mid, high, notes)


def calculate_attorney_fees(total_damages_mid: float, claim_type: ClaimType) -> Tuple[float, List[str]]:
    """
    Estimate attorney's fees (for fee-shifting statutes)

    § 1983, ADA, and other civil rights statutes allow prevailing party to recover attorney's fees
    """
    notes = []

    if claim_type in [ClaimType.SECTION_1983, ClaimType.ADA]:
        notes.append("Attorney's fees available under 42 U.S.C. § 1988 (§ 1983) or 42 U.S.C. § 12205 (ADA)")
        notes.append("Fees calculated using lodestar method (hours × rate)")

        # Estimate: Complex civil rights case typically 200-500 hours
        # Attorney hourly rate: $300-$500/hour
        # Conservative estimate: 300 hours × $350/hour = $105,000
        estimated_fees = 105000

        # For higher-value cases, fees may be higher (more hours, experts, etc.)
        if total_damages_mid > 500000:
            estimated_fees = 200000
            notes.append("High-value case - estimated fees higher due to complexity")
        elif total_damages_mid > 100000:
            estimated_fees = 150000

        notes.append(f"Estimated attorney's fees: ${estimated_fees:,.0f}")
        notes.append("Actual fees depend on hours worked and complexity")

        return (estimated_fees, notes)
    else:
        notes.append("⚠️ No fee-shifting statute - contingency fee typical (33-40% of recovery)")
        return (0, notes)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate estimated damages for civil rights and tort cases",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Moderate injury, § 1983 case (California)
  python damages_calculator.py --state CA --age 35 --claim-type 1983 \\
      --medical-expenses 50000 --lost-wages 25000 --injury-severity moderate \\
      --conduct-severity malicious

  # Wrongful death (Texas)
  python damages_calculator.py --state TX --age 45 --claim-type wrongful-death \\
      --medical-expenses 100000 --lost-wages 50000 --future-lost-earnings 2000000 \\
      --injury-severity death --conduct-severity egregious

  # ADA case (New York)
  python damages_calculator.py --state NY --age 50 --claim-type ada \\
      --medical-expenses 10000 --injury-severity minor
        """
    )

    parser.add_argument("--state", required=True, help="Two-letter state code")
    parser.add_argument("--age", type=int, required=True, help="Plaintiff's age")
    parser.add_argument(
        "--claim-type",
        required=True,
        choices=["1983", "ada", "state-tort", "wrongful-death"],
        help="Type of legal claim"
    )

    parser.add_argument(
        "--injury-severity",
        required=True,
        choices=["minor", "moderate", "serious", "catastrophic", "death"],
        help="Severity of injury"
    )

    parser.add_argument(
        "--conduct-severity",
        default="reckless",
        choices=["negligent", "reckless", "malicious", "egregious"],
        help="Severity of defendant's conduct (for punitive damages)"
    )

    # Economic damages
    parser.add_argument("--medical-expenses", type=float, default=0, help="Past medical expenses")
    parser.add_argument("--future-medical", type=float, default=0, help="Future medical expenses")
    parser.add_argument("--lost-wages", type=float, default=0, help="Past lost wages")
    parser.add_argument("--future-lost-earnings", type=float, default=0, help="Future lost earning capacity")
    parser.add_argument("--property-damage", type=float, default=0, help="Property damage")

    args = parser.parse_args()

    # Validate inputs
    if args.age < 0 or args.age > 120:
        print("Error: Age must be between 0 and 120", file=sys.stderr)
        sys.exit(1)

    state_upper = args.state.upper()

    # Parse enums
    injury_severity = InjurySeverity(args.injury_severity)
    claim_type = ClaimType(args.claim_type)

    # Calculate economic damages
    econ_low, econ_mid, econ_high = calculate_economic_damages(
        args.medical_expenses,
        args.future_medical,
        args.lost_wages,
        args.future_lost_earnings,
        args.property_damage
    )

    # Calculate non-economic damages
    non_econ_low, non_econ_mid, non_econ_high, non_econ_notes = calculate_non_economic_damages(
        injury_severity,
        args.age,
        econ_mid,
        state_upper
    )

    # Calculate punitive damages
    compensatory_mid = econ_mid + non_econ_mid
    pun_low, pun_mid, pun_high, pun_notes = calculate_punitive_damages(
        compensatory_mid,
        args.conduct_severity,
        state_upper,
        claim_type
    )

    # Total damages
    total_low = econ_low + non_econ_low + pun_low
    total_mid = econ_mid + non_econ_mid + pun_mid
    total_high = econ_high + non_econ_high + pun_high

    # Attorney's fees
    atty_fees, atty_notes = calculate_attorney_fees(total_mid, claim_type)

    # Compile notes
    all_notes = []
    all_notes.extend(non_econ_notes)
    all_notes.extend(pun_notes)
    all_notes.extend(atty_notes)

    limitations = [
        "⚠️ This is an ESTIMATE only - actual damages depend on evidence and jury",
        "⚠️ Consult controlling case law in your jurisdiction",
        "⚠️ Economic damages require documentation (medical records, wage statements)",
        "⚠️ Non-economic damages highly variable based on jury sympathy",
        "⚠️ Punitive damages require clear and convincing evidence of malice/recklessness"
    ]

    # Create result
    result = DamagesEstimate(
        economic_low=econ_low,
        economic_mid=econ_mid,
        economic_high=econ_high,
        non_economic_low=non_econ_low,
        non_economic_mid=non_econ_mid,
        non_economic_high=non_econ_high,
        punitive_low=pun_low,
        punitive_mid=pun_mid,
        punitive_high=pun_high,
        total_low=total_low,
        total_mid=total_mid,
        total_high=total_high,
        attorney_fees_estimate=atty_fees,
        notes=all_notes,
        limitations=limitations
    )

    # Display results
    print("=" * 80)
    print("DAMAGES ESTIMATE")
    print("=" * 80)
    print(f"\nClaim Type: {args.claim_type.upper()}")
    print(f"State: {state_upper}")
    print(f"Injury Severity: {injury_severity.value.title()}")
    print(f"Plaintiff Age: {args.age}")
    print(f"Conduct Severity: {args.conduct_severity.title()}")

    print(f"\n{'ECONOMIC DAMAGES':<30} {'Low':<15} {'Mid':<15} {'High':<15}")
    print("-" * 80)
    print(f"{'Medical Expenses':<30} ${econ_low:>13,.0f} ${econ_mid:>13,.0f} ${econ_high:>13,.0f}")

    print(f"\n{'NON-ECONOMIC DAMAGES':<30} {'Low':<15} {'Mid':<15} {'High':<15}")
    print("-" * 80)
    print(f"{'Pain & Suffering':<30} ${non_econ_low:>13,.0f} ${non_econ_mid:>13,.0f} ${non_econ_high:>13,.0f}")

    print(f"\n{'PUNITIVE DAMAGES':<30} {'Low':<15} {'Mid':<15} {'High':<15}")
    print("-" * 80)
    if pun_mid > 0:
        print(f"{'Punitive (if proven)':<30} ${pun_low:>13,.0f} ${pun_mid:>13,.0f} ${pun_high:>13,.0f}")
    else:
        print(f"{'Punitive':<30} {'Not Available':>15} {'Not Available':>15} {'Not Available':>15}")

    print(f"\n{'TOTAL DAMAGES':<30} {'Low':<15} {'Mid':<15} {'High':<15}")
    print("=" * 80)
    print(f"{'TOTAL ESTIMATE':<30} ${total_low:>13,.0f} ${total_mid:>13,.0f} ${total_high:>13,.0f}")

    if atty_fees > 0:
        print(f"\n{'Attorney\'s Fees (if prevail)':<30} ${atty_fees:>13,.0f}")

    if result.notes:
        print(f"\nNOTES:")
        for note in result.notes:
            print(f"  {note}")

    if result.limitations:
        print(f"\nDISCLAIMER / LIMITATIONS:")
        for limitation in result.limitations:
            print(f"  {limitation}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
