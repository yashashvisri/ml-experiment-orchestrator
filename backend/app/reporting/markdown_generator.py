from typing import Dict, Any
from datetime import datetime

def generate_markdown_report(data: Dict[str, Any], ai_narrative: str = "") -> str:
    proj = data.get("project", {})
    runs = data.get("runs", [])
    datasets = data.get("datasets", [])
    best_run = data.get("best_run")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md = []
    md.append(f"# 📊 AI Experiment & Performance Report")
    md.append(f"**Project:** {proj.get('name', 'N/A')}")
    md.append(f"**Generated At:** {now_str}")
    md.append(f"**Executive Overview:** {proj.get('description', '')}\n")
    md.append("---")

    md.append("## 📁 Datasets Overview")
    if datasets:
        md.append("| Dataset Name | File Size (KB) |")
        md.append("| --- | --- |")
        for d in datasets:
            md.append(f"| {d['name']} | {d['size_kb']} KB |")
    else:
        md.append("*No datasets uploaded to this project.*")
    md.append("")

    md.append("## 🧪 ML Runs & Model Performance")
    md.append(f"Total Logged Runs: **{len(runs)}**\n")
    if runs:
        md.append("| Run Name | Experiment | Status | Accuracy / Metric | Params |")
        md.append("| --- | --- | --- | --- | --- |")
        for r in runs:
            acc = r.get("metrics", {}).get("accuracy")
            acc_str = f"{acc:.4f}" if isinstance(acc, (int, float)) else "N/A"
            params_str = ", ".join([f"{k}={v}" for k, v in list(r.get("params", {}).items())[:2]]) or "N/A"
            md.append(f"| {r['name']} | {r['experiment_name']} | {r['status']} | {acc_str} | {params_str} |")
    else:
        md.append("*No runs logged for this experiment yet.*")
    md.append("")

    if best_run:
        md.append("## 🏆 Champion Model")
        acc = best_run.get("metrics", {}).get("accuracy", "N/A")
        md.append(f"- **Champion Run:** {best_run.get('name')}")
        md.append(f"- **Accuracy:** {acc}")
        md.append(f"- **Parameters:** {best_run.get('params')}\n")

    if ai_narrative:
        md.append("## 🤖 AI Data Scientist Insights & Recommendations")
        md.append(ai_narrative)
        md.append("")

    md.append("---")
    md.append("*Generated automatically by ML Experiment Orchestrator.*")
    return "\n".join(md)
