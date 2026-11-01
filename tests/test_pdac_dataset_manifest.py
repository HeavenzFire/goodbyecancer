import json
from pathlib import Path


def test_pdac_dataset_manifest_is_valid_and_traceable():
    manifest_path = Path(__file__).parents[1] / "data" / "pdac_datasets.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["target_disease"] == "pancreatic ductal adenocarcinoma (PDAC)"
    datasets = manifest["datasets"]
    accessions = [dataset["accession"] for dataset in datasets]

    assert len(accessions) == len(set(accessions))
    assert {"GSE235548", "GSE169321", "GSE186960"}.issubset(accessions)

    for dataset in datasets:
        assert dataset["title"]
        assert dataset["organism"] == "Homo sapiens"
        assert dataset["source_url"].startswith("https://")
        assert dataset["role"]
        assert dataset["limitations"]
