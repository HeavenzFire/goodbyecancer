# Experiment 001 — TP53-window chromatin-model smoke test

**Status:** completed exploratory tool smoke test; not a biological discovery.

## Input provenance

- Input: bundled demo sequence `promoter_tp53`
- Sequence length: 25,768 bp
- Demo header: human TP53, GRCh38.p14, chr17:7661779–7687546, strand -1
- Important caveat: the bundled sequence is described as a gene-body window anchored to TP53, not a verified transcription-start-site-centered promoter window.

## Model and output

- Task: chromatin annotation
- Model: `g0-deepsea`
- Model catalog description: ENCODE chromatin-accessibility features across 919 cell types/features
- Reported windows processed: 129
- Reported annotations: 4,075
- Reported label count: 919
- Inference time reported by the service: 620 ms
- Threshold reported: 0.5

## Interpretation

This confirms that a genomic sequence can be submitted to the available chromatin-prediction service and that the service returns structured, multi-window annotations. It does **not** establish a TP53 cancer mechanism, mutation effect, tumor-specific activity, prognosis, or treatment response.

The input window's gene-body context is not sufficient to make promoter-specific claims. A proper follow-up needs a precisely defined genomic interval, strand-aware coordinates, a suitable reference dataset, a relevant cell/tumor context, controls, and independent validation.

## Reproducibility and limitations

The tool response provided a bundled demo identifier and aggregate counts, but this note does not preserve the full raw annotation payload. The run should therefore be treated as a smoke-test record, not a fully archived scientific result. Future experiments should save the complete output, model identifier/version, request metadata, sequence checksum, dataset provenance, and a reproducible command or API request.

No patient data was used. This exploratory result is not for clinical use.
