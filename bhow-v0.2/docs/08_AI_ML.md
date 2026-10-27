# 08 — ML strategy: ambitious discovery, calibrated uncertainty

## What needs ML, and what must not

| Use case | Data path | Rule |
|---|---|---|
| Breed visual resemblance | Dog image → quality gate → model candidate scores → calibration → abstain/describe | No genetic ancestry claim; no diagnosis from appearance |
| Food label photo | Image → OCR → editable transcript → approved ingredient lookup | Never infer safe from missing matches |
| Document parsing | Record photo → OCR → editable extracted fields → caregiver confirms → unverified record | Only authenticated vet can verify |
| Walk guidance | Licensed weather/AQI → typed domain + validated safety guidelines | Explicit freshness; when missing, fall back to nonlive generic advice |
| Symptom observation | Structured inputs + vet-reviewed red flags → next-step resource | NEVER unsupervised image diagnosis/medicine dosing |
| Lost dog similarity | Photos → retrieval candidates → human verification | Not proof of identity; strong abuse controls |

## Breed ML model spec (`breed-visual-v1`)

- Collect legally licensed, consented photos spanning Indian Indies, mixed breeds, Indian named breeds and common foreign breeds; document exclusions and ambiguous labels.
- Split train/validation/test by **dog identity**, not only by photo, to avoid leakage. Include field photos: low light, crowd, mixed background, age and coat variation.
- Prefer a lightweight proven vision backbone; PyTorch for training, ONNX for serving; release only if reproducible on target CPU/mobile hardware.
- Report top-1/top-3 on *labeled benchmarks* alongside false-confidence rate, unrecognized/mixed-breed abstention rate, calibration ECE, performance by subgroup, and OOD testing.
- `interpret_breed_scores()` in `bhow_core/breed.py` is a **presentation boundary**, not an evaluated classifier. Its default threshold is illustrative; choose release threshold from validation data with conservative costs for confident errors.
- Display language: `Appearance resembles...`, `Possibly...`, `I couldn't tell confidently`. User corrections must not automatically become ground-truth training data.

## Model/artifact registry per version

`model_id`, model checksum, weights license, dataset provenance/license, label map, preprocessing recipe, hardware runtime, measured p50/p95 latency, training commit, accuracy metrics, calibration, high-risk failure examples, signed release approver, rollback version. A model release is a deployable product change; no silent model updates.

## Food OCR safety gates

Check image MIME by magic bytes, upload size and decompression limits, antivirus scan and EXIF stripping; ensure storage consent. OCR returns *untrusted text*; confirmation screen highlights uncertain terms and retained original photo if consented. Lookups use a reviewed, versioned KB. If OCR fails, offer text input. Do not mix ingredient identification, toxicity, and dietary completeness as one result.

## LLM guardrails (if added at all)

Only explain citations from an approved veterinary KB with version and explicit context. Disallow treatment protocols, drug dosage and implied diagnoses. Require deterministically triggered emergency banners not suppressible by model output. Any summarizer must preserve notes' source labels and known/unknown distinction. Prompt injection in uploaded documents is untrusted content. Evaluate on red-team prompts and vet-labeled scenarios, log only deidentified quality metrics with consent.

## Release criteria before `/integrations/breed/estimate` becomes live

Commercial data and model rights cleared; representative independent test set available; bias and abstention documented; content reviewed by vets; secure upload completed; inference latency p95 and failure monitoring established; rollback exercised; explicit consent and retention documented. Until then endpoint 503 is correct behavior.
