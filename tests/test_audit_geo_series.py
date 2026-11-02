import unittest

from scripts.audit_geo_series import family_soft_url, parse_family_soft


FIXTURE = """^SERIES = GSE123456
^SAMPLE = GSM1234567
!Sample_title = PDAC001 baseline
!Sample_source_name_ch1 = patient-derived organoid
!Sample_platform_id = GPL24676
!Sample_characteristics_ch1 = treatment: untreated
!Sample_characteristics_ch1 = cell line: PDAC001
!Sample_relation = BioSample: SAMN000001
!Sample_supplementary_file = https://example.org/counts.txt.gz
^SAMPLE = GSM1234568
!Sample_title = PDAC001 treated
!Sample_source_name_ch1 = patient-derived organoid
!Sample_platform_id = GPL24676
!Sample_characteristics_ch1 = treatment: gemcitabine
"""


class GeoSeriesAuditTests(unittest.TestCase):
    def test_builds_valid_family_soft_url(self):
        self.assertEqual(
            family_soft_url("GSE235548"),
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE235nnn/GSE235548/soft/GSE235548_family.soft.gz",
        )

    def test_rejects_invalid_series_accession(self):
        with self.assertRaises(ValueError):
            family_soft_url("GSM1234567")

    def test_extracts_one_row_per_sample_and_repeated_metadata(self):
        samples = parse_family_soft(FIXTURE, "GSE123456")
        self.assertEqual(len(samples), 2)
        self.assertEqual(samples[0]["sample_accession"], "GSM1234567")
        self.assertIn("treatment: untreated", samples[0]["characteristics"])
        self.assertIn("cell line: PDAC001", samples[0]["characteristics"])
        self.assertEqual(samples[1]["title"], "PDAC001 treated")
        self.assertIn("treatment: gemcitabine", samples[1]["characteristics"])

    def test_rejects_duplicate_sample_accessions(self):
        fixture = FIXTURE + "\n^SAMPLE = GSM1234567\n!Sample_title = duplicate\n"
        with self.assertRaisesRegex(ValueError, "duplicate sample accession"):
            parse_family_soft(fixture, "GSE123456")


if __name__ == "__main__":
    unittest.main()
