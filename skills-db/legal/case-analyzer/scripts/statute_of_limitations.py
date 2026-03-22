#!/usr/bin/env python3
"""
Statute of Limitations Calculator

Calculates statute of limitations deadlines for civil rights and tort claims
across all U.S. jurisdictions.

Usage:
    python statute_of_limitations.py --claim-type 1983 --state CA --injury-date 2025-01-15
    python statute_of_limitations.py --claim-type ada-title-ii --state NY --injury-date 2024-06-01

Version: 1.0.0
Last Updated: 2026-01-01
"""

import argparse
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ClaimType(Enum):
    """Legal claim types with associated SOL rules"""
    SECTION_1983 = "1983"
    ADA_TITLE_I = "ada-title-i"
    ADA_TITLE_II = "ada-title-ii"
    ADA_TITLE_III = "ada-title-iii"
    TITLE_VII = "title-vii"
    FMLA = "fmla"
    FLSA = "flsa"
    STATE_TORT = "state-tort"
    WRONGFUL_DEATH = "wrongful-death"
    MEDICAL_MALPRACTICE = "medical-malpractice"


@dataclass
class SOLResult:
    """Statute of limitations calculation result"""
    claim_type: str
    jurisdiction: str
    injury_date: datetime
    sol_period: str
    deadline: datetime
    days_remaining: int
    expired: bool
    notes: List[str]
    warnings: List[str]
    tolling_factors: List[str]


# ============================================================================
# State-Specific SOL Data (§ 1983 Personal Injury Borrowing)
# ============================================================================

STATE_PERSONAL_INJURY_SOL = {
    "AL": (2, "Alabama - 2 years"),
    "AK": (2, "Alaska - 2 years"),
    "AZ": (2, "Arizona - 2 years"),
    "AR": (3, "Arkansas - 3 years"),
    "CA": (2, "California - 2 years"),
    "CO": (2, "Colorado - 2 years (3 years if bodily injury)"),
    "CT": (2, "Connecticut - 2 years (3 years for some torts)"),
    "DE": (2, "Delaware - 2 years"),
    "FL": (4, "Florida - 4 years"),
    "GA": (2, "Georgia - 2 years"),
    "HI": (2, "Hawaii - 2 years"),
    "ID": (2, "Idaho - 2 years"),
    "IL": (2, "Illinois - 2 years"),
    "IN": (2, "Indiana - 2 years"),
    "IA": (2, "Iowa - 2 years"),
    "KS": (2, "Kansas - 2 years"),
    "KY": (1, "Kentucky - 1 year"),
    "LA": (1, "Louisiana - 1 year"),
    "ME": (6, "Maine - 6 years"),
    "MD": (3, "Maryland - 3 years"),
    "MA": (3, "Massachusetts - 3 years"),
    "MI": (3, "Michigan - 3 years"),
    "MN": (2, "Minnesota - 2 years (6 years for certain claims)"),
    "MS": (3, "Mississippi - 3 years"),
    "MO": (5, "Missouri - 5 years"),
    "MT": (3, "Montana - 3 years"),
    "NE": (4, "Nebraska - 4 years"),
    "NV": (2, "Nevada - 2 years"),
    "NH": (3, "New Hampshire - 3 years"),
    "NJ": (2, "New Jersey - 2 years"),
    "NM": (3, "New Mexico - 3 years"),
    "NY": (3, "New York - 3 years"),
    "NC": (3, "North Carolina - 3 years"),
    "ND": (6, "North Dakota - 6 years"),
    "OH": (2, "Ohio - 2 years"),
    "OK": (2, "Oklahoma - 2 years"),
    "OR": (2, "Oregon - 2 years"),
    "PA": (2, "Pennsylvania - 2 years"),
    "RI": (3, "Rhode Island - 3 years"),
    "SC": (3, "South Carolina - 3 years"),
    "SD": (3, "South Dakota - 3 years"),
    "TN": (1, "Tennessee - 1 year"),
    "TX": (2, "Texas - 2 years"),
    "UT": (4, "Utah - 4 years"),
    "VT": (3, "Vermont - 3 years"),
    "VA": (2, "Virginia - 2 years"),
    "WA": (3, "Washington - 3 years"),
    "WV": (2, "West Virginia - 2 years"),
    "WI": (3, "Wisconsin - 3 years"),
    "WY": (4, "Wyoming - 4 years"),
    "DC": (3, "Washington D.C. - 3 years"),
}


# ============================================================================
# ADA Statute of Limitations
# ============================================================================

ADA_SOL = {
    "ADA_TITLE_I": {
        "administrative": 180,  # days (EEOC charge)
        "administrative_state": 300,  # days (if state agency)
        "lawsuit": 90,  # days after EEOC right-to-sue letter
        "notes": [
            "Must file EEOC charge within 180 days (or 300 days if state FEPA)",
            "After EEOC right-to-sue letter, 90 days to file lawsuit",
            "Failure to file EEOC charge bars lawsuit"
        ]
    },
    "ADA_TITLE_II": {
        "default_years": 2,
        "notes": [
            "Borrows state statute of limitations for personal injury",
            "Typically 2-4 years depending on state",
            "No administrative exhaustion required"
        ]
    },
    "ADA_TITLE_III": {
        "default_years": 2,
        "notes": [
            "No specific federal statute of limitations",
            "Courts typically apply state personal injury SOL",
            "2-4 years depending on jurisdiction"
        ]
    }
}


# ============================================================================
# Other Federal Claims
# ============================================================================

FEDERAL_CLAIMS_SOL = {
    "TITLE_VII": {
        "administrative": 180,  # EEOC charge
        "administrative_state": 300,  # If state FEPA
        "lawsuit": 90,  # After right-to-sue
        "notes": [
            "Must file EEOC charge within 180/300 days",
            "90 days after right-to-sue letter to file lawsuit"
        ]
    },
    "FMLA": {
        "default_years": 2,
        "willful_years": 3,
        "notes": [
            "2 years for standard violations",
            "3 years for willful violations",
            "No administrative exhaustion"
        ]
    },
    "FLSA": {
        "default_years": 2,
        "willful_years": 3,
        "notes": [
            "2 years for wage violations",
            "3 years for willful violations",
            "Liquidated damages available"
        ]
    }
}


# ============================================================================
# State Tort Claims (Wrongful Death, Medical Malpractice)
# ============================================================================

WRONGFUL_DEATH_SOL = {
    "AL": (2, "2 years from death"),
    "AK": (2, "2 years from death"),
    "AZ": (2, "2 years from death"),
    "AR": (3, "3 years from death"),
    "CA": (2, "2 years from death"),
    "CO": (2, "2 years from death"),
    "CT": (2, "2 years from death"),
    "DE": (2, "2 years from death"),
    "FL": (2, "2 years from death"),
    "GA": (2, "2 years from death"),
    "HI": (2, "2 years from death"),
    "ID": (2, "2 years from death"),
    "IL": (2, "2 years from death"),
    "IN": (2, "2 years from death"),
    "IA": (2, "2 years from death"),
    "KS": (2, "2 years from death"),
    "KY": (1, "1 year from death"),
    "LA": (1, "1 year from death"),
    "ME": (2, "2 years from death"),
    "MD": (3, "3 years from death"),
    "MA": (3, "3 years from death"),
    "MI": (3, "3 years from death"),
    "MN": (3, "3 years from death"),
    "MS": (3, "3 years from death"),
    "MO": (3, "3 years from death"),
    "MT": (3, "3 years from death"),
    "NE": (2, "2 years from death"),
    "NV": (2, "2 years from death"),
    "NH": (3, "3 years from death"),
    "NJ": (2, "2 years from death"),
    "NM": (3, "3 years from death"),
    "NY": (2, "2 years from death"),
    "NC": (2, "2 years from death"),
    "ND": (2, "2 years from death"),
    "OH": (2, "2 years from death"),
    "OK": (2, "2 years from death"),
    "OR": (3, "3 years from death"),
    "PA": (2, "2 years from death"),
    "RI": (3, "3 years from death"),
    "SC": (3, "3 years from death"),
    "SD": (3, "3 years from death"),
    "TN": (1, "1 year from death"),
    "TX": (2, "2 years from death"),
    "UT": (2, "2 years from death"),
    "VT": (2, "2 years from death"),
    "VA": (2, "2 years from death"),
    "WA": (3, "3 years from death"),
    "WV": (2, "2 years from death"),
    "WI": (3, "3 years from death"),
    "WY": (2, "2 years from death"),
    "DC": (2, "2 years from death"),
}


# ============================================================================
# Calculator Functions
# ============================================================================

def calculate_section_1983(state: str, injury_date: datetime) -> SOLResult:
    """
    Calculate § 1983 statute of limitations

    § 1983 borrows the state's personal injury statute of limitations
    """
    if state not in STATE_PERSONAL_INJURY_SOL:
        raise ValueError(f"Unknown state: {state}")

    years, description = STATE_PERSONAL_INJURY_SOL[state]
    deadline = injury_date + timedelta(days=years * 365)
    days_remaining = (deadline - datetime.now()).days

    notes = [
        "§ 1983 borrows state personal injury statute of limitations",
        description,
        "Accrues when plaintiff knows (or should know) of injury",
        "Tolling may apply for minors or mental incompetency"
    ]

    warnings = []
    if days_remaining < 90:
        warnings.append("⚠️ URGENT: Less than 90 days remaining!")
    elif days_remaining < 180:
        warnings.append("⚠️ WARNING: Less than 180 days remaining")

    tolling_factors = [
        "Plaintiff was minor at time of injury",
        "Plaintiff was mentally incompetent",
        "Defendant fraudulently concealed claim",
        "Continuing violation doctrine may apply"
    ]

    return SOLResult(
        claim_type="42 U.S.C. § 1983",
        jurisdiction=state,
        injury_date=injury_date,
        sol_period=f"{years} years",
        deadline=deadline,
        days_remaining=days_remaining,
        expired=days_remaining < 0,
        notes=notes,
        warnings=warnings,
        tolling_factors=tolling_factors
    )


def calculate_ada_title_i(state: str, injury_date: datetime, eeoc_filed: bool = False,
                          eeoc_rts_date: Optional[datetime] = None) -> SOLResult:
    """
    Calculate ADA Title I (employment) statute of limitations

    Requires EEOC charge within 180/300 days, then 90 days after right-to-sue
    """
    notes = []
    warnings = []

    # Has state FEPA (Fair Employment Practices Agency)?
    state_fepa_states = ["CA", "NY", "IL", "TX", "FL", "PA", "OH", "MI", "WA", "MA",
                         "NJ", "MD", "VA", "WI", "MN", "CO", "AZ", "OR", "CT", "NV",
                         "NM", "HI", "RI", "VT", "DE", "ME", "NH", "AK", "DC"]

    has_fepa = state in state_fepa_states
    admin_days = 300 if has_fepa else 180

    if not eeoc_filed:
        # Calculate EEOC filing deadline
        deadline = injury_date + timedelta(days=admin_days)
        days_remaining = (deadline - datetime.now()).days

        notes.append(f"Must file EEOC charge within {admin_days} days of adverse action")
        if has_fepa:
            notes.append(f"{state} has state FEPA - 300 day deadline applies")
        else:
            notes.append(f"{state} does not have state FEPA - 180 day deadline applies")
        notes.append("After EEOC investigation, will receive right-to-sue letter")
        notes.append("Then 90 days to file lawsuit from right-to-sue letter")

        if days_remaining < 30:
            warnings.append("🚨 CRITICAL: File EEOC charge immediately!")
        elif days_remaining < 60:
            warnings.append("⚠️ URGENT: EEOC charge deadline approaching")

        return SOLResult(
            claim_type="ADA Title I (Employment)",
            jurisdiction=state,
            injury_date=injury_date,
            sol_period=f"{admin_days} days (EEOC charge)",
            deadline=deadline,
            days_remaining=days_remaining,
            expired=days_remaining < 0,
            notes=notes,
            warnings=warnings,
            tolling_factors=["Continuing violation doctrine may extend deadline"]
        )
    else:
        # EEOC filed, calculate lawsuit deadline
        if not eeoc_rts_date:
            notes.append("EEOC charge filed - awaiting right-to-sue letter")
            notes.append("After receiving right-to-sue letter, you have 90 days to file lawsuit")
            return SOLResult(
                claim_type="ADA Title I (Employment)",
                jurisdiction=state,
                injury_date=injury_date,
                sol_period="Awaiting right-to-sue letter",
                deadline=None,
                days_remaining=0,
                expired=False,
                notes=notes,
                warnings=[],
                tolling_factors=[]
            )
        else:
            deadline = eeoc_rts_date + timedelta(days=90)
            days_remaining = (deadline - datetime.now()).days

            notes.append("Right-to-sue letter received")
            notes.append("90 days from right-to-sue letter to file lawsuit")

            if days_remaining < 14:
                warnings.append("🚨 CRITICAL: File lawsuit immediately!")
            elif days_remaining < 30:
                warnings.append("⚠️ URGENT: Lawsuit deadline approaching")

            return SOLResult(
                claim_type="ADA Title I (Employment)",
                jurisdiction=state,
                injury_date=injury_date,
                sol_period="90 days from right-to-sue",
                deadline=deadline,
                days_remaining=days_remaining,
                expired=days_remaining < 0,
                notes=notes,
                warnings=warnings,
                tolling_factors=[]
            )


def calculate_ada_title_ii(state: str, injury_date: datetime) -> SOLResult:
    """
    Calculate ADA Title II (state/local government) statute of limitations

    Borrows state personal injury SOL, typically 2-4 years
    """
    if state not in STATE_PERSONAL_INJURY_SOL:
        raise ValueError(f"Unknown state: {state}")

    years, description = STATE_PERSONAL_INJURY_SOL[state]
    deadline = injury_date + timedelta(days=years * 365)
    days_remaining = (deadline - datetime.now()).days

    notes = [
        "ADA Title II borrows state personal injury statute of limitations",
        description,
        "No administrative exhaustion required (unlike Title I)",
        "Can sue directly in federal court"
    ]

    warnings = []
    if days_remaining < 90:
        warnings.append("⚠️ URGENT: Less than 90 days remaining!")
    elif days_remaining < 180:
        warnings.append("⚠️ WARNING: Less than 180 days remaining")

    tolling_factors = [
        "Plaintiff was minor at time of injury",
        "Plaintiff was mentally incompetent",
        "Equitable tolling for extraordinary circumstances"
    ]

    return SOLResult(
        claim_type="ADA Title II (State/Local Government)",
        jurisdiction=state,
        injury_date=injury_date,
        sol_period=f"{years} years",
        deadline=deadline,
        days_remaining=days_remaining,
        expired=days_remaining < 0,
        notes=notes,
        warnings=warnings,
        tolling_factors=tolling_factors
    )


def calculate_wrongful_death(state: str, death_date: datetime) -> SOLResult:
    """
    Calculate wrongful death statute of limitations

    Accrues from date of death (not injury)
    """
    if state not in WRONGFUL_DEATH_SOL:
        raise ValueError(f"Unknown state: {state}")

    years, description = WRONGFUL_DEATH_SOL[state]
    deadline = death_date + timedelta(days=years * 365)
    days_remaining = (deadline - datetime.now()).days

    notes = [
        "Wrongful death accrues from DATE OF DEATH (not date of injury)",
        description,
        "Survival action may have different SOL (from date of injury)",
        "Can plead both wrongful death and survival action"
    ]

    warnings = []
    if days_remaining < 90:
        warnings.append("⚠️ URGENT: Less than 90 days remaining!")
    elif days_remaining < 180:
        warnings.append("⚠️ WARNING: Less than 180 days remaining")

    tolling_factors = [
        "Beneficiaries were minors at time of death",
        "Discovery rule generally does NOT apply (death is obvious event)"
    ]

    return SOLResult(
        claim_type="Wrongful Death",
        jurisdiction=state,
        injury_date=death_date,
        sol_period=f"{years} years from death",
        deadline=deadline,
        days_remaining=days_remaining,
        expired=days_remaining < 0,
        notes=notes,
        warnings=warnings,
        tolling_factors=tolling_factors
    )


# ============================================================================
# Display Functions
# ============================================================================

def format_result(result: SOLResult) -> str:
    """Format SOL result for display"""
    output = []
    output.append("=" * 80)
    output.append(f"STATUTE OF LIMITATIONS ANALYSIS")
    output.append("=" * 80)
    output.append(f"\nClaim Type: {result.claim_type}")
    output.append(f"Jurisdiction: {result.jurisdiction}")
    output.append(f"Injury/Event Date: {result.injury_date.strftime('%Y-%m-%d')}")
    output.append(f"SOL Period: {result.sol_period}")

    if result.deadline:
        output.append(f"\n{'FILING DEADLINE:':<20} {result.deadline.strftime('%Y-%m-%d %A')}")
        output.append(f"{'Days Remaining:':<20} {result.days_remaining} days")

        if result.expired:
            output.append(f"\n{'STATUS:':<20} 🚨 EXPIRED - Claim likely time-barred")
        elif result.days_remaining < 30:
            output.append(f"\n{'STATUS:':<20} 🚨 CRITICAL - File immediately!")
        elif result.days_remaining < 90:
            output.append(f"\n{'STATUS:':<20} ⚠️ URGENT - Deadline approaching")
        elif result.days_remaining < 180:
            output.append(f"\n{'STATUS:':<20} ⚠️ WARNING - Less than 6 months")
        else:
            output.append(f"\n{'STATUS:':<20} ✓ Active - {result.days_remaining} days remaining")

    if result.warnings:
        output.append(f"\nWARNINGS:")
        for warning in result.warnings:
            output.append(f"  {warning}")

    if result.notes:
        output.append(f"\nNOTES:")
        for note in result.notes:
            output.append(f"  • {note}")

    if result.tolling_factors:
        output.append(f"\nPOTENTIAL TOLLING FACTORS:")
        for factor in result.tolling_factors:
            output.append(f"  • {factor}")

    output.append("\n" + "=" * 80)
    output.append("⚠️  DISCLAIMER: This is a general calculation. Consult controlling law in")
    output.append("   your jurisdiction. Exceptions and tolling may apply.")
    output.append("=" * 80)

    return "\n".join(output)


# ============================================================================
# Main Function
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Calculate statute of limitations deadlines for civil rights and tort claims",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # § 1983 excessive force (California)
  python statute_of_limitations.py --claim-type 1983 --state CA --injury-date 2025-01-15

  # ADA Title II (New York)
  python statute_of_limitations.py --claim-type ada-title-ii --state NY --injury-date 2024-06-01

  # Wrongful death (Texas)
  python statute_of_limitations.py --claim-type wrongful-death --state TX --death-date 2025-03-10

  # ADA Title I with EEOC filed
  python statute_of_limitations.py --claim-type ada-title-i --state CA --injury-date 2025-01-15 \\
      --eeoc-filed --eeoc-rts-date 2025-11-01
        """
    )

    parser.add_argument(
        "--claim-type",
        required=True,
        choices=["1983", "ada-title-i", "ada-title-ii", "wrongful-death", "state-tort"],
        help="Type of legal claim"
    )

    parser.add_argument(
        "--state",
        required=True,
        help="Two-letter state code (e.g., CA, NY, TX)"
    )

    parser.add_argument(
        "--injury-date",
        type=str,
        help="Date of injury or discriminatory act (YYYY-MM-DD)"
    )

    parser.add_argument(
        "--death-date",
        type=str,
        help="Date of death (for wrongful death claims, YYYY-MM-DD)"
    )

    parser.add_argument(
        "--eeoc-filed",
        action="store_true",
        help="EEOC charge already filed (for ADA Title I)"
    )

    parser.add_argument(
        "--eeoc-rts-date",
        type=str,
        help="Date of EEOC right-to-sue letter (YYYY-MM-DD)"
    )

    args = parser.parse_args()

    # Validate state code
    state_upper = args.state.upper()
    if state_upper not in STATE_PERSONAL_INJURY_SOL:
        print(f"Error: Unknown state code '{args.state}'", file=sys.stderr)
        print(f"Valid codes: {', '.join(sorted(STATE_PERSONAL_INJURY_SOL.keys()))}", file=sys.stderr)
        sys.exit(1)

    # Parse dates
    try:
        if args.claim_type == "wrongful-death":
            if not args.death_date:
                print("Error: --death-date required for wrongful death claims", file=sys.stderr)
                sys.exit(1)
            event_date = datetime.strptime(args.death_date, "%Y-%m-%d")
        else:
            if not args.injury_date:
                print("Error: --injury-date required", file=sys.stderr)
                sys.exit(1)
            event_date = datetime.strptime(args.injury_date, "%Y-%m-%d")

        eeoc_rts_date = None
        if args.eeoc_rts_date:
            eeoc_rts_date = datetime.strptime(args.eeoc_rts_date, "%Y-%m-%d")

    except ValueError as e:
        print(f"Error parsing date: {e}", file=sys.stderr)
        print("Use format: YYYY-MM-DD (e.g., 2025-01-15)", file=sys.stderr)
        sys.exit(1)

    # Calculate SOL
    try:
        if args.claim_type == "1983":
            result = calculate_section_1983(state_upper, event_date)
        elif args.claim_type == "ada-title-i":
            result = calculate_ada_title_i(state_upper, event_date, args.eeoc_filed, eeoc_rts_date)
        elif args.claim_type == "ada-title-ii":
            result = calculate_ada_title_ii(state_upper, event_date)
        elif args.claim_type == "wrongful-death":
            result = calculate_wrongful_death(state_upper, event_date)
        elif args.claim_type == "state-tort":
            result = calculate_section_1983(state_upper, event_date)  # Same as § 1983 (borrows state SOL)
        else:
            print(f"Error: Unsupported claim type '{args.claim_type}'", file=sys.stderr)
            sys.exit(1)

        # Display result
        print(format_result(result))

        # Exit with status code
        if result.expired:
            sys.exit(2)  # Expired
        elif result.days_remaining and result.days_remaining < 30:
            sys.exit(1)  # Critical
        else:
            sys.exit(0)  # OK

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
