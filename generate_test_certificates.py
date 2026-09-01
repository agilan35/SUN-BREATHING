"""
Generate sample test certificate images for SUN BREATHING platform
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFont

# Configure safe output encoding for Windows
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


def get_fonts():
    try:
        title_font = ImageFont.truetype("arial.ttf", 44)
        header_font = ImageFont.truetype("arial.ttf", 32)
        body_font = ImageFont.truetype("arial.ttf", 24)
        small_font = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    return title_font, header_font, body_font, small_font


def create_fake_certificate():
    """Create a fake certificate that should be detected as FAKE"""
    img = Image.new('RGB', (1000, 1400), color='#ffffff')
    draw = ImageDraw.Draw(img)
    title_font, header_font, body_font, small_font = get_fonts()

    # Red/suspicious border
    border_color = (200, 20, 20)
    draw.rectangle([(20, 20), (980, 1380)], outline=border_color, width=6)
    draw.rectangle([(32, 32), (968, 1368)], outline=(100, 0, 0), width=2)

    # Title
    draw.text((500, 90), "CERTIFICATE OF ACHIEVEMENT", fill=(200, 20, 20),
              font=title_font, anchor="mm")

    y_pos = 220
    content = [
        "This is to certify that",
        "",
        "John Smith",
        "",
        "Has successfully completed",
        "",
        "Advanced Blockchain Development",
        "",
        "Issued by: Harvard University",
        "",
        "Certificate ID: CERT-FAKE-2026-9999",
        "Issue Date: 2026-08-30",
        "Verification Code: XYZ-INVALID-ABC",
    ]

    for line in content:
        draw.text((500, y_pos), line, fill=(20, 20, 20), font=body_font, anchor="mm")
        y_pos += 75

    # Visual anomalies & tampering lines
    draw.text((500, y_pos + 40), "[UNVERIFIED EXTERNAL CREDENTIAL]", fill=(220, 0, 0),
              font=small_font, anchor="mm")

    for i in range(0, 1000, 40):
        draw.line([(i, 0), (i + 40, 80)], fill=(220, 220, 220), width=1)

    filepath = os.path.join(os.path.dirname(__file__), "uploads", "fake_certificate_sample.jpg")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath, quality=80)
    print(f"[+] FAKE Certificate created: {filepath}")
    return filepath


def create_real_certificate():
    """Create a real certificate that matches database records"""
    img = Image.new('RGB', (1000, 1400), color='#FAFAFA')
    draw = ImageDraw.Draw(img)
    title_font, header_font, body_font, small_font = get_fonts()

    # Elegant gold & blue border
    draw.rectangle([(20, 20), (980, 1380)], outline=(185, 0, 21), width=6)
    draw.rectangle([(32, 32), (968, 1368)], outline=(218, 165, 32), width=3)

    # Title
    draw.text((500, 90), "CERTIFICATE OF COMPLETION", fill=(185, 0, 21),
              font=title_font, anchor="mm")

    y_pos = 220
    content = [
        "This is to officially certify that",
        "",
        "Tanjiro Kamado",
        "",
        "Has successfully fulfilled all requirements for",
        "",
        "Advanced Computer Vision",
        "",
        "Issued by: Massachusetts Institute of Technology",
        "",
        "Certificate ID: CERT-MIT-2023-001",
        "Institution Code: MIT-001",
        "Issue Date: 2023-08-30",
        "Verification Status: VERIFIED",
    ]

    for line in content:
        draw.text((500, y_pos), line, fill=(15, 15, 15), font=body_font, anchor="mm")
        y_pos += 70

    # Signature line & official badge
    y_pos += 60
    draw.line([(250, y_pos), (750, y_pos)], fill=(80, 80, 80), width=2)
    draw.text((500, y_pos + 30), "Dean of Academic Affairs - MIT", fill=(50, 50, 50),
              font=small_font, anchor="mm")

    filepath = os.path.join(os.path.dirname(__file__), "uploads", "real_certificate_sample.jpg")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath, quality=98)
    print(f"[+] REAL Certificate created: {filepath}")
    return filepath


def create_suspicious_document():
    """Create a suspicious government document"""
    img = Image.new('RGB', (1000, 1400), color='#F0F4F8')
    draw = ImageDraw.Draw(img)
    title_font, header_font, body_font, small_font = get_fonts()

    draw.rectangle([(20, 20), (980, 1380)], outline=(180, 120, 0), width=5)

    draw.text((500, 90), "OFFICIAL IDENTITY DOCUMENT", fill=(160, 100, 0),
              font=title_font, anchor="mm")

    y_pos = 240
    content = [
        "Official Republic Identity Credential",
        "",
        "Holder Name: Jane Doe",
        "",
        "Document Type: PASSPORT",
        "",
        "Document ID: PASS-USA-987654321",
        "",
        "Issuing Authority: Department of State",
        "Country: USA",
        "Issue Date: 2024-05-10",
        "Expiry Date: 2034-05-10"
    ]

    for line in content:
        draw.text((500, y_pos), line, fill=(30, 30, 30), font=body_font, anchor="mm")
        y_pos += 75

    filepath = os.path.join(os.path.dirname(__file__), "uploads", "suspicious_document_sample.jpg")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath, quality=88)
    print(f"[+] SUSPICIOUS Document created: {filepath}")
    return filepath


if __name__ == "__main__":
    print("Generating sample test certificates for Sun Breathing...")
    real_p = create_real_certificate()
    fake_p = create_fake_certificate()
    susp_p = create_suspicious_document()
    print("\nAll sample certificates created in uploads directory.")
