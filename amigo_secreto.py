import csv
from pathlib import Path

import pandas as pd
import streamlit as st

# ---------- CONFIGURACIÓN ----------
ARCHIVO_APORTES = Path("aportes.csv")
IMAGEN_PORTADA = "portada_posada.jpeg"

# Lista fija de participantes
PARTICIPANTES = [
    "Katherine Silvestre", "Marden Ferruzo", "Rocio Dominguez", "George Aliaga",
    "Janet Rivera", "Ana Raez", "Israel Juarez", "Luis Moreano", "Yessevel Calvo",
    "Yelitza Arias", "Eduardo Pinto", "Millary Antunez", "Manuel Reyes",
    "Vladimir Tucto", "Rocio Arango", "Axel Fuentes", "Camila Alva",
    "Ricardo Céspedes",
]

# Listas por categoría
LISTA_PIQUEOS = [
    "Alfajores", "Petipan de pollo", "Empanaditas surtidas", "Cheetos y chizitos",
    "Waffers y dulces", "Minitriples de jamón y queso", "Tamal",
    "Papás, chifles, camotes y chifles", "Otro (indicar)",
]

LISTA_BEBIDAS_ALC = ["Ninguna", "Pisco", "Cerveza", "Vino", "Ron", "Otro (indicar)"]

LISTA_BEBIDAS_NO_ALC = ["Ninguna", "Gaseosa", "Everest", "Agua", "Hielo", "Limón", "Otro (indicar)"]


# ---------- FUNCIONES AUXILIARES ----------
def cargar_aportes():
    if ARCHIVO_APORTES.exists():
        return pd.read_csv(ARCHIVO_APORTES, dtype=str)
    else:
        return pd.DataFrame(columns=[
            "nombre", "piqueo", "cant_piqueo",
            "bebida_alcoholica", "cant_bebida_alcoholica",
            "bebida_no_alcoholica", "cant_bebida_no_alcoholica"
        ])


def guardar_aportes(df_aportes):
    df_aportes.to_csv(ARCHIVO_APORTES, index=False, encoding="utf-8")


# ---------- APP ----------
def main():
    st.set_page_config(
        page_title="Aportes Posada Territorial 2025",
        page_icon="🎄",
        layout="centered",
    )

    # Estilos visuales
    st.markdown(
        """
        <style>
html, body, [data-testid="stAppViewContainer"], .stApp {
    color-scheme: light !important;
}
.stApp {
    background: linear-gradient(180deg, #fff7f0 0%, #ffffff 40%);
}
.card {
    background-color: #ffffff;
    padding: 1.2rem 1rem;
    border-radius: 0.8rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border: 1px solid #f0e0d2;
}
.titulo {
    font-size: 2.1rem; font-weight:700; text-align:center; color:#234;
}
.subtitulo {
    text-align:center; font-size:1rem; color:#555;
}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Portada
    if Path(IMAGEN_PORTADA).exists():
        st.image(IMAGEN_PORTADA, use_column_width=True)

    st.markdown('<div class="titulo">🎄 Aportes Posada Territorial 2025 🎁</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo">Registra tu piqueo y tus bebidas para organizar mejor la mesa ✨</div>', unsafe_allow_html=True)

    # Aviso importante
    st.markdown(
        """
        <div style="
            background-color:#fff2e6;
            padding:12px 18px;
            border-radius:8px;
            border:1px solid #f5c09a;
            font-size:0.95rem;
            color:#5a3c2c;
            margin-top:10px;
            text-align:justify;">
            ⚠️ <strong>Aviso importante:</strong><br>
            Teniendo en cuenta que somos <strong>18 personas</strong>, sería ideal que, en la medida de lo posible,
            los productos puedan traerse en sus <strong>presentaciones grandes o familiares</strong>,
            para que todos podamos compartir sin problema. 🫶✨
        </div>
        """,
        unsafe_allow_html=True,
    )

    df_aportes = cargar_aportes()

    st.markdown("<br>", unsafe_allow_html=True)

    # Layout columnas
    col_izq, col_der = st.columns([1.2, 0.9])

    # ------------ COLUMNA DERECHA ------------
    with col_der:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📋 Lista de ideas")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Piqueos**")
            for i in LISTA_PIQUEOS:
                st.write(f"- {i}")

        with col2:
            st.markdown("**Bebidas alcohólicas**")
            for i in LISTA_BEBIDAS_ALC[1:]:
                st.write(f"- {i}")

        with col3:
            st.markdown("**Bebidas no alcohólicas**")
            for i in LISTA_BEBIDAS_NO_ALC[1:]:
                st.write(f"- {i}")

        st.markdown('</div>', unsafe_allow_html=True)

    # ------------ COLUMNA IZQUIERDA (FORM) ------------
    with col_izq:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📝 Registrar tu aporte")

        with st.form("form_aporte"):

            # Nombre
            nombre = st.selectbox("Selecciona tu nombre:", PARTICIPANTES)

            # PIQUEO
            st.markdown("#### 🧀 Piqueo")
            piqueo_sel = st.radio("¿Qué piqueo vas a llevar?", LISTA_PIQUEOS)
            piqueo_otro = ""
            if piqueo_sel == "Otro (indicar)":
                piqueo_otro = st.text_input("Indica el piqueo")
            cant_piqueo = st.number_input("Cantidad de piqueo:", min_value=0, step=1)

            # BEBIDA ALCOHÓLICA
            st.markdown("#### 🍷 Bebida alcohólica (opcional)")
            beb_alc_sel = st.radio("Elige una:", LISTA_BEBIDAS_ALC)
            beb_alc_otro = ""
            if beb_alc_sel == "Otro (indicar)":
                beb_alc_otro = st.text_input("Especifica la bebida alcohólica")
            cant_beb_alc = st.number_input("Cantidad:", min_value=0, step=1, key="alc")

            # BEBIDA NO ALCOHÓLICA
            st.markdown("#### 🥤 Bebida no alcohólica (opcional)")
            beb_noalc_sel = st.radio("Elige una:", LISTA_BEBIDAS_NO_ALC)
            beb_noalc_otro = ""
            if beb_noalc_sel == "Otro (indicar)":
                beb_noalc_otro = st.text_input("Especifica la bebida no alcohólica")
            cant_beb_noalc = st.number_input("Cantidad:", min_value=0, step=1, key="no_alc")

            enviado = st.form_submit_button("✅ Registrar aporte")

        # ------------ PROCESAR ENVÍO ------------
        if enviado:

            # Evitar duplicado
            if nombre in df_aportes["nombre"].values:
                st.error("Ya registraste tu aporte antes.")
                st.stop()

            # Resolver textos
            piqueo_final = piqueo_otro if piqueo_sel == "Otro (indicar)" else piqueo_sel

            if pib := beb_alc_sel == "Otro (indicar)":
                beb_alc_final = beb_alc_otro
            else:
                beb_alc_final = "" if beb_alc_sel == "Ninguna" else beb_alc_sel

            if beb_noalc_sel == "Otro (indicar)":
                beb_noalc_final = beb_noalc_otro
            else:
                beb_noalc_final = "" if beb_noalc_sel == "Ninguna" else beb_noalc_sel

            # Validaciones
            if cant_piqueo <= 0:
                st.error("Indica la cantidad de piqueo (mayor a 0).")
                st.stop()

            if beb_alc_final and cant_beb_alc <= 0:
                st.error("Si llevas bebida alcohólica, indica la cantidad.")
                st.stop()

            if beb_noalc_final and cant_beb_noalc <= 0:
                st.error("Si llevas bebida no alcohólica, indica la cantidad.")
                st.stop()

            # Guardar
            nuevo = {
                "nombre": nombre,
                "piqueo": piqueo_final,
                "cant_piqueo": cant_piqueo,
                "bebida_alcoholica": beb_alc_final,
                "cant_bebida_alcoholica": cant_beb_alc,
                "bebida_no_alcoholica": beb_noalc_final,
                "cant_bebida_no_alcoholica": cant_beb_noalc,
            }

            df_aportes = pd.concat([df_aportes, pd.DataFrame([nuevo])], ignore_index=True)
            guardar_aportes(df_aportes)

            st.success("¡Aporte registrado correctamente! 🎉")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Mostrar aportes
    if not df_aportes.empty:
        st.subheader("📋 Aportes registrados")

        df_mostrar = df_aportes.rename(columns={
            "nombre": "Nombre",
            "piqueo": "Piqueo",
            "cant_piqueo": "Cantidad piqueo",
            "bebida_alcoholica": "Bebida alcohólica",
            "cant_bebida_alcoholica": "Cantidad beb. alcohólica",
            "bebida_no_alcoholica": "Bebida no alcohólica",
            "cant_bebida_no_alcoholica": "Cantidad beb. no alcohólica",
        })

        df_mostrar = df_mostrar.sort_values("Nombre").reset_index(drop=True)
        st.dataframe(df_mostrar, use_container_width=True)

        # Faltantes
        registrados = set(df_aportes["nombre"])
        faltan = [p for p in PARTICIPANTES if p not in registrados]
        if faltan:
            st.warning("Faltan registrar: " + ", ".join(faltan))
        else:
            st.success("🎉 ¡Todos ya registraron su aporte!")


if __name__ == "__main__":
    main()