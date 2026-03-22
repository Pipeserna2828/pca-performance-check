import os
from pathlib import Path
from typing import Any

import requests
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "assets" / "sistecredito_color.png"
BACKEND_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")

st.set_page_config(
    page_title="PCA Performance Check",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        html, body, [data-testid="stAppViewContainer"], .stApp {
            background: #f6f8fc !important;
            color: #0f172a !important;
        }

        [data-testid="stHeader"], [data-testid="stToolbar"] {
            background: transparent !important;
        }

        [data-testid="stSidebar"] {
            display: none !important;
        }

        .block-container {
            max-width: 980px;
            padding-top: 1rem;
            padding-bottom: 2rem;
        }

        h1, h2, h3, h4, h5, h6, p, label, div, span, li {
            color: #0f172a;
        }

        .app-card {
            background: #ffffff;
            border: 1px solid #d9e2ef;
            border-radius: 16px;
            padding: 1rem 1.15rem;
            margin-bottom: 1rem;
        }

        .app-title {
            color: #003090;
            font-size: 1.7rem;
            font-weight: 800;
            margin: 0 0 0.2rem 0;
        }

        .app-subtitle {
            color: #475569;
            font-size: 0.95rem;
            margin: 0;
        }

        .section-card {
            background: #ffffff;
            border: 1px solid #d9e2ef;
            border-radius: 16px;
            padding: 1rem 1.1rem;
            margin-bottom: 1rem;
        }

        .section-title {
            color: #0f172a;
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .section-helper {
            color: #475569;
            font-size: 0.9rem;
            margin-bottom: 0.9rem;
        }

        .metric-card {
            background: #ffffff;
            border: 1px solid #d9e2ef;
            border-radius: 14px;
            padding: 0.95rem;
            min-height: 112px;
        }

        .metric-label {
            color: #475569;
            font-size: 0.76rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }

        .metric-value {
            color: #0f172a;
            font-size: 1.45rem;
            font-weight: 800;
            line-height: 1.1;
            margin-top: 0.25rem;
        }

        .metric-helper {
            color: #475569;
            font-size: 0.84rem;
            margin-top: 0.45rem;
            line-height: 1.35;
        }

        .metric-center {
            display: flex;
            min-height: 42px;
            align-items: center;
            justify-content: center;
            margin-top: 0.2rem;
            margin-bottom: 0.4rem;
        }

        .pill {
            display: inline-block;
            padding: 0.34rem 0.7rem;
            border-radius: 999px;
            font-weight: 700;
            font-size: 0.82rem;
            border: 1px solid transparent;
            text-align: center;
        }

        .pill-ready { background: rgba(64,208,32,0.14); color: #166534; border-color: rgba(22,101,52,0.12); }
        .pill-gaps { background: rgba(250,204,21,0.20); color: #854d0e; border-color: rgba(133,77,14,0.14); }
        .pill-blocked { background: rgba(239,68,68,0.14); color: #991b1b; border-color: rgba(153,27,27,0.14); }
        .pill-high { background: rgba(239,68,68,0.14); color: #991b1b; border-color: rgba(153,27,27,0.14); }
        .pill-medium { background: rgba(245,158,11,0.16); color: #92400e; border-color: rgba(146,64,14,0.14); }
        .pill-low { background: rgba(59,130,246,0.12); color: #1d4ed8; border-color: rgba(29,78,216,0.14); }

        .request-id-box {
            background: #f8fafc;
            border: 1px dashed #c9d5e6;
            border-radius: 12px;
            padding: 0.8rem 0.9rem;
            color: #0f172a;
            font-family: Consolas, monospace;
            font-size: 0.92rem;
            margin-top: 0.8rem;
        }

        .list-box {
            background: #ffffff;
            border: 1px solid #d9e2ef;
            border-radius: 12px;
            padding: 0.8rem 0.9rem;
            margin-bottom: 0.6rem;
            color: #0f172a;
        }

        .source-note {
            display: inline-block;
            padding: 0.24rem 0.55rem;
            border-radius: 999px;
            font-size: 0.74rem;
            font-weight: 600;
            color: #475569;
            background: #f8fafc;
            border: 1px solid #d9e2ef;
            margin-bottom: 0.65rem;
        }

        .summary-box, .assistant-box {
            background: #f8fafc;
            border: 1px solid #d9e2ef;
            border-radius: 12px;
            padding: 0.95rem 1rem;
            color: #0f172a;
        }

        .assistant-box {
            background: #eefbf0;
            border-color: #b7e4c0;
            margin-bottom: 0.8rem;
        }

        .assistant-step {
            background: #ffffff;
            border: 1px solid #d9e2ef;
            border-radius: 12px;
            padding: 0.75rem 0.85rem;
            margin-bottom: 0.55rem;
            color: #0f172a;
        }

        .section-label {
            color: #003090;
            font-size: 0.95rem;
            font-weight: 700;
            margin: 1rem 0 0.55rem 0;
        }

        div[data-testid="stCheckbox"] > label p,
        div[data-testid="stTextInput"] label p,
        div[data-testid="stSelectbox"] label p,
        div[data-testid="stNumberInput"] label p,
        div[data-testid="stTextArea"] label p {
            color: #0f172a !important;
            font-weight: 500 !important;
        }

        div[data-baseweb="input"] {
            background: #ffffff !important;
            border-radius: 10px !important;
            border: 1px solid #d9e2ef !important;
        }

        div[data-baseweb="input"] input {
            background: #ffffff !important;
            color: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
        }

        div[data-baseweb="select"] > div {
            background: #ffffff !important;
            color: #0f172a !important;
            border-radius: 10px !important;
            border: 1px solid #d9e2ef !important;
        }

        div[data-baseweb="select"] span,
        div[data-baseweb="select"] svg,
        div[data-baseweb="select"] input {
            color: #0f172a !important;
            fill: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
        }

        div[data-testid="stNumberInput"] button {
            background: #ffffff !important;
            color: #0f172a !important;
            border: 1px solid #d9e2ef !important;
        }

        textarea {
            background: #ffffff !important;
            color: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
            border: 1px solid #d9e2ef !important;
            border-radius: 10px !important;
        }

        ul[role="listbox"],
        ul[role="listbox"] li,
        div[role="listbox"],
        div[role="option"] {
            background: #ffffff !important;
            color: #0f172a !important;
        }

        [data-baseweb="popover"] *,
        [data-baseweb="menu"] *,
        [role="listbox"] *,
        [role="option"] * {
            color: #0f172a !important;
            background: #ffffff !important;
            fill: #0f172a !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def post(path: str, payload: dict | None = None) -> dict[str, Any]:
    response = requests.post(f"{BACKEND_URL}{path}", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def get(path: str) -> dict[str, Any]:
    response = requests.get(f"{BACKEND_URL}{path}", timeout=30)
    response.raise_for_status()
    return response.json()


def safe_request(operation: str, callback):
    try:
        return callback(), None
    except requests.exceptions.RequestException as exc:
        return None, f"No fue posible {operation}: {exc}"
    except Exception as exc:  # pragma: no cover
        return None, f"Ocurrió un error durante {operation}: {exc}"


def decision_class(decision: str) -> str:
    return {
        "LISTA": "pill-ready",
        "LISTA CON BRECHAS": "pill-gaps",
        "NO LISTA": "pill-blocked",
    }.get(decision, "pill-gaps")


def risk_class(level: str) -> str:
    return {
        "ALTO": "pill-high",
        "MEDIO": "pill-medium",
        "BAJO": "pill-low",
    }.get(level, "pill-medium")


def render_pill(text: str, css_class: str) -> str:
    return f'<span class="pill {css_class}">{text}</span>'


def render_metric(label: str, value_html: str, helper: str, centered: bool = False) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="{'metric-center' if centered else 'metric-value'}">{value_html}</div>
            <div class="metric-helper">{helper}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def score_message(score: int) -> str:
    if score >= 85:
        return "Buen nivel de alistamiento para avanzar."
    if score >= 65:
        return "Puede avanzar, pero todavía tiene brechas."
    return "Aún no tiene el alistamiento mínimo requerido."


def format_breakdown_key(key: str) -> str:
    mapping = {
        "demanda_esperada_definida": "Demanda esperada definida",
        "objetivo_p95_definido": "Objetivo p95 definido",
        "ambiente_estable_disponible": "Ambiente estable disponible",
        "observabilidad_disponible": "Observabilidad disponible",
        "baseline_previo_disponible": "Línea base previa disponible",
        "dependencias_externas_identificadas": "Dependencias externas identificadas",
        "descripcion_clara_del_cambio": "Descripción clara del cambio",
        # compatibilidad si quedan resultados viejos en el JSON
        "expected_demand_defined": "Demanda esperada definida",
        "target_p95_defined": "Objetivo p95 definido",
        "stable_environment_available": "Ambiente estable disponible",
        "observability_available": "Observabilidad disponible",
        "baseline_available": "Línea base previa disponible",
        "external_dependencies_identified": "Dependencias externas identificadas",
        "clear_change_description": "Descripción clara del cambio",
    }
    return mapping.get(key, key.replace("_", " ").capitalize())


st.session_state.setdefault("request_id", "")
st.session_state.setdefault("result", None)

if LOGO_PATH.exists():
    st.image(str(LOGO_PATH), width=180)

st.markdown(
    """
    <div class="app-card">
        <div class="app-title">PCA Performance Check</div>
        <p class="app-subtitle">Registra una solicitud y visualiza el resultado del análisis en una sola vista.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

form_col, result_col = st.columns([1, 1.05], gap="large")

with form_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Solicitud</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-helper">Completa solo la información necesaria para el análisis.</div>', unsafe_allow_html=True)

    with st.form("analysis_form", clear_on_submit=False):
        system_name = st.text_input("Nombre del sistema", value="Credinet Credit API")

        row_1 = st.columns(2)
        with row_1[0]:
            component_type = st.selectbox("Tipo de componente", ["API", "BATCH", "WORKER", "QUEUE_CONSUMER"])
        with row_1[1]:
            service_criticality = st.selectbox("Criticidad", ["LOW", "MEDIUM", "HIGH", "CRITICAL"], index=3)

        row_2 = st.columns(2)
        with row_2[0]:
            change_type = st.selectbox("Tipo de cambio", ["UI", "BACKEND", "DATABASE", "INTEGRATION", "INFRASTRUCTURE"], index=1)
        with row_2[1]:
            target_p95_ms = st.number_input("Objetivo p95 (ms)", min_value=1, value=500, step=50)

        row_3 = st.columns(2)
        with row_3[0]:
            expected_demand_value = st.number_input("Demanda esperada", min_value=1.0, value=120.0, step=10.0)
        with row_3[1]:
            expected_demand_unit = st.selectbox("Unidad de demanda", ["TPS", "TX_HOUR", "CONCURRENT_USERS"], index=2)

        st.markdown('<div class="section-label">Prerequisitos técnicos</div>', unsafe_allow_html=True)
        flags_1 = st.columns(2)
        with flags_1[0]:
            stable_environment_available = st.checkbox("Ambiente estable disponible", value=True)
        with flags_1[1]:
            observability_available = st.checkbox("Observabilidad disponible", value=True)

        flags_2 = st.columns(2)
        with flags_2[0]:
            baseline_available = st.checkbox("Baseline previo disponible", value=False)
        with flags_2[1]:
            external_dependencies = st.checkbox("Usa dependencias externas", value=True)

        change_description = st.text_area(
            "Descripción breve del cambio",
            value="Actualización de lógica transaccional e integración con servicio externo de scoring.",
            height=110,
        )

        analyze_clicked = st.form_submit_button("Analizar solicitud", type="primary", use_container_width=True)

    if analyze_clicked:
        payload = {
            "system_name": system_name,
            "component_type": component_type,
            "service_criticality": service_criticality,
            "change_type": change_type,
            "expected_demand_value": expected_demand_value,
            "expected_demand_unit": expected_demand_unit,
            "target_p95_ms": target_p95_ms,
            "stable_environment_available": stable_environment_available,
            "observability_available": observability_available,
            "baseline_available": baseline_available,
            "external_dependencies": external_dependencies,
            "change_description": change_description,
        }

        created, error = safe_request("registrar la solicitud", lambda: post("/api/v1/analysis-requests", payload))
        if error:
            st.error(error)
        else:
            request_id = created["request_id"]
            st.session_state["request_id"] = request_id

            executed, error = safe_request(
                "ejecutar el análisis",
                lambda: post(f"/api/v1/analysis-requests/{request_id}/execute"),
            )
            if error:
                st.error(error)
            else:
                result, error = safe_request(
                    "consultar el resultado",
                    lambda: get(f"/api/v1/analysis-requests/{request_id}/result"),
                )
                if error:
                    st.error(error)
                else:
                    st.session_state["result"] = result
                    st.success("Análisis completado correctamente.")

    if st.session_state.get("request_id"):
        st.markdown(
            f'<div class="request-id-box">Request ID: {st.session_state["request_id"]}</div>',
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)

result = st.session_state.get("result")

with result_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Resultado</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-helper">Vista resumida del score, la decisión y la recomendación del motor.</div>', unsafe_allow_html=True)

    if result:
        top_metrics = st.columns(2)
        with top_metrics[0]:
            render_metric("Readiness score", str(result["readiness_score"]), score_message(result["readiness_score"]))
        with top_metrics[1]:
            render_metric("Prueba recomendada", result["recommended_test_type"], "Tipo de prueba sugerido por el motor.")

        bottom_metrics = st.columns(2)
        with bottom_metrics[0]:
            render_metric(
                "Decisión",
                render_pill(result["readiness_decision"], decision_class(result["readiness_decision"])),
                "Estado final del alistamiento.",
                centered=True,
            )
        with bottom_metrics[1]:
            render_metric(
                "Riesgo",
                render_pill(result["risk_level"], risk_class(result["risk_level"])),
                "Nivel de riesgo técnico identificado.",
                centered=True,
            )

        st.markdown('<div class="section-label">Resumen</div>', unsafe_allow_html=True)
        st.markdown('<div class="summary-box">', unsafe_allow_html=True)
        st.write(f"**Requiere pruebas de performance:** {'Sí' if result['requires_performance_testing'] else 'No'}")
        st.write(f"**Generado en:** {result['generated_at']}")
        st.write("**Desglose del score**")
        for key, value in result.get("score_breakdown", {}).items():
            st.write(f"- {format_breakdown_key(key)}: {value}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-label">Brechas y riesgos</div>', unsafe_allow_html=True)
        left_list, right_list = st.columns(2, gap="large")
        with left_list:
            st.write("**Hallazgos de riesgo**")
            if result.get("risk_findings"):
                for item in result["risk_findings"]:
                    st.markdown(f'<div class="list-box">{item}</div>', unsafe_allow_html=True)
            else:
                st.success("No se identificaron hallazgos de riesgo relevantes.")
        with right_list:
            st.write("**Prerequisitos faltantes**")
            if result.get("missing_prerequisites"):
                for item in result["missing_prerequisites"]:
                    st.markdown(f'<div class="list-box">{item}</div>', unsafe_allow_html=True)
            else:
                st.success("La solicitud cuenta con los prerequisitos mínimos del MVP.")

        st.markdown('<div class="section-label">Asistente</div>', unsafe_allow_html=True)
        explanation = result["explanation"]
        source_label = "Foundry" if explanation.get("source") == "azure_openai" else "Fallback local"
        st.markdown(f'<div class="source-note">Fuente de explicación: {source_label}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="assistant-box"><strong>Resumen ejecutivo</strong><br>{explanation["executive_summary"]}</div>',
            unsafe_allow_html=True,
        )
        st.write("**Explicación de la decisión**")
        st.write(explanation["decision_explanation"])
        st.write("**Siguientes pasos sugeridos**")
        for step in explanation["recommended_next_steps"]:
            st.markdown(f'<div class="assistant-step">{step}</div>', unsafe_allow_html=True)
    else:
        st.info("Completa la solicitud y selecciona Analizar solicitud para visualizar aquí el resultado.")

    st.markdown('</div>', unsafe_allow_html=True)
