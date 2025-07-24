#!/usr/bin/env python3
# coding: utf-8
import argparse
import json
import pathlib
from typing import Final

from main_app.dmarc_record import is_dmarc_record_strong
from main_app.spf_record import is_spf_record_strong
from main_app.spoofing_utils import evaluate_spoofable


def main():
    parser = argparse.ArgumentParser(
        description="Check if a domain is vulnerable to email spoofing by evaluating SPF and DMARC policies."
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Domain to check (e.g., example.com)"
    )
    parser.add_argument(
        "--output",
        help="Path to JSON file for saving the result (optional)"
    )
    args = parser.parse_args()

    domain = args.target

    MAIN_DIR: Final[pathlib.Path] = pathlib.Path(__file__).resolve().parents[0]
    output_file = MAIN_DIR / args.output

    spf_ok = is_spf_record_strong(domain)
    dmarc_ok = is_dmarc_record_strong(domain)
    spoofable = evaluate_spoofable(domain)

    result = {
        "target": domain,
        "spf_strong": spf_ok,
        "dmarc_strong": dmarc_ok,
        "spoofable": spoofable
    }

    with output_file.open("w") as jf:
        json.dump(result, jf, indent=2)


if __name__ == "__main__":
    main()
