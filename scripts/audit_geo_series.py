"""Download and audit GEO series metadata without downloading sequencing reads.

The script retrieves GEO family SOFT metadata, extracts one row per GSM sample,
and records SHA-256 provenance. It does not download SRA or supplementary assay
files and does not infer response labels.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import re
import urllib.request
from pathlib import Path
from typing import Iterable

DEFAULT_SERIES = (
    "GSE235548",
    "GSE169321",
    "GSE186960",
    "GSE197613",
    "GSE205013",
    "GSE297770",
)
GEO_SERIES = re.compile(r"^GSE(\d+)$")
SAMPLE_START = re.compile(r"^\^SAMPLE = (GSM\d+)$")
FIELDS = {
    "!Sample_title": "title",
    "!Sample_source_name_ch1": "source_name",
    "!Sample_platform_id": "platform_id",
    "!Sample_characteristics_ch1": "characteristics",
    "!Sample_relation": "relations",
    "!Sample_supplementary_file": "supplementary_files",
}


def family_soft_url(accession: str) -> str:
    match = GEO_SERIES.fullmatch(accession)
    if not match:
        raise ValueError(f"invalid GEO series accession: {accession}")
    digits = match.group(1)
    bucket = "GSE" + digits[:-3] + "nnn"
    return (
        "https://ftp.ncbi.nlm.nih.gov/geo/series/"
        f"{bucket}/{accession}/soft/{accession}_family.soft.gz"
    )


def parse_family_soft(text: str, accession: str) -> list[dict[str, str]]:
    samples: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for line in text.splitlines():
        start = SAMPLE_START.match(line)
        if start:
            if current is not None:
                samples.append(current)
            current = {
                "series_accession": accession,
                "sample_accession": start.group(1),
                "title": "",
                "source_name": "",
                "platform_id": "",
                "characteristics": "",
                "relations": "",
                "supplementary_files": "",
            }
            continue

        if current is None or " = " not in line:
            continue
        key, value = line.split(" = ", 1)
        field = FIELDS.get(key)
        if field:
            existing = current[field]
            current[field] = " | ".join(x for x in (existing, value) if x)

    if current is not None:
        samples.append(current)

    seen: set[str] = set()
    for sample in samples:
        gsm = sample["sample_accession"]
        if gsm in seen:
            raise ValueError(f"duplicate sample accession: {gsm}")
        seen.add(gsm)
    return samples


def download_family_soft(accession: str, cache_dir: Path, timeout: int = 60) -> tuple[Path, str]:
    url = family_soft_url(accession)
    cache_dir.mkdir(parents=True, exist_ok=True)
    target = cache_dir / f"{accession}_family.soft.gz"
    request = urllib.request.Request(
        url, headers={"User-Agent": "GoodbyeCancer-PDAC-provenance-audit/1.0"}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = response.read()
    digest = hashlib.sha256(payload).hexdigest()
    target.write_bytes(payload)
    return target, digest


def audit_series(accession: str, cache_dir: Path, output_dir: Path) -> dict[str, object]:
    source_path, source_sha256 = download_family_soft(accession, cache_dir)
    with gzip.open(source_path, "rt", encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    samples = parse_family_soft(text, accession)

    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / f"{accession}_samples.csv"
    fields = list(samples[0]) if samples else [
        "series_accession", "sample_accession", "title", "source_name",
        "platform_id", "characteristics", "relations", "supplementary_files",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(samples)

    return {
        "series_accession": accession,
        "source_url": family_soft_url(accession),
        "source_file": source_path.name,
        "source_sha256": source_sha256,
        "sample_count": len(samples),
        "sample_manifest": csv_path.name,
        "sample_manifest_sha256": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
    }


def run(series: Iterable[str], cache_dir: Path, output_dir: Path) -> list[dict[str, object]]:
    summaries = [audit_series(accession, cache_dir, output_dir) for accession in series]
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "geo_audit_summary.json"
    summary_path.write_text(
        json.dumps({"schema_version": "1.0", "series": summaries}, indent=2) + "\n",
        encoding="utf-8",
    )
    return summaries


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--series", nargs="+", default=list(DEFAULT_SERIES))
    parser.add_argument("--cache-dir", type=Path, default=Path("data/cache/geo"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/manifests"))
    args = parser.parse_args()
    print(json.dumps(run(args.series, args.cache_dir, args.output_dir), indent=2))


if __name__ == "__main__":
    main()
