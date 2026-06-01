"""
Fitness Sentiment Analyzer — Gradio app for Hugging Face Spaces.
Authors: Zain, Usama, Ali
"""
import html
import os

import gradio as gr
from dotenv import load_dotenv

from sentiment.engine import analyze_and_recommend

load_dotenv()

AUTHORS = "Zain, Usama, Ali"

SENTIMENT_COLORS = {
    "Positive": "#22c55e",
    "Neutral": "#eab308",
    "Negative": "#ef4444",
}

CUSTOM_CSS = """
.gradio-container {
    font-family: system-ui, -apple-system, Segoe UI, sans-serif !important;
    max-width: 1100px !important;
    margin: auto;
}
.hero-title {
    text-align: center;
    color: #15803d;
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
}
.hero-sub {
    text-align: center;
    color: #64748b;
    margin-bottom: 1rem;
}
.footer-authors {
    text-align: center;
    color: #94a3b8;
    font-size: 0.9rem;
    margin-top: 1rem;
}
"""


def _format_time(value) -> str:
    if hasattr(value, "strftime"):
        return value.strftime("%Y-%m-%d %H:%M UTC")
    return str(value) if value is not None else "—"


def _history_to_markdown(rows: list[dict], error: str | None = None) -> str:
    if error:
        return f"**Error:** {error}"
    if not rows:
        return "*No saved analyses yet. Run an analysis above first.*"

    lines = [
        "| Time | Name | Text | Sentiment | Workout | Confidence |",
        "|------|------|------|-----------|---------|------------|",
    ]
    for row in rows:
        lines.append(
            "| {time} | {name} | {text} | {sentiment} | {workout} | {confidence} |".format(
                time=_format_time(row.get("time", "")).replace("|", "/"),
                name=str(row.get("name", "—")).replace("|", "/")[:30],
                text=str(row.get("text", "")).replace("|", "/")[:50],
                sentiment=str(row.get("sentiment", "")).replace("|", "/"),
                workout=str(row.get("workout", "")).replace("|", "/")[:40],
                confidence=str(row.get("confidence", "")).replace("|", "/"),
            )
        )
    return "\n".join(lines)


def _load_history_markdown() -> tuple[str, str]:
    from db.mongo import get_recent_history, is_db_configured

    if not is_db_configured():
        return (
            "MongoDB not configured.",
            "*Set MONGODB_URI in Space secrets to enable history.*",
        )
    try:
        rows = get_recent_history(20)
        if not rows:
            return ("No saved analyses yet.", "*History is empty.*")
        return (f"Loaded {len(rows)} analyses.", _history_to_markdown(rows))
    except Exception as exc:
        return ("Could not load history.", f"**Error:** {exc}")


def _badge_html(label: str, confidence: float) -> str:
    color = SENTIMENT_COLORS.get(label, "#64748b")
    return f"""
    <div style="text-align:center;padding:1.25rem;border-radius:16px;
                background:linear-gradient(145deg,{color}22,{color}11);
                border:2px solid {color};">
        <div style="font-size:2rem;font-weight:700;color:{color};">{html.escape(label)}</div>
        <div style="font-size:1.1rem;color:#334155;margin-top:0.35rem;">
            {confidence:.1f}% confidence
        </div>
    </div>
    """


def _scores_chart(scores: dict) -> str:
    bars = []
    for label in ("Negative", "Neutral", "Positive"):
        pct = scores.get(label, 0)
        color = SENTIMENT_COLORS[label]
        bars.append(
            f'<div style="margin:8px 0;">'
            f'<div style="display:flex;justify-content:space-between;font-size:0.9rem;">'
            f"<span>{html.escape(label)}</span><span>{pct:.1f}%</span></div>"
            f'<div style="background:#e2e8f0;border-radius:8px;height:12px;overflow:hidden;">'
            f'<div style="width:{min(pct, 100)}%;height:100%;background:{color};border-radius:8px;"></div>'
            f"</div></div>"
        )
    return "<div>" + "".join(bars) + "</div>"


def _workout_markdown(plan: dict) -> str:
    lines = [
        f"### {plan.get('mode', 'Workout')}",
        plan.get("description", ""),
        "",
        f"**Intensity:** {plan.get('intensity', '—')}  ",
        f"**Rest:** {plan.get('rest_period', '—')}",
        "",
        "| Exercise | Sets | Reps | Notes |",
        "|----------|------|------|-------|",
    ]
    for ex in plan.get("exercises", []):
        lines.append(
            f"| {ex.get('exercise', '')} | {ex.get('sets', '')} | "
            f"{ex.get('reps', '')} | {ex.get('note', '')} |"
        )
    tips = plan.get("tips", [])
    if tips:
        lines.extend(["", "**Tips**", ""])
        lines.extend(f"- {t}" for t in tips)
    return "\n".join(lines)


def _diet_markdown(plan: dict) -> str:
    lines = [
        f"### {plan.get('mode', 'Diet')}",
        plan.get("description", ""),
        "",
        f"**Hydration:** {plan.get('hydration', '—')}",
        "",
    ]
    for meal in plan.get("meals", []):
        foods = ", ".join(meal.get("foods", []))
        lines.append(f"**{meal.get('timing', 'Meal')}** — {foods}")
        if meal.get("macros"):
            lines.append(f"  *{meal['macros']}*")
        lines.append("")
    supp = plan.get("supplements", [])
    if supp:
        lines.append(f"**Supplements:** {', '.join(supp)}")
    if plan.get("key_principle"):
        lines.append(f"\n> {plan['key_principle']}")
    return "\n".join(lines)


def _db_status_message() -> str:
    from db.mongo import is_db_configured

    if is_db_configured():
        return "MongoDB connected."
    return "MongoDB URI not set — history will not persist until you add the secret."


def analyze(text: str, display_name: str):
    text = (text or "").strip()
    if not text:
        return (
            "<p style='color:#ef4444'>Please enter how you're feeling about your workout.</p>",
            "",
            "",
            "",
            "",
            "Enter some text to analyze.",
            _db_status_message(),
        )

    result = analyze_and_recommend(text)
    s = result["sentiment"]
    dominant = s["dominant"]

    badge = _badge_html(dominant, s["confidence_pct"])
    scores_html = _scores_chart(s["scores"])
    processed = f"**Processed text:** `{s.get('processed_text', '')[:500]}`"
    workout_md = _workout_markdown(result["workout_plan"])
    diet_md = _diet_markdown(result["diet_plan"])
    message = f"### Message for you\n\n{result['message']}"

    from db.mongo import is_db_configured, save_analysis

    if is_db_configured():
        try:
            save_analysis(text, result, display_name or None)
            db_note = "Saved to MongoDB."
        except Exception as exc:
            db_note = f"Analysis OK, but database save failed: {exc}"
    else:
        db_note = "MongoDB not configured — analysis only."

    return badge, scores_html, processed, workout_md, diet_md, message, db_note


def load_history():
    status, table_md = _load_history_markdown()
    return table_md, status


def build_ui() -> gr.Blocks:
    with gr.Blocks(
        title=f"Fitness Sentiment Analyzer — {AUTHORS}",
        css=CUSTOM_CSS,
        theme=gr.themes.Soft(primary_hue="green", secondary_hue="emerald"),
    ) as demo:
        gr.HTML(
            f"""
            <div class="hero-title">Fitness Sentiment Analyzer</div>
            <div class="hero-sub">
              English, Roman Urdu, emojis &amp; gym slang — get workout &amp; diet plans instantly.
            </div>
            <div class="hero-sub" style="font-size:0.95rem;">By {html.escape(AUTHORS)}</div>
            """
        )

        db_status = gr.Markdown(_db_status_message())

        with gr.Row():
            with gr.Column(scale=1):
                user_text = gr.Textbox(
                    label="How are you feeling about fitness today?",
                    placeholder="e.g. beast mode activated, hit a new PR today!",
                    lines=4,
                )
                user_name = gr.Textbox(
                    label="Your name (optional)",
                    placeholder="Your name",
                    max_lines=1,
                )
                analyze_btn = gr.Button("Analyze & Get My Plan", variant="primary", size="lg")
            with gr.Column(scale=1):
                sentiment_badge = gr.HTML(label="Sentiment")
                scores_plot = gr.HTML(label="Scores")

        processed_out = gr.Markdown(label="Preprocessing")
        db_note = gr.Textbox(label="Database", interactive=False)

        with gr.Row():
            with gr.Column():
                workout_out = gr.Markdown(label="Workout plan")
            with gr.Column():
                diet_out = gr.Markdown(label="Diet plan")
        message_out = gr.Markdown(label="Motivation")

        gr.Markdown("---")

        with gr.Accordion("Saved history (MongoDB)", open=False):
            gr.Markdown(
                "Expand this section, then click **Load history**. "
                "History is on the same page so the app stays stable."
            )
            load_history_btn = gr.Button("Load history", variant="secondary")
            history_status = gr.Markdown("")
            history_table = gr.Markdown(value="*Click Load history.*")

        gr.HTML(
            f'<div class="footer-authors">Built by <strong>{html.escape(AUTHORS)}</strong></div>'
        )

        analyze_btn.click(
            fn=analyze,
            inputs=[user_text, user_name],
            outputs=[
                sentiment_badge,
                scores_plot,
                processed_out,
                workout_out,
                diet_out,
                message_out,
                db_note,
            ],
        ).then(fn=lambda: _db_status_message(), outputs=db_status)

        load_history_btn.click(
            fn=load_history,
            outputs=[history_table, history_status],
        )

    return demo


if __name__ == "__main__":
    app = build_ui()
    app.launch(
        server_name=os.getenv("GRADIO_SERVER_NAME", "0.0.0.0"),
        server_port=int(os.getenv("GRADIO_SERVER_PORT", "7860")),
    )
