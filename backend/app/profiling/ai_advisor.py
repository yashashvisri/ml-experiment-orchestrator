from typing import Dict, Any
from app.core.config import settings

def generate_ai_dataset_advice(summary: Dict[str, Any], columns: list, target_info: Dict[str, Any]) -> str:
    high_missing = [c["name"] for c in columns if c.get("missing_pct", 0) > 20.0]
    high_outliers = [c["name"] for c in columns if (c.get("outlier_count") or 0) > 10]
    skewed = [c["name"] for c in columns if abs(c.get("skewness") or 0) > 1.5]

    deterministic_advice = []
    deterministic_advice.append("### 🧠 AI Automated Data Quality & Preprocessing Audit")
    
    # Missing values
    if high_missing:
        deterministic_advice.append(f"- **High Missingness Warning:** Columns `{', '.join(high_missing)}` contain >20% null values. Recommend median imputation or drop if redundant.")
    else:
        deterministic_advice.append("- **Completeness:** Dataset exhibits excellent completeness with low overall missing rates.")

    # Skewness
    if skewed:
        deterministic_advice.append(f"- **Distribution Skewness:** Feature(s) `{', '.join(skewed)}` show heavy tail skew. Consider applying log(1+x) or Box-Cox transformation.")

    # Outliers
    if high_outliers:
        deterministic_advice.append(f"- **Outlier Detection:** Detected substantial IQR outliers in `{', '.join(high_outliers)}`. Tree-based models (XGBoost/LightGBM) will naturally resist these, while linear models require robust scaling.")

    # Task & Modeling
    task = target_info.get("task_type", "ML")
    target = target_info.get("target_column", "Target")
    deterministic_advice.append(f"- **Modeling Recommendation:** Detected candidate target `{target}` ({task}). Recommended baseline: Optuna-tuned LightGBM or Random Forest with Stratified/K-Fold validation.")

    if not settings.GEMINI_API_KEY:
        return "\n".join(deterministic_advice)

    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.messages import HumanMessage, SystemMessage
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2, google_api_key=settings.GEMINI_API_KEY)
        sys_msg = SystemMessage(content="You are a Principal AI Data Scientist. Provide a concise, bulleted EDA assessment and specific feature engineering recommendations for this dataset.")
        prompt = f"Dataset Summary: {summary}\nTarget: {target_info}\nIssues: Missing={high_missing}, Skewed={skewed}, Outliers={high_outliers}"
        res = llm.invoke([sys_msg, HumanMessage(content=prompt)])
        return "\n".join(deterministic_advice) + "\n\n### 🤖 Gemini Advanced Insights\n" + res.content
    except Exception:
        return "\n".join(deterministic_advice)
