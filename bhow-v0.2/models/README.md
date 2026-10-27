# Machine learning model registry (contract, not pretend inference)

**There is no trained breed model in this repository.** The FastAPI endpoint intentionally returns 503 until a commercially licensed model has passed the release gates.

Expected future model artifact: `breed-visual-v1.onnx`, SHA-256 digest, label-map.json, calibration report, dataset provenance ledger, bias/failure analysis, latency evaluation, and model card. Use ONNX Runtime behind an inference adapter; the domain interpreter already supports confidence thresholds and abstention, but numerical scores must be calibrated empirically. UI must not treat model outputs as genetic ancestry or make clinical claims.

Food photo recognition is not synonymous with food safety. Start with OCR + manual ingredient confirmation + deterministic knowledge-base lookup. Camera pipeline is deferred until upload security and consent are implemented.
