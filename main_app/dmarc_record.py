# dmarc_record.py
#!/usr/bin/env python3
# coding: utf-8

import dns.resolver
from typing import Optional

def fetch_dmarc_record(domain: str) -> Optional[str]:
    name = f"_dmarc.{domain}"
    try:
        answers = dns.resolver.resolve(name, 'TXT')
    except Exception:
        return None

    for rdata in answers:
        txt = ''.join(part.decode() for part in rdata.strings)
        if txt.lower().startswith('v=dmarc1'):
            return txt
    return None

def parse_dmarc_strong(dmarc_text: str) -> bool:
    lower = dmarc_text.lower()
    if 'p=reject' in lower or 'p=quarantine' in lower:
        return True
    return False

def is_dmarc_record_strong(domain: str) -> bool:
    dmarc = fetch_dmarc_record(domain)
    if not dmarc:
        return False
    return parse_dmarc_strong(dmarc)
