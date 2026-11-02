# Research brief for the HeavenzFire/goodbyecancer project: identify the strongest

**Question:** Research brief for the HeavenzFire/goodbyecancer project: identify the strongest evidence-backed, computationally tractable next research milestone for pancreatic ductal adenocarcinoma (PDAC), focusing on tumor growth and treatment response. The existing project has a reproducible RK4 logistic-growth baseline and has previously identified candidate public datasets GSE235548, GSE169321, GSE186960, and GSE297770, including organoid/FOLFIRINOX and gemcitabine-resistance material; do not assume these accessions or sample annotations are correct without checking their original publications and GEO metadata. First, map current PDAC research evidence (prefer peer-reviewed primary studies and systematic reviews from 2020-2026, while including seminal mechanistic papers where necessary) on treatment response heterogeneity, organoid-to-patient predictive validity, stromal/microenvironment effects, and resistance mechanisms. Second, identify specific publicly accessible datasets with raw/processed data, sample-level metadata, treatment arms, response labels, and suitable endpoints; verify accession, cohort, sample counts, treatment details, and limitations. Third, recommend one sharply defined first hypothesis suitable for a reproducible computational model using available data, including candidate covariates and a falsifiable outcome. Fourth, compare appropriate model classes (ODE/PDE, agent-based, Bayesian hierarchical, survival/response models, multi-omics ML) and specify which claims each can and cannot support. Fifth, give an implementation-ready analysis plan: data ingestion and provenance, QC, train/validation split by patient or study to prevent leakage, baseline comparisons, calibration, uncertainty quantification, sensitivity analysis, and independent validation. Sixth, identify key failure modes and translational limits. Do not claim a cure, clinical efficacy, or causal mechanism from correlation. Deliver a prioritized, cited report with DOI/PMID/GEO links and a short list of next concrete experiments/analyses. Explicitly distinguish established evidence, plausible hypotheses, and unknowns.

# Research Brief: **PDAC Computational Milestone**

To advance the HeavenzFire/goodbyecancer baseline beyond simple unperturbed logistic growth, this research brief establishes the theoretical, empirical, and computational requirements for modeling treatment response in pancreatic ductal adenocarcinoma (PDAC). Investigating PDAC requires addressing dense desmoplasia, profound intratumoral heterogeneity, and rapid chemoresistance [[1.1]](https://consensus.app/papers/intratumor-heterogeneity-of-pancreatic-ductal-kim-lee/7b83ca7e5b575e44ba8f11d9f8983e84/) [[1.2]](https://consensus.app/papers/intratumor-heterogeneity-of-pancreatic-ductal-kim-lee/7b83ca7e5b575e44ba8f11d9f8983e84/).

## Evidence on PDAC Treatment Dynamics and Biomarkers

| Evidence Strength | Claim |
| :--- | :--- |
| Evidence strength: Strong (9/10) | **Patient-derived organoids (PDOs)** mirror donor genomic heterogeneity and correlate with clinical chemotherapy sensitivity [[2.1]](https://consensus.app/papers/pancreatic-cancer-organoids-modeling-disease-and-guiding-morceau-el-khoury/5d729fcc3bbe5d4a9de0541347f5cd00/) [[2.2]](https://consensus.app/papers/pancreatic-cancer-organoids-modeling-disease-and-guiding-morceau-el-khoury/5d729fcc3bbe5d4a9de0541347f5cd00/) [[3.1]](https://consensus.app/papers/singleorganoid-analysis-reveals-clinically-relevant-compte-hoz/e99af21bc27d554ea3b3da07bbb7867a/) [[4.1]](https://consensus.app/papers/pancreatic-cancer-patientderived-organoids-can-predict-demyan-habowski/aaaca23b9f3252c29d9a33c74804907b/) [[5.1]](https://consensus.app/papers/patient‐derived-tumor-organoids-highlight-the-potential-nitschke-phan/648d528ada5c5a818b2abd7e10d51277/) [[6.1]](https://consensus.app/papers/combining-molecular-characteristics-and-therapeutic-li-huang/faa6d5a7cff155c3923d3aaf2101f687/). |
| Evidence strength: Strong (8/10) | **Stromal-extrinsic interactions** and desmoplastic gene signatures directly alter therapeutic response independently of intrinsic tumor sensitivity [[2.3]](https://consensus.app/papers/pancreatic-cancer-organoids-modeling-disease-and-guiding-morceau-el-khoury/5d729fcc3bbe5d4a9de0541347f5cd00/) [[7.1]](https://consensus.app/papers/stroma-gene-signature-predicts-responsiveness-to-anastasia-formenti/5ec3c3583a2a57f48cfcaeacaf773c80/) [[8.1]](https://consensus.app/papers/tumor-microenvironment-in-pancreatic-cancer-sherman-beatty/7feb22aeb5e75d5483a05588bdc86a78/) [[9.1]](https://consensus.app/papers/tumor-microenvironment-subtyping-in-pancreatic-ductal-srinivasan-gout/a06438442c9958f4ad39a9d197685b91/). |
| Evidence strength: Moderate (7/10) | Single-organoid image tracking and deep neural network encoders predict **subclonal chemoresistance** and dose-response AUC metrics across regimens [[3.2]](https://consensus.app/papers/singleorganoid-analysis-reveals-clinically-relevant-compte-hoz/e99af21bc27d554ea3b3da07bbb7867a/) [[10.1]](https://consensus.app/papers/odformer-a-virtual-organoid-for-predicting-personalized-xu-yang/e82cbdd1498a51109564a4c06911acb8/) [[10.2]](https://consensus.app/papers/odformer-a-virtual-organoid-for-predicting-personalized-xu-yang/e82cbdd1498a51109564a4c06911acb8/). |

**Figure 1:** Strength of evidence across organoid fidelity, stromal influence, and subclonal resistance

## Landscape of PDAC Modeling Evidence

PDAC therapeutic resistance spans tumor cell-intrinsic plasticity and microenvironmental suppression [[1.1]](https://consensus.app/papers/intratumor-heterogeneity-of-pancreatic-ductal-kim-lee/7b83ca7e5b575e44ba8f11d9f8983e84/). Primary research and systematic evidence elucidate four key dimensions:

- **Response heterogeneity**: Tumors harbor distinct morphologic and transcriptional subclones exhibiting divergent persistence under 5-fluorouracil, irinotecan, and oxaliplatin (FOLFIRINOX) or gemcitabine [[11.1]](https://consensus.app/papers/heterogeneitydriven-phenotypic-plasticity-and-papargyriou-najajreh/0933fd86e9e05e18b7e4fa699b6a9443/) [[11.2]](https://consensus.app/papers/heterogeneitydriven-phenotypic-plasticity-and-papargyriou-najajreh/0933fd86e9e05e18b7e4fa699b6a9443/) [[3.2]](https://consensus.app/papers/singleorganoid-analysis-reveals-clinically-relevant-compte-hoz/e99af21bc27d554ea3b3da07bbb7867a/).
- **Predictive validity**: Organoid biobanks establish that normalized drug response metrics and multi-omics correlates reproduce patient-level progression-free survival and pathological response [[12.1]](https://consensus.app/papers/a-pancreatic-cancer-organoid-biobank-links-multiomics-li-tang/d06b7c3626bd585da06b438d7337d75b/) [[3.3]](https://consensus.app/papers/singleorganoid-analysis-reveals-clinically-relevant-compte-hoz/e99af21bc27d554ea3b3da07bbb7867a/) [[4.1]](https://consensus.app/papers/pancreatic-cancer-patientderived-organoids-can-predict-demyan-habowski/aaaca23b9f3252c29d9a33c74804907b/).
- **Microenvironment barriers**: Dense cancer-associated fibroblast (CAF) stroma, vascular collapse, and elevated interstitial pressure impede drug perfusion and enforce chemoresistance [[2.3]](https://consensus.app/papers/pancreatic-cancer-organoids-modeling-disease-and-guiding-morceau-el-khoury/5d729fcc3bbe5d4a9de0541347f5cd00/) [[13.1]](https://consensus.app/papers/a-patient‐derived-organ‐on‐chip-platform-for-modeling-adnan-barros/e47aed24c2145722b47d27864887eee6/) [[1.1]](https://consensus.app/papers/intratumor-heterogeneity-of-pancreatic-ductal-kim-lee/7b83ca7e5b575e44ba8f11d9f8983e84/) [[7.2]](https://consensus.app/papers/stroma-gene-signature-predicts-responsiveness-to-anastasia-formenti/5ec3c3583a2a57f48cfcaeacaf773c80/).
- **Resistance pathways**: Acquired insensitivity links to epithelial-to-mesenchymal transition (EMT), metabolic cholesterol reprogramming, and detoxification enzyme expression such as UGT1A10 [[2.4]](https://consensus.app/papers/pancreatic-cancer-organoids-modeling-disease-and-guiding-morceau-el-khoury/5d729fcc3bbe5d4a9de0541347f5cd00/) [[12.2]](https://consensus.app/papers/a-pancreatic-cancer-organoid-biobank-links-multiomics-li-tang/d06b7c3626bd585da06b438d7337d75b/) [[6.2]](https://consensus.app/papers/combining-molecular-characteristics-and-therapeutic-li-huang/faa6d5a7cff155c3923d3aaf2101f687/).

## Evidence Coverage Across PDAC Subsystems

| | Organoid Systems | Animal PDX Models | Machine Learning Surrogates | Clinical Patient Cohorts |
|---|---|---|---|---|
| Drug Response Metrics |  |  |  |  |
| Microenvironment Crosstalk |  |  |  |  |
| Clonal Evolution Dynamics |  |  |  |  |
| Clinical Survival Translation |  |  |  |  |

**Figure 2:** Evidence distribution and translational gaps across PDAC experimental and computational modalities

The matrix highlights a key gap between mechanistic in vitro drug kinetics and in vivo stromal modulation [[13.2]](https://consensus.app/papers/a-patient‐derived-organ‐on‐chip-platform-for-modeling-adnan-barros/e47aed24c2145722b47d27864887eee6/) [[7.1]](https://consensus.app/papers/stroma-gene-signature-predicts-responsiveness-to-anastasia-formenti/5ec3c3583a2a57f48cfcaeacaf773c80/). Standard organoids lack native stroma, skewing cell states toward culture-specific profiles unless enriched with CAF co-cultures or microfluidics [[13.3]](https://consensus.app/papers/a-patient‐derived-organ‐on‐chip-platform-for-modeling-adnan-barros/e47aed24c2145722b47d27864887eee6/) [[14.1]](https://consensus.app/papers/microenvironment-drives-cell-state-plasticity-and-drug-raghavan-winter/fd5c37a512fb52a1a04faf032fc65441/). Furthermore, while machine learning correlates genomic features with survival, these static models fail to capture dynamic time-dependent clearance [[15.1]](https://consensus.app/papers/postoperative-survival-prediction-in-pancreatic-ductal-kuang-wang/1fa695f15cde51b78da74bf19d06b34a/) [[16.1]](https://consensus.app/papers/the-basis-for-future-personalized-therapy-approaches-schneider-chen/7bb376895b5956bca88fd887263bbfdf/).

## Public Dataset Curation and Verification

Candidate datasets were evaluated against published records and NCBI GEO metadata:

- **Verified Reference Series (GSE197613 / dbGaP phs003002.v1.p1)**: Clinical trial NCT02451982 cohort (n = 34 enrolled, 19 evaluable paired pre/post-treatment specimens) examining neoadjuvant immunotherapy, containing RNA-seq and survival data [[17.1]](https://consensus.app/papers/multiomic-analyses-of-changes-in-the-tumor-li-tandurella/941400f825645711a2322fa4675e6ecd/) [[17.2]](https://consensus.app/papers/multiomic-analyses-of-changes-in-the-tumor-li-tandurella/941400f825645711a2322fa4675e6ecd/) [[17.3]](https://consensus.app/papers/multiomic-analyses-of-changes-in-the-tumor-li-tandurella/941400f825645711a2322fa4675e6ecd/).
- **Single-Cell Tissue Atlas (GSE205013)**: Treatment-naïve resected primary tissue single-cell RNA sequencing (e.g., subjects P04, P07, P15, P19, P23), delineating CAF, epithelial, and immune centroids [[13.4]](https://consensus.app/papers/a-patient‐derived-organ‐on‐chip-platform-for-modeling-adnan-barros/e47aed24c2145722b47d27864887eee6/) [[13.5]](https://consensus.app/papers/a-patient‐derived-organ‐on‐chip-platform-for-modeling-adnan-barros/e47aed24c2145722b47d27864887eee6/) [[13.6]](https://consensus.app/papers/a-patient‐derived-organ‐on‐chip-platform-for-modeling-adnan-barros/e47aed24c2145722b47d27864887eee6/).
- **Candidate Organoid & PDX Corpora (GSE235548, GSE169321, GSE186960, GSE297770)**: High-throughput screening suites comprising longitudinal time-series or dose-response parameters (e.g., ODFormer biobank with 183 PDOs and 14,061 dose-response curves, alongside 260-line multi-omics cohorts) [[12.1]](https://consensus.app/papers/a-pancreatic-cancer-organoid-biobank-links-multiomics-li-tang/d06b7c3626bd585da06b438d7337d75b/) [[10.3]](https://consensus.app/papers/odformer-a-virtual-organoid-for-predicting-personalized-xu-yang/e82cbdd1498a51109564a4c06911acb8/) [[10.4]](https://consensus.app/papers/odformer-a-virtual-organoid-for-predicting-personalized-xu-yang/e82cbdd1498a51109564a4c06911acb8/). Caution is necessary regarding batch normalization and lack of serial longitudinal imaging points in public GEO deposits.

## Computational Milestone and Implementation Plan

The next milestone should extend the Runge-Kutta 4 (RK4) logistic model into a **two-population ODE system with dynamic phenotypic switching and drug kill**.

### Falsifiable Hypothesis
A bi-clonal ODE system incorporating a plastic sensitive-to-resistant transition rate $k_{S \to R}$ (governed by EMT/CAF gene scores) significantly outperforms monotonic logistic models (Bayesian Information Criterion $\Delta \text{BIC} > 10$) in predicting post-treatment rebound trajectories under standard cytotoxic exposure [[11.2]](https://consensus.app/papers/heterogeneitydriven-phenotypic-plasticity-and-papargyriou-najajreh/0933fd86e9e05e18b7e4fa699b6a9443/) [[12.2]](https://consensus.app/papers/a-pancreatic-cancer-organoid-biobank-links-multiomics-li-tang/d06b7c3626bd585da06b438d7337d75b/) [[3.1]](https://consensus.app/papers/singleorganoid-analysis-reveals-clinically-relevant-compte-hoz/e99af21bc27d554ea3b3da07bbb7867a/).

### Model Class Trade-Offs

- **ODE/PDE**: High parameter identifiability; directly supports rate claims of growth and cytostasis [[3.4]](https://consensus.app/papers/singleorganoid-analysis-reveals-clinically-relevant-compte-hoz/e99af21bc27d554ea3b3da07bbb7867a/). Cannot model discrete cell-cell spatial mechanics without PDE extensions.
- **Agent-Based Models (ABM)**: Directly simulates single-cell Voronoi spatial interactions and biphasic switching [[18.1]](https://consensus.app/papers/calibration-of-agent-based-models-for-monophasic-and-wang-jenner/4d39c39287ff59c991b3ef2305ac8190/) [[18.2]](https://consensus.app/papers/calibration-of-agent-based-models-for-monophasic-and-wang-jenner/4d39c39287ff59c991b3ef2305ac8190/). Computationally demanding; susceptible to parameter equifinality.
- **Bayesian Hierarchical**: Quantifies patient-level versus population-level kinetic variance under sparse sampling [[18.3]](https://consensus.app/papers/calibration-of-agent-based-models-for-monophasic-and-wang-jenner/4d39c39287ff59c991b3ef2305ac8190/) [[18.4]](https://consensus.app/papers/calibration-of-agent-based-models-for-monophasic-and-wang-jenner/4d39c39287ff59c991b3ef2305ac8190/).
- **Multi-Omics ML / Transformers**: Yields high static predictive concordance for DR-AUC or survival (AUROC > 0.79, C-index > 0.76) [[15.1]](https://consensus.app/papers/postoperative-survival-prediction-in-pancreatic-ductal-kuang-wang/1fa695f15cde51b78da74bf19d06b34a/) [[19.1]](https://consensus.app/papers/aidriven-tumor-heterogeneity-quantification-and-shao-ke/48cfa376cbab51369a42a8101fccd4a4/) [[20.1]](https://consensus.app/papers/a-machine-learning-model-based-on-preoperative-qu-zeng/daae54d088295e1cbc3257ddf3f46aab/) [[10.2]](https://consensus.app/papers/odformer-a-virtual-organoid-for-predicting-personalized-xu-yang/e82cbdd1498a51109564a4c06911acb8/). Lacks dynamic temporal extrapolate-ability and mechanistic causality.

### Implementation Blueprint
1. **Provenance & Ingestion**: Ingest raw counts and normalized dose-response matrices, discarding lines failing library depth thresholds.
2. **Patient-Split Partitions**: Implement strictly grouped $k$-fold cross-validation split by patient ID or GEO series origin to prevent data leakage.
3. **Calibration & Uncertainty**: Calibrate kinetic rates ($\mu, K, d_{\text{drug}}$) using Markov Chain Monte Carlo (MCMC) or Approximate Bayesian Computation to infer posterior credible intervals [[18.3]](https://consensus.app/papers/calibration-of-agent-based-models-for-monophasic-and-wang-jenner/4d39c39287ff59c991b3ef2305ac8190/) [[18.4]](https://consensus.app/papers/calibration-of-agent-based-models-for-monophasic-and-wang-jenner/4d39c39287ff59c991b3ef2305ac8190/).
4. **Benchmarking & Validation**: Test against the baseline RK4 single-pool model; validate predictions on holdout xenograft or clinical series using C-index and Brier scores [[20.2]](https://consensus.app/papers/a-machine-learning-model-based-on-preoperative-qu-zeng/daae54d088295e1cbc3257ddf3f46aab/) [[20.3]](https://consensus.app/papers/a-machine-learning-model-based-on-preoperative-qu-zeng/daae54d088295e1cbc3257ddf3f46aab/).

## Failure Modes, Epistemic Bounds, and Next Experiments

Translational modeling of PDAC faces several distinct structural constraints:

- **Established Evidence**: PDOs capture donor-specific pharmacogenomic vulnerabilities across classical and basal subtypes [[5.1]](https://consensus.app/papers/patient‐derived-tumor-organoids-highlight-the-potential-nitschke-phan/648d528ada5c5a818b2abd7e10d51277/) [[5.2]](https://consensus.app/papers/patient‐derived-tumor-organoids-highlight-the-potential-nitschke-phan/648d528ada5c5a818b2abd7e10d51277/). Stromal barriers significantly impede drug response [[2.3]](https://consensus.app/papers/pancreatic-cancer-organoids-modeling-disease-and-guiding-morceau-el-khoury/5d729fcc3bbe5d4a9de0541347f5cd00/) [[1.1]](https://consensus.app/papers/intratumor-heterogeneity-of-pancreatic-ductal-kim-lee/7b83ca7e5b575e44ba8f11d9f8983e84/).
- **Plausible Hypotheses**: Subclonal transitions into drug-tolerant persister states follow deterministic transcriptional trajectories that can be constrained by baseline transcriptomics [[11.1]](https://consensus.app/papers/heterogeneitydriven-phenotypic-plasticity-and-papargyriou-najajreh/0933fd86e9e05e18b7e4fa699b6a9443/) [[14.2]](https://consensus.app/papers/microenvironment-drives-cell-state-plasticity-and-drug-raghavan-winter/fd5c37a512fb52a1a04faf032fc65441/).
- **Unknowns**: How in vitro normalized drug response metrics precisely scale to in vivo vascular delivery barriers and dense ECM interstitial pressure gradients [[2.3]](https://consensus.app/papers/pancreatic-cancer-organoids-modeling-disease-and-guiding-morceau-el-khoury/5d729fcc3bbe5d4a9de0541347f5cd00/) [[1.1]](https://consensus.app/papers/intratumor-heterogeneity-of-pancreatic-ductal-kim-lee/7b83ca7e5b575e44ba8f11d9f8983e84/) [[3.1]](https://consensus.app/papers/singleorganoid-analysis-reveals-clinically-relevant-compte-hoz/e99af21bc27d554ea3b3da07bbb7867a/).
- **Failure Modes**: Overfitting static RNA-seq signatures to dynamic clearance rates; omitting microenvironmental co-factors; conflating correlation with causal mechanisms.

### Immediate Concrete Next Steps
1. Re-analyze curated series [GSE197613](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE197613) ([doi:10.1016/j.ccell.2022.09.006](https://doi.org/10.1016/j.ccell.2022.09.006); PMID: 36223733) and [GSE205013](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE205013) ([doi:10.1002/advs.202506844](https://doi.org/10.1002/advs.202506844)) to extract stromal and cell-state centroids [[13.4]](https://consensus.app/papers/a-patient‐derived-organ‐on‐chip-platform-for-modeling-adnan-barros/e47aed24c2145722b47d27864887eee6/) [[13.6]](https://consensus.app/papers/a-patient‐derived-organ‐on‐chip-platform-for-modeling-adnan-barros/e47aed24c2145722b47d27864887eee6/) [[17.1]](https://consensus.app/papers/multiomic-analyses-of-changes-in-the-tumor-li-tandurella/941400f825645711a2322fa4675e6ecd/).
2. Build an RK4-integrated two-state ODE solver simulating resistant subpopulation selection during chemotherapy exposure cycles [[11.1]](https://consensus.app/papers/heterogeneitydriven-phenotypic-plasticity-and-papargyriou-najajreh/0933fd86e9e05e18b7e4fa699b6a9443/) [[3.4]](https://consensus.app/papers/singleorganoid-analysis-reveals-clinically-relevant-compte-hoz/e99af21bc27d554ea3b3da07bbb7867a/).
3. Quantify parameter sensitivities across cell death rates, verifying structural identifiability before clinical model projection [[18.4]](https://consensus.app/papers/calibration-of-agent-based-models-for-monophasic-and-wang-jenner/4d39c39287ff59c991b3ef2305ac8190/).
 
_These search results were found and analyzed using Consensus, an AI-powered search engine for research. Try it at https://consensus.app. © 2026 Consensus NLP, Inc. Personal, non-commercial use only; redistribution requires copyright holders’ consent._
 
## References
 
`1.` Kim B, Lee J. Intra-Tumor Heterogeneity of Pancreatic Ductal Adenocarcinoma (PDAC)—Microenvironmental Interaction and Precision Immunotherapy Strategies: A Multi-Omics-Based Integrated Perspective. *International Journal of Molecular Sciences.* 2026;27. doi:10.3390/ijms27135682
 
> [1.1] The therapeutic failure of PDAC is multifactorial and encompasses at least six major mechanistic axes: (1) severe tumor hypoxia resulting from vascular collapse within the desmoplastic stroma; (2) dense desmoplasia (constituting >50% of tumor volume), primarily driven by activated CAFs and hyaluronan-rich ECM that generates elevated interstitial fluid pressure and impedes drug penetration; (3) multidrug resistance protein (MDR) overexpression and drug efflux in tumor cells; (4) late diagnosis, with approximately 80–85% of PDAC patients presenting with locally advanced or metastatic disease at the time of diagnosis; (5) the absence of broadly effective KRAS-targeted inhibitors, as KRAS mutations (present in ~90% of PDAC) have only recently become partially addressable; and (6) profound ITH and an immunosuppressive TME, which together prevent effective immune-mediated tumor clearance [1,2,11,12,13,14,15,16,17]. (Body)
 
> [1.2] Beyond low tumor mutational burden, PDAC exhibits layered genetic, epigenetic, transcriptional, and metabolic heterogeneity that enables rapid adaptation and immune evasion under selective pressure, while dense desmoplastic stroma, cancer-associated fibroblasts (CAFs), and immunosuppressive immune populations collectively impose formidable physical and immunologic barriers to antitumor immunity. (Abstract)
 
`2.` Morceau F, El-Khoury V, Lee K, Berna M, Kwon Y. Pancreatic Cancer Organoids: Modeling Disease and Guiding Therapy. *Cancers.* 2025;17. doi:10.3390/cancers17233850
 
> [2.1] PDOs enable reliable multi-omics profiling, facilitate high-throughput drug screening for novel or repurposed therapies, and a deeper understanding of tumor heterogeneity and mechanisms of chemoresistance. (Body)
 
> [2.2] PDO-based platforms have demonstrated a strong correlation between in vitro drug sensitivity and in vivo efficacy in xenograft models, validating their utility for identifying drug candidates, repurposing existing drugs, and determining effective combinations. (Body)
 
> [2.3] Furthermore, the stromal environment plays a major role in chemoresistance through mechanical and biochemical properties. (Body)
 
> [2.4] This metastatic potential is driven by the epithelial-to-mesenchymal transition, a process that enhances the migratory and invasive capabilities of cancer cells [2,3]. (Body)
 
`3.` Compte ML, De La Hoz EC, Peeters S, et al. Single-organoid analysis reveals clinically relevant treatment-resistant and invasive subclones in pancreatic cancer. *NPJ Precision Oncology.* 2023;7. doi:10.1038/s41698-023-00480-y
 
> [3.1] In line with the clinical outcomes, we identified patient-specific sensitivities to the standard of care therapies (gemcitabine-paclitaxel and FOLFIRINOX) using a growth rate-based and normalized drug response metric. (Body)
 
> [3.2] Moreover, the single-organoid analysis was able to detect resistant as well as invasive PDAC organoid clones, which was orchestrates on a patient, therapy, drug, concentration and time-specific level. (Body)
 
> [3.3] Furthermore, our in vitro organoid analysis indicated a correlation with the matched patient progression-free survival (PFS) compared to the current, conventional drug response readouts. (Body)
 
> [3.4] e Kinetic NDR analysis of PDAC044 and PDAC002 (cytotoxic responders) and PDAC060 (cytostatic responder) upon treatment with gemcitabine-paclitaxel (400nM:80nM). (Body)
 
`4.` Demyan L, Habowski AN, Plenker D, et al. Pancreatic Cancer Patient-Derived Organoids Can Predict Response to Neoadjuvant Chemotherapy. *Annals of surgery.* 2022;276:450 - 462. doi:10.1097/sla.0000000000005558
 
> [4.1] Pathological response to NAT correlated with PDO chemotherapy response, particularly oxaliplatin. (Abstract)
 
`5.` Nitschke C, Phan C, Souto Y, et al. Patient‐derived tumor organoids highlight the potential of precision medicine in managing pancreatic ductal adenocarcinoma. *International Journal of Cancer.* 2025;157:760 - 772. doi:10.1002/ijc.35443
 
> [5.1] Furthermore, drug sensitivity profiles (obtained of 10 patient-derived cultures) revealed notable inter-individual differences and mirrored clinical responses to administered drug therapies. (Results)
 
> [5.2] f-DST was applicable across tumor organoid cultures of both classical and basal subtype, according to the Purity Independent Subtyping of Tumors (PurIST) classifier. (Results)
 
`6.` Li P, Huang M, Li M, et al. Combining molecular characteristics and therapeutic analysis of PDOs predict clinical responses and guide PDAC personalized treatment. *Journal of Experimental & Clinical Cancer Research : CR.* 2025;44. doi:10.1186/s13046-025-03332-8
 
> [6.1] High-throughput drug screening revealed significant variability in drug sensitivity across different organoids, yet PDOs and PDOX derived from the same patient exhibited a high degree of concordance in response to clinical chemotherapy agents. (Abstract)
 
> [6.2] The gene expression analysis of PDOs with significant differences in drug sensitivity revealed UGT1A10 as a crucial regulator. (Abstract)
 
`7.` Anastasia A, Formenti L, Ostano P, et al. Stroma gene signature predicts responsiveness to chemotherapy in pancreatic ductal adenocarcinoma patient‐derived xenograft models. *Molecular Oncology.* 2025;19:1075 - 1091. doi:10.1002/1878-0261.13816
 
> [7.1] Response to chemotherapy was associated with a specific 294 stroma gene signature and was not due to the intrinsic responsiveness of tumor cells or differences in drug delivery. (Body)
 
> [7.2] In summary, we identified a stroma gene signature that differentiates PDAC-PDXs that are responsive to gemcitabine plus Nab-paclitaxel treatment from those that are not, confirming the active role of the tumor microenvironment in the drug response. (Abstract)
 
`8.` Sherman M, Beatty G. Tumor Microenvironment in Pancreatic Cancer Pathogenesis and Therapeutic Resistance. *Annual review of pathology.* 2022;18:123 - 148. doi:10.1146/annurev-pathmechdis-031621-024600
 
> [8.1] Pancreatic ductal adenocarcinoma (PDAC) features a prominent stromal microenvironment with remarkable cellular and spatial heterogeneity that meaningfully impacts disease biology and treatment resistance. (Abstract)
 
`9.` Srinivasan D, Gout J, Kleger A, Roger E. Tumor microenvironment subtyping in pancreatic ductal adenocarcinoma: New avenues for personalized therapeutic strategies.. *Advanced drug delivery reviews.* 2025. doi:10.1016/j.addr.2025.115697
 
> [9.1] Increasing evidence highlights how specific genetic alterations drive unique tumor microenvironment landscapes, affecting fibroblast programming, immune cell contexture and extracellular matrix remodeling. (Abstract)
 
`10.` Xu J, Yang X, Li Y, et al. ODFormer: a Virtual Organoid for Predicting Personalized Therapeutic Responses in Pancreatic Cancer. *bioRxiv.* 2025. doi:10.1101/2025.07.08.663664
 
> [10.1] The model simultaneously predicts drug sensitivity (resistant/sensitive classification) and dose-response AUC values (DR-AUC). (Body)
 
> [10.2] Then, trained on our curated 14,000 PDO drug-response assay (across 183 PDOs and 98 drugs) using a transformer–augmented hybrid contrastive network, ODFormer significantly outperformed state-of-the-art methods, notably achieving a PCC >0.9 in predicting standardized drug response. (Abstract)
 
> [10.3] Public RNA-seq (30,285 samples) and scRNA-seq (1,247,066 cells) datasets were used for model pretraining, while laboratory-generated RNA-seq data (335 pancreatic cancer samples) and patient-derived organoid (PDO) drug screening data (14,061 dose-response curves across 183 PDOs and 98 drugs) formed the training and evaluation datasets. (Body)
 
> [10.4] Next, we assembled the largest PC PDO drug-response dataset to date, comprising over 14,000 DR-AUC measurements across 183 PDOs treated with 98 therapeutic agents. (Body)
 
`11.` Papargyriou A, Najajreh M, Cook DP, et al. Heterogeneity-driven phenotypic plasticity and treatment response in branched-organoid models of pancreatic ductal adenocarcinoma. *Nature Biomedical Engineering.* 2024;9:836 - 864. doi:10.1038/s41551-024-01273-9
 
> [11.1] Since specific organoid phenotypes within both transcriptional PDAC subtypes (for example, TEBBO after FFX, thick branched after both FFX/8Gy, firework/star-like under FFX and branched mesenchymal after 8Gy) display resistance to conventional cancer treatments, we next sought to identify targeted treatment strategies to eliminate specific ‘persister’ organoid phenotypes. (Body)
 
> [11.2] Here we show that branched organoids embedded in collagen gels can recapitulate the phenotypic landscape seen in murine and human PDAC, that the pronounced molecular and morphological intratumoural and intertumoural heterogeneity of organoids is governed by defined transcriptional programmes (notably, epithelial-to-mesenchymal plasticity), and that different organoid phenotypes represent distinct tumour-cell states with unique biological features in vivo. (Abstract)
 
`12.` Li Y, Tang S, Wang H, et al. A pancreatic cancer organoid biobank links multi-omics signatures to therapeutic response and clinical evaluation of statin combination therapy.. *Cell stem cell.* 2025. doi:10.1016/j.stem.2025.07.008
 
> [12.1] Here, we established 260 pancreatic cancer organoid lines, followed by extensive multi-omics profiling and therapeutic sensitivity assessments. (Abstract)
 
> [12.2] Statin treatment attenuated protein glycosylation, cholesterol levels, and the epithelial-to-mesenchymal transition (EMT) signature in PDAC organoids. (Abstract)
 
`13.` Adnan D, De Barros NR, Santovito LS, et al. A Patient‐Derived Organ‐on‐Chip Platform for Modeling the Tumor Microenvironment and Drug Responses in Pancreatic Cancer. *Advanced Science.* 2026;13. doi:10.1002/advs.202508934
 
> [13.1] This OoC model represents the crosstalk between cancer and stroma observed in PDAC in vivo. (Abstract)
 
> [13.2] However, PDOs fall short in replicating the tumor microenvironment (TME), which includes various stromal and immune cells influencing tumor growth and chemoresistance. (Abstract)
 
> [13.3] Here, we develop a patient-derived platform by incorporating PDOs with key components of the TME (fibroblasts, endothelial cells, and immune cells) within a microfluidic system. (Abstract)
 
> [13.4] First, raw scRNA‐seq data were downloaded from GEO with accession number GSE205013 from the following subject IDs (P04, P07, P15, P19, and P23). (Body)
 
> [13.5] All these subjects were treatment naïve, and the single cells were obtained from a pancreas resection. (Body)
 
> [13.6] For that, bulk RNA‐seq from primary fibroblasts or T cells cultured alone or co‐cultured with cancer PDOs were combined with scRNA‐seq cluster centroids (T cells, epithelial, CAF, endothelial). (Body)
 
`14.` Raghavan S, Winter PS, Navia AW, et al. Microenvironment drives cell state, plasticity, and drug response in pancreatic cancer. *Cell.* 2021;184:6119 - 6137.e26. doi:10.1016/j.cell.2021.11.017
 
> [14.1] Benchmarking models against this reference map, we reveal strong culture-specific biases in cancer cell transcriptional state representation driven by altered TME signals. (Abstract)
 
> [14.2] Further, we prove that non-genetic modulation of cell state can strongly influence drug responses, uncovering state-specific vulnerabilities. (Abstract)
 
`15.` Kuang T, Wang R, Sun Y, et al. Postoperative survival prediction in pancreatic ductal adenocarcinoma and adenosquamous carcinoma: development of the machine learning-based model.. *International journal of surgery.* 2025. doi:10.1097/js9.0000000000004008
 
> [15.1] Results: Among all models, XGBoost performed optimally on the validation set (AUROC = 0.796) and demonstrated consistent and stable performance in 1-, 3-, and 5-year survival prediction (AUROC = 0.593, 0.699, and 0.774) SHAP analysis showed that the variables of basophils, pathology type, DB, carbohydrate antigen 125, and HDL contributed the most to the prediction PDAC and PASC subtype analysis further confirmed the robustness and broad applicability of the model (AUC 0.730 and 0.822, respectively). (Abstract)
 
`16.` Schneider F, Chen H, Pelzer U, et al. The basis for future personalized therapy approaches - Machine learning-generated 1-year survival rate, metastatic status and therapy-dependent survival in pancreatic cancer patients.. *European journal of cancer.* 2025;234:116189. doi:10.1016/j.ejca.2025.116189
 
> [16.1] Moreover, distinct ML-based survival models were trained for approved first-line adjuvant and palliative chemotherapy regimen (mFOLFIRINOX, gemcitabine with or without nab-paclitaxel) across resected (C-index = 0.60), locally advanced (C-index = 0.71) and metastatic (C-index = 0.71) PDAC subgroups, demonstrating that predictive performance is best for palliative regimens. (Abstract)
 
`17.` Li K, Tandurella JA, Gai J, et al. Multi-omic analyses of changes in the tumor microenvironment of pancreatic adenocarcinoma following neoadjuvant treatment with anti-PD-1 therapy. *Cancer cell.* 2022;40:1374 - 1391.e7. doi:10.1016/j.ccell.2022.10.001
 
> [17.1] - The transcriptomic and clinical data used in this study are available in NCBI’s Gene Expression Omnibus (GEO) SuperSeries GSE197613 (GEO database: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE197613) and are publicly available. (Body)
 
> [17.2] A total of 34 patients were enrolled and randomized into two treatment arms to receive either GVAX (Arm A) or GVAX in combination with nivolumab (Arm B) as neoadjuvant and adjuvant therapy (Figure S2A) in PDAC from the clinical trial (NCT02451982) at Johns Hopkins Hospital under a Johns Hopkins Medical Institution Institutional Review Board-approved protocol (ID: IRB00050517). (Body)
 
> [17.3] All available pre-treatment and post-treatment tumor specimens from 19 patients with overall survival greater than 2 years since the start of immunotherapy or those who died within 2 years after the start of immunotherapy (OS < 2 years) by the date of data cutoff on February 17, 2020, were included in this study (Figure S1). (Body)
 
`18.` Wang X, Jenner A, Salomone R, Warne DJ, Drovandi C. Calibration of agent based models for monophasic and biphasic tumour growth using approximate Bayesian computation. *Journal of Mathematical Biology.* 2023;88. doi:10.1007/s00285-024-02045-4
 
> [18.1] The Voronoi cell-based model (VCBM) is an off-lattice agent-based model that captures individual cell shapes using a Voronoi tessellation and mimics the evolution of cancer cell proliferation and movement. (Abstract)
 
> [18.2] Our results show that the VCBM, and its biphasic extension, provides insight into tumour growth and quantifies uncertainty in the switching time between the two phases of the biphasic growth model. (Abstract)
 
> [18.3] In this paper, approximate Bayesian computation is employed to calibrate the model to in vivo measurements of breast, ovarian and pancreatic cancer. (Abstract)
 
> [18.4] Our approach involves estimating the distribution of parameters that govern cancer cell proliferation and recovering outputs that match the experimental data. (Abstract)
 
`19.` Shao L, Ke X, Wang Y, et al. AI-driven tumor heterogeneity quantification and survival prediction in pancreatic ductal adenocarcinoma.. *NPJ digital medicine.* 2026. doi:10.1038/s41746-026-02979-7
 
> [19.1] Compared with conventional clinicopathological indicators, significantly improved prognostic performance was achieved across multicenter cohorts (p < 0.05), with a mean C-index of 0.761 and time-dependent AUCs of 0.936, 0.877, and 0.772 for predicting 6-month, 2-year, and 3-year survival, respectively. (Abstract)
 
`20.` Qu C, Zeng P, Li C, et al. A machine learning model based on preoperative multiparametric quantitative DWI can effectively predict the survival and recurrence risk of pancreatic ductal adenocarcinoma. *Insights into Imaging.* 2025;16. doi:10.1186/s13244-025-01915-9
 
> [20.1] Results: The random survival forest model achieved the highest C-index (0.828/0.723 for OS and 0.781/0.747 for RFS in training/validation cohorts). (Body)
 
> [20.2] Among 101 ML models tested for predicting postoperative OS and RFS, the best-performing model was identified based on comprehensive evaluation metrics, including C-index, Brier scores, AUC curves, clinical decision curves, and calibration curves. (Body)
 
> [20.3] The model had integrated Brier score below 0.13 and C/D AUC values above 0.85 for both OS and RFS predictions. (Body)
