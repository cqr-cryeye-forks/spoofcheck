# spoofing_utils.py
#!/usr/bin/env python3
# coding: utf-8

from main_app.spf_record import is_spf_record_strong
from main_app.dmarc_record import is_dmarc_record_strong

def evaluate_spoofable(domain: str) -> bool:
    spf_ok = is_spf_record_strong(domain)
    dmarc_ok = is_dmarc_record_strong(domain)
    return not (spf_ok and dmarc_ok)
