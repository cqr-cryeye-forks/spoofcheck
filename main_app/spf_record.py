# spf_record.py
#!/usr/bin/env python3
# coding: utf-8

import dns.resolver
from typing import Optional

def fetch_spf_record(domain: str) -> Optional[str]:
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
    except Exception:
        return None

    for rdata in answers:
        txt = ''.join(part.decode() for part in rdata.strings)
        if txt.lower().startswith('v=spf1'):
            return txt
    return None

def parse_spf_strong(spf_text: str) -> bool:
    lower = spf_text.lower()
    if '-all' in lower:
        return True
    if 'redirect=' in lower:
        return True
    return False

def is_spf_record_strong(domain: str) -> bool:
    spf = fetch_spf_record(domain)
    if not spf:
        return False
    return parse_spf_strong(spf)
