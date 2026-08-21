#!/usr/bin/env python3
"""
zatca_qr_tlv.py — Build the Base64 TLV-encoded QR payload ZATCA requires on
every Simplified Tax Invoice (Phase 1: 5 tags, Phase 2: 9 tags).

This script handles the TLV/Base64 ENCODING correctly — it does not perform
the actual ECDSA signing needed for Phase 2 tags 7-9. Those values (the
cryptographic stamp, the seller's public key, and the certificate signature)
must come from your CSID (Cryptographic Stamp Identity) issued through
FATOORA portal onboarding. Signing invoices is a security-sensitive
operation that belongs in a properly reviewed signing service, not copied
from a script docstring — this tool just gets the wire format right once you
have those values.

TLV format: for each tag, one byte for the tag number, one byte for the
UTF-8 byte-length of the value, then the value's raw bytes. All tags are
concatenated in order, then the whole thing is Base64-encoded — that
Base64 string is what gets embedded in the QR code.

Tag reference (see references/phase1-generation.md and
references/phase2-integration.md for the full explanation of each):

  1. Seller name
  2. Seller VAT registration number
  3. Invoice timestamp (ISO 8601, e.g. 2026-08-21T14:30:00Z)
  4. Invoice total (with VAT), as a decimal string, e.g. "115.00"
  5. VAT total, as a decimal string, e.g. "15.00"
  --- Phase 2 only, appended after the above ---
  6. Invoice XML hash (Base64-encoded SHA-256 digest of the invoice XML)
  7. ECDSA signature of the invoice hash (the "cryptographic stamp"), Base64
  8. Seller's ECDSA public key, Base64 (DER-encoded)
  9. ECDSA signature of the public key by ZATCA's CA ("certificate signature"), Base64

Usage:
  # Phase 1 (5-tag) payload
  python3 zatca_qr_tlv.py \\
      --seller-name "Example Trading Co." \\
      --vat-number "300000000000003" \\
      --timestamp "2026-08-21T14:30:00Z" \\
      --total "115.00" \\
      --vat-amount "15.00"

  # Phase 2 (9-tag) payload — pass the extra four values once you have them
  # from your CSID-signed invoice
  python3 zatca_qr_tlv.py \\
      --seller-name "Example Trading Co." \\
      --vat-number "300000000000003" \\
      --timestamp "2026-08-21T14:30:00Z" \\
      --total "115.00" \\
      --vat-amount "15.00" \\
      --invoice-hash "<base64>" \\
      --signature "<base64>" \\
      --public-key "<base64>" \\
      --cert-signature "<base64>"

Add --qr-image out.png to also render a scannable PNG (requires the
`qrcode` package: pip install qrcode[pil] --break-system-packages).
"""

import argparse
import base64
import sys


def tlv_encode(tag: int, value: bytes) -> bytes:
    """Encode a single ZATCA TLV field: 1-byte tag, 1-byte length, value bytes."""
    if not (0 <= tag <= 255):
        raise ValueError(f"Tag {tag} out of range for a single byte")
    if len(value) > 255:
        raise ValueError(
            f"Value for tag {tag} is {len(value)} bytes — TLV length field is "
            "a single byte (max 255). Truncate or split the field."
        )
    return bytes([tag]) + bytes([len(value)]) + value


def build_tlv_payload(fields: "list[tuple[int, str | bytes]]") -> str:
    """Build the full Base64 TLV payload from an ordered list of (tag, value) pairs.

    String values are UTF-8 encoded; bytes values (e.g. a hash you've already
    decoded) are used as-is.
    """
    out = b""
    for tag, value in fields:
        value_bytes = value.encode("utf-8") if isinstance(value, str) else value
        out += tlv_encode(tag, value_bytes)
    return base64.b64encode(out).decode("ascii")


def build_phase1_qr(seller_name: str, vat_number: str, timestamp: str,
                     total: str, vat_amount: str) -> str:
    return build_tlv_payload([
        (1, seller_name),
        (2, vat_number),
        (3, timestamp),
        (4, total),
        (5, vat_amount),
    ])


def build_phase2_qr(seller_name: str, vat_number: str, timestamp: str,
                     total: str, vat_amount: str, invoice_hash_b64: str,
                     signature_b64: str, public_key_b64: str,
                     cert_signature_b64: str) -> str:
    return build_tlv_payload([
        (1, seller_name),
        (2, vat_number),
        (3, timestamp),
        (4, total),
        (5, vat_amount),
        (6, base64.b64decode(invoice_hash_b64)),
        (7, base64.b64decode(signature_b64)),
        (8, base64.b64decode(public_key_b64)),
        (9, base64.b64decode(cert_signature_b64)),
    ])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a ZATCA-compliant Base64 TLV QR payload for a Simplified Tax Invoice.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--seller-name", required=True)
    parser.add_argument("--vat-number", required=True)
    parser.add_argument("--timestamp", required=True, help="ISO 8601, e.g. 2026-08-21T14:30:00Z")
    parser.add_argument("--total", required=True, help='Invoice total incl. VAT, e.g. "115.00"')
    parser.add_argument("--vat-amount", required=True, help='VAT amount, e.g. "15.00"')
    parser.add_argument("--invoice-hash", help="Base64 SHA-256 hash of the invoice XML (Phase 2)")
    parser.add_argument("--signature", help="Base64 ECDSA signature / cryptographic stamp (Phase 2)")
    parser.add_argument("--public-key", help="Base64 seller ECDSA public key (Phase 2)")
    parser.add_argument("--cert-signature", help="Base64 certificate signature (Phase 2)")
    parser.add_argument("--qr-image", metavar="PATH", help="Also render a PNG QR code to this path")
    args = parser.parse_args()

    phase2_fields = [args.invoice_hash, args.signature, args.public_key, args.cert_signature]
    if any(phase2_fields) and not all(phase2_fields):
        parser.error(
            "For a Phase 2 (9-tag) payload, pass all four of --invoice-hash, "
            "--signature, --public-key, and --cert-signature together. "
            "Omit all four for a Phase 1 (5-tag) payload."
        )

    if all(phase2_fields):
        payload = build_phase2_qr(
            args.seller_name, args.vat_number, args.timestamp, args.total,
            args.vat_amount, args.invoice_hash, args.signature,
            args.public_key, args.cert_signature,
        )
        mode = "Phase 2 (9-tag)"
    else:
        payload = build_phase1_qr(
            args.seller_name, args.vat_number, args.timestamp, args.total, args.vat_amount,
        )
        mode = "Phase 1 (5-tag)"

    print(f"Mode: {mode}")
    print(f"Base64 TLV payload:\n{payload}")

    if args.qr_image:
        try:
            import qrcode
        except ImportError:
            print(
                "\n[!] --qr-image requested but the 'qrcode' package isn't installed.\n"
                "    Install it with: pip install qrcode[pil] --break-system-packages",
                file=sys.stderr,
            )
            return 1
        img = qrcode.make(payload)
        img.save(args.qr_image)
        print(f"\nQR image written to {args.qr_image}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
