#!/usr/bin/env python3
"""
Blood Group Compatibility Checker - Command Line Interface

Usage:
    python -m bloodgroup_checker.cli --check-compatibility O+ A-
"""

import argparse
import json
import sys
from pathlib import Path

from bloodgroup_checker.models import BloodGroupProfile, BloodType, RhType
from bloodgroup_checker.analyzer import check_compatibility, get_universal_status
from bloodgroup_checker.database import get_blood_group_database


def create_parser():
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description="Blood Group Compatibility Checker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --check O- A+
  %(prog)s --universal O-
  %(prog)s --systems
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--check", "-c",
        nargs=2,
        metavar=("DONOR", "RECIPIENT"),
        help="Check compatibility (e.g., O- A+)"
    )
    group.add_argument(
        "--universal", "-u",
        metavar="BLOOD_TYPE",
        help="Check universal donor status (e.g., O-)"
    )
    group.add_argument(
        "--systems", "-s",
        action="store_true",
        help="List supported blood group systems"
    )

    parser.add_argument(
        "--extended", "-e",
        action="store_true",
        help="Include extended antigen checking"
    )

    return parser


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if args.check:
        donor, recipient = args.check
        d_abo = donor[:-1]
        d_rh = donor[-1]
        r_abo = recipient[:-1]
        r_rh = recipient[-1]

        result = check_compatibility(d_abo, d_rh, r_abo, r_rh, args.extended)

        print(f"\nBlood Group Compatibility Check")
        print("=" * 50)
        print(f"Donor: {donor}")
        print(f"Recipient: {recipient}")
        print(f"Compatible: {'✓ Yes' if result['compatible'] else '✗ No'}")
        print(f"Risk Level: {result['risk_level']}")
        print(f"Reason: {result['reason']}")

    elif args.universal:
        blood_type = args.universal
        bp = BloodGroupProfile(
            abo=BloodType(blood_type[:-1]),
            rh=RhType(blood_type[-1])
        )
        result = get_universal_status(bp.abo, bp.rh)

        print(f"\n{blood_type} Blood Type Status")
        print("=" * 30)
        print(f"Universal Red Cell Donor: {'✓ Yes' if result['universal_red_cell_donor'] else '✗ No'}")
        print(f"Universal Plasma Donor: {'✓ Yes' if result['universal_plasma_donor'] else '✗ No'}")

    elif args.systems:
        db = get_blood_group_database()
        systems = db.get_extended_systems()

        print("\nSupported Blood Group Systems")
        print("=" * 40)
        for sys_id, data in systems.items():
            print(f"\n{sys_id}: Antigens = {data.antigens}")


if __name__ == "__main__":
    main()