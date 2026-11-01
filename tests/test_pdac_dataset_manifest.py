import json
from pathlib import Path


def load_manifest():
    manifest_path = Path(__file__).parents[1] / "data" / "pdac_datasets.json"
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def test_pdac_dataset_manifest_is_valid_and_traceable():
    manifest = load_manifest()

    assert manifest["target_disease"] == "pancreatic ductal adenocarcinoma (PDAC)"
    datasets = manifest["datasets"]
    accessions = [dataset["accession"] for dataset in datasets]

    assert len(accessions) == len(set(accessions))
    assert {"GSE235548", "GSE169321", "GSE186960", "GSE297770"}.issubset(accessions)

    for dataset in datasets:
        assert dataset["title"]
        assert dataset["organism"] == "Homo sapiens"
        assert dataset["source_url"].startswith("https://")
        assert dataset["role"]
        assert dataset["limitations"]
        assert dataset["geo_sample_composition"]
        assert dataset["geo_response_endpoint"]
        assert dataset["sample_metadata_audit"]
        assert dataset["model_eligibility"]


def test_expression_series_are_not_mislabeled_as_response_assays():
    datasets = {d["accession"]: d for d in load_manifest()["datasets"]}

    assert datasets["GSE169321"]["sample_count_reported"] == 20
    assert "not the drug-sensitivity assay table" in datasets["GSE169321"]["geo_response_endpoint"]

    assert datasets["GSE297770"]["sample_count_reported"] == 5
    assert "not present" in datasets["GSE297770"]["geo_response_endpoint"]
    assert "No treatment-arm RNA-seq samples" in datasets["GSE297770"]["limitations"]

    assert datasets["GSE186960"]["sample_count_reported"] == 6
    assert "not a patient-derived organoid" in datasets["GSE186960"]["model_eligibility"]


def test_response_cohort_requires_publication_phenotype_linkage():
    datasets = {d["accession"]: d for d in load_manifest()["datasets"]}

    assert datasets["GSE235548"]["sample_count_reported"] == 30
    assert "publication response tables" in datasets["GSE235548"]["model_eligibility"]
    assert "not a complete longitudinal response matrix" in datasets["GSE235548"]["geo_response_endpoint"]
