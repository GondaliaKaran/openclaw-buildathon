"""
Web Report Dashboard for Vendor Evaluation Agent
Serves beautiful interactive reports with PDF export
"""
import os
import json
import asyncio
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "vendor-eval-secret-key")

# Store reports in memory + disk
REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# In-memory cache
reports_cache = {}


def load_reports():
    """Load all saved reports from disk."""
    for f in REPORTS_DIR.glob("*.json"):
        try:
            data = json.loads(f.read_text())
            reports_cache[f.stem] = data
        except Exception:
            pass


def save_report(report_id, data):
    """Save report to disk and cache."""
    reports_cache[report_id] = data
    (REPORTS_DIR / f"{report_id}.json").write_text(json.dumps(data, indent=2))


def generate_report_id(query):
    """Generate a short unique ID for a report."""
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    h = hashlib.md5(f"{query}{ts}".encode()).hexdigest()[:6]
    return f"eval-{ts}-{h}"


@app.route("/")
def index():
    """Dashboard home — list all reports."""
    load_reports()
    reports_list = []
    for rid, rdata in reports_cache.items():
        candidates = rdata.get("candidates", [])
        rec = rdata.get("recommendation", {})
        created = rdata.get("created_at", "")
        try:
            date_str = datetime.fromisoformat(created).strftime("%b %d, %Y %H:%M")
        except Exception:
            date_str = created[:10] if created else "—"
        reports_list.append({
            "id": rid,
            "query": rdata.get("query", "Untitled evaluation"),
            "date": date_str,
            "candidates_count": len(candidates),
            "winner": rec.get("primary", ""),
            "status": rdata.get("status", "pending"),
        })
    reports_list.sort(key=lambda x: x["date"], reverse=True)
    return render_template("index.html", reports=reports_list)


@app.route("/report/<report_id>")
def view_report(report_id):
    """View a single evaluation report."""
    load_reports()
    report = reports_cache.get(report_id)
    if not report:
        return render_template("404.html"), 404
    return render_template("report.html", report=report, report_id=report_id)


@app.route("/api/reports", methods=["POST"])
def create_report():
    """API endpoint to create a new report (called by agent or CLI)."""
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    report_id = generate_report_id(data.get("query", "unknown"))
    data["report_id"] = report_id
    data["created_at"] = datetime.now().isoformat()

    save_report(report_id, data)

    base_url = request.host_url.rstrip("/")
    return jsonify({
        "id": report_id,
        "report_id": report_id,
        "url": f"{base_url}/report/{report_id}",
        "message": "Report created successfully"
    }), 201


@app.route("/api/reports/<report_id>", methods=["GET"])
def get_report_api(report_id):
    """API endpoint to fetch report data."""
    load_reports()
    report = reports_cache.get(report_id)
    if not report:
        return jsonify({"error": "Report not found"}), 404
    return jsonify(report)


@app.route("/api/reports", methods=["GET"])
def list_reports_api():
    """API endpoint to list all reports."""
    load_reports()
    return jsonify({
        "reports": [
            {
                "id": rid,
                "query": r.get("query", ""),
                "created_at": r.get("created_at", ""),
                "recommendation": r.get("recommendation", {}).get("primary", "")
            }
            for rid, r in sorted(
                reports_cache.items(),
                key=lambda x: x[1].get("created_at", ""),
                reverse=True
            )
        ]
    })


@app.route("/new", methods=["GET", "POST"])
def new_evaluation():
    """Form to submit a new evaluation query."""
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if not query:
            return render_template("new.html", error="Please enter an evaluation query")

        # Create a placeholder report
        report_id = generate_report_id(query)
        data = {
            "report_id": report_id,
            "query": query,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "message": "Submit this query to the Telegram/Slack bot to generate the full report."
        }
        save_report(report_id, data)
        return redirect(url_for("view_report", report_id=report_id))

    return render_template("new.html")


# --- Demo report for testing ---
@app.route("/demo")
def demo_report():
    """Generate a demo report to showcase the UI."""
    demo_data = {
        "report_id": "demo-001",
        "query": "evaluate payment gateways for Indian startup with 10K transactions/month",
        "status": "complete",
        "created_at": datetime.now().isoformat(),
        "context": {
            "tech_stack": "Python / React / AWS",
            "domain": "Fintech Startup",
            "region": "India",
            "scale": "~10,000 transactions/month",
            "stated_priorities": "UPI support, low MDR, fast onboarding",
            "inferred_priorities": "RBI compliance, payment success rates, settlement speed, webhooks/recon"
        },
        "candidates": [
            {"name": "Razorpay", "rationale": "Market leader for Indian startups; broad payment method coverage + strong compliance positioning"},
            {"name": "Cashfree Payments", "rationale": "Claims industry-leading success rates via in-house UPI/card switches + smart routing"},
            {"name": "PayU", "rationale": "Large incumbent; wide payment-mode coverage (150+ modes); often used as backup gateway"},
            {"name": "PhonePe Payment Gateway", "rationale": "UPI-first approach; aggressive pricing offers; strong if UPI is dominant payment method"}
        ],
        "discoveries": [
            {
                "title": "Razorpay Claims PCI DSS + ISO 27001 + GDPR Compliance",
                "evidence": "Razorpay homepage: '100% PCI DSS, GDPR compliant and ISO 27001 certified' (razorpay.com)",
                "why_it_matters": "Even at 10K tx/mo, startups need credible security posture for investors and partners. Explicit compliance claims are a discriminator.",
                "weight_shift": "RBI/PCI Compliance: 20% → 28% (+8)",
                "triggered": "Verified compliance pages for Cashfree, PayU, PhonePe — found Cashfree's security page returned 403"
            },
            {
                "title": "Cashfree In-House Switches Enable Higher Success Rates",
                "evidence": "Cashfree homepage: 'Industry-leading success rates via in-house card and UPI switches, AI-driven smart routing' (cashfree.com)",
                "why_it_matters": "At 10K tx/mo, even 2-3% higher success rates = 200-300 extra successful transactions/month. For UPI-heavy India startup this is critical.",
                "weight_shift": "Payment Success Rate: 20% → 28% (+8)",
                "triggered": "Searched for objective success-rate benchmarks across all 4 vendors; checked status pages for UPI-specific incidents"
            },
            {
                "title": "Promo Pricing is Widespread — Steady-State MDR Unclear",
                "evidence": "Cashfree: '1.6% gateway fee for new merchants – limited period' (cashfree.com). PhonePe: '1.95% FREE — Limited Period Offer' (business.phonepe.com). Razorpay pricing page redirected to US pricing.",
                "why_it_matters": "Promo pricing misleads cost projections. At 10K tx/mo with avg ₹500 ticket, difference between 1.6% and 2.5% MDR = ₹45,000/month.",
                "weight_shift": "Pricing/MDR: 10% → 20% (+10)",
                "triggered": "Calculated cost projections at current, 3x, and 10x scale for each vendor; flagged FX risk for any USD-billing vendor"
            }
        ],
        "weights": {
            "before": {
                "RBI/PCI Compliance": 20,
                "Payment Success Rate": 20,
                "UPI/Local Methods": 15,
                "Settlement Terms": 10,
                "Pricing/MDR": 10,
                "Webhook/Recon Quality": 10,
                "Support Escalation": 10,
                "Vendor Health": 5
            },
            "after": {
                "RBI/PCI Compliance": 28,
                "Payment Success Rate": 28,
                "UPI/Local Methods": 10,
                "Settlement Terms": 6,
                "Pricing/MDR": 20,
                "Webhook/Recon Quality": 4,
                "Support Escalation": 2,
                "Vendor Health": 2
            },
            "reasons": {
                "RBI/PCI Compliance": "Razorpay explicit PCI/ISO claim — compliance is a real discriminator",
                "Payment Success Rate": "Cashfree in-house switches claim — success rates directly impact revenue",
                "UPI/Local Methods": "All vendors cover UPI adequately — less differentiating",
                "Settlement Terms": "No concrete settlement data found — deprioritized",
                "Pricing/MDR": "Promo pricing widespread — true costs unclear, needs extra diligence",
                "Webhook/Recon Quality": "Could verify SDK existence but not recon quality",
                "Support Escalation": "No verifiable SLA data — deprioritized",
                "Vendor Health": "No concerning signals found — kept minimal"
            }
        },
        "scorecard": {
            "criteria": ["RBI/PCI Compliance (28%)", "Payment Success Rate (28%)", "UPI/Local Methods (10%)", "Settlement Terms (6%)", "Pricing/MDR (20%)", "Webhook/Recon (4%)", "Support (2%)", "Vendor Health (2%)"],
            "vendors": {
                "Razorpay": {
                    "scores": [8, 7, 7, 5, 5, 7, 5, 6],
                    "notes": ["PCI DSS + ISO 27001 claimed", "No public success metrics", "UPI/RuPay/Netbanking/Cards", "Unable to verify T+X", "Pricing redirected to US page", "Python SDK with retry support", "Unable to verify SLA", "SDK actively maintained"],
                    "weighted_total": 6.4
                },
                "Cashfree": {
                    "scores": [6, 8, 8, 5, 7, 6, 5, 6],
                    "notes": ["Security page blocked (403)", "In-house switches + smart routing", "180+ ways to pay", "Unable to verify", "1.6% promo (limited period)", "Python SDK exists", "Unable to verify", "SDK repo active"],
                    "weighted_total": 6.9
                },
                "PayU": {
                    "scores": [5, 6, 8, 5, 5, 5, 5, 5],
                    "notes": ["No evidence pulled", "Claims 'highest success rates'", "150+ payment modes", "Unable to verify", "No concrete fee schedule", "No SDK evidence", "Unable to verify", "Large incumbent"],
                    "weighted_total": 5.7
                },
                "PhonePe PG": {
                    "scores": [5, 7, 7, 5, 6, 5, 5, 5],
                    "notes": ["No evidence pulled", "Claims 'unmatched success rates'", "PG broadly supported", "Unable to verify", "1.95% FREE — limited promo", "No SDK evidence", "Unable to verify", "Large platform"],
                    "weighted_total": 5.9
                }
            }
        },
        "hidden_risks": {
            "maintainer_health": [
                {"vendor": "Razorpay", "status": "check", "detail": "Python SDK exists (github.com/razorpay/razorpay-python) — commit recency not verified in this run"},
                {"vendor": "Cashfree", "status": "check", "detail": "Python SDK exists (github.com/cashfree/cashfree-pg-sdk-python) — commit recency not verified"}
            ],
            "pricing_traps": [
                {"vendor": "Cashfree", "status": "warning", "detail": "1.6% is promotional — steady-state MDR may be 2%+. Get method-wise MDR in writing."},
                {"vendor": "PhonePe PG", "status": "warning", "detail": "1.95% FREE is limited offer — post-promo pricing unknown. Confirm expiry terms."}
            ],
            "vendor_lockin": [
                {"vendor": "All", "status": "info", "detail": "Standard PG lock-in: webhook formats, settlement reports, dispute flows differ. Abstract via payment service layer."}
            ],
            "acquisition_risk": [
                {"vendor": "PayU", "status": "check", "detail": "Parent company Prosus has restructured fintech division — monitor roadmap commitments."}
            ],
            "compliance_drift": [
                {"vendor": "Razorpay", "status": "info", "detail": "Claims compliance on homepage — request actual audit letters/attestations for PCI scope."}
            ],
            "tech_deprecation": [
                {"vendor": "All", "status": "ok", "detail": "No deprecation notices found. Ask about API versioning and backward compatibility policies."}
            ]
        },
        "cost_projection": {
            "scale_labels": ["10K tx/mo (₹500 avg)", "30K tx/mo (3×)", "100K tx/mo (10×)"],
            "vendors": {
                "Razorpay": {"costs": ["₹1,00,000", "₹3,00,000", "₹10,00,000"], "risk": "Pricing page redirected to US — verify India MDR"},
                "Cashfree": {"costs": ["₹80,000", "₹2,40,000", "₹8,00,000"], "risk": "Promo rate 1.6% — may increase after onboarding"},
                "PayU": {"costs": ["₹1,00,000", "₹3,00,000", "₹10,00,000"], "risk": "No concrete MDR found — estimate based on industry avg"},
                "PhonePe PG": {"costs": ["₹97,500", "₹2,92,500", "₹9,75,000"], "risk": "1.95% FREE promo — post-promo pricing unknown"}
            }
        },
        "recommendation": {
            "primary": "Cashfree Payments",
            "primary_score": 6.9,
            "primary_reasons": [
                "Highest success rate positioning via in-house UPI/card switches (cashfree.com)",
                "Broadest method coverage: 180+ payment modes including UPI, cards, netbanking",
                "Most competitive promo pricing at 1.6% (verify steady-state MDR before committing)"
            ],
            "primary_tradeoffs": [
                "Promo pricing may not reflect long-term MDR — but at 10K tx/mo you can renegotiate or switch"
            ],
            "backup": "Razorpay",
            "backup_score": 6.4,
            "backup_reason": "Strong compliance positioning (PCI/ISO) + mature ecosystem + widely used Python SDK",
            "conditional": "If UPI is >80% of volume → pilot PhonePe PG as secondary rail for UPI-specific success rates",
            "conditional_reason": "PhonePe heavily optimized for UPI flows — may outperform on UPI-specific success rates"
        },
        "reproducibility": {
            "date": "2026-02-28",
            "sources_count": 12,
            "vendors_count": 4,
            "sources": [
                "razorpay.com — homepage compliance claims",
                "razorpay.com/pricing — redirected to US pricing",
                "github.com/razorpay/razorpay-python — SDK repo",
                "cashfree.com — homepage success rate + promo pricing",
                "github.com/cashfree/cashfree-pg-sdk-python — SDK repo",
                "payu.in — homepage + pricing page",
                "payu.in/pricing — payment modes listed",
                "business.phonepe.com/payment-gateway — PG features + promo"
            ],
            "unable_to_verify": [
                "Cashfree security/compliance page (403 blocked)",
                "India-specific MDR for Razorpay (pricing redirected to US)",
                "Objective uptime/incident history for all vendors",
                "Support SLAs and escalation terms",
                "Settlement timelines (T+X days)"
            ]
        }
    }
    save_report("demo-001", demo_data)
    return redirect(url_for("view_report", report_id="demo-001"))


if __name__ == "__main__":
    load_reports()
    port = int(os.getenv("REPORT_PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
