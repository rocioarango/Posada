import csv
from pathlib import Path

import pandas as pd
import streamlit as st

# ---------- CONFIGURACIÓN ----------
ARCHIVO_APORTES = Path("aportes.csv")

IMAGEN_PORTADA = "portada_posada.jpeg"  # cambia el nombre si quieres

# Participantes
PARTICIPANTES = [
    "Katherine Silvestre",
    "Marden Ferruzo",
    "Rocio Dominguez",
    "George Aliaga",
    "Janet Rivera",
    "Ana Raez",
    "Israel Juarez",
    "Luis Moreano",
    "Yessevel Calvo",
    "Yelitza Arias",
    "Eduardo Pinto",
    "Millary Antunez",
    "Manuel Reyes",
    "Vladimir Tucto",
    "Rocio Arango",
    "Axel Fuentes",
    "Camila Alva",
    "Ricardo Céspedes",
]

# Listas por categoría
LISTA_PIQUEOS = [
    "Alfajores",
    "Petipan de pollo",
    "Empanaditas surtidas",
    "Cheetos y chizitos",
    "Waffers y dulces",
    "Minitriples de jamón y queso",
    "Tamal",
    "Papás, chifles, camotes y chifles",
    "Otro (indicar)",
]

LISTA_BEBIDAS_ALC = [
    "Ninguna",
    "Pisco",
    "Cerveza",
    "Vino",
    "Ron",
    "Otro (indicar)",
]

LISTA_BEBIDAS_NO_ALC = [
    "Ninguna",
    "Gaseosa",
    "Everest",
    "Agua",
    "Hielo",
    "Limón",
    "Otro (indicar)",
]

# Cupos máximos por piqueo (número de personas)
PIQUEO_CUPOS_MAX = {
    "Alfajores": 3,
    "Petipan de pollo": 2,
    "Empanaditas surtidas": 3,
    "Cheetos y chizitos": 2,
    "Waffers y dulces": 2,
    "Minitriples de jamón y queso": 2,
    "Tamal": 2,
    "Papás, chifles, camotes y chifles": 3,
    # "Otro (indicar)" sin límite
}

# ---------- FUNCIONES AUXILIARES ----------

def cargar_aportes():
    columnas = [
        "nombre",
        "piqueo",
        "cant_piqueo",
        "bebida_alcoholica",
        "cant_bebida_alcoholica",
        "bebida_no_alcoholica",
        "cant_bebida_no_alcoholica",
    ]
    if ARCHIVO_APORTES.exists():
        df = pd.read_csv(ARCHIVO_APORTES, dtype=str)
        for c in columnas:
            if c not in df.columns:
                df[c] = ""
        df = df[columnas]
    else:
        df = pd.DataFrame(columns=columnas)
    return df


def guardar_aportes(df_aportes: pd.DataFrame):
    df_aportes.to_csv(ARCHIVO_APORTES, index=False, encoding="utf-8")


def contar_piqueos(df_aportes: pd.DataFrame):
    conteo = {p: 0 for p in PIQUEO_CUPOS_MAX.keys()}
    if not df_aportes.empty:
        for p in df_aportes["piqueo"]:
            if p in conteo:
                conteo[p] += 1
    return conteo


# ---------- APP STREAMLIT ----------

def main():
    st.set_page_config(
        page_title="Aportes Posada Territorial 2025",
        page_icon="🎄",
        layout="centered",
    )

    # ---- Estilos ----
    st.markdown(
        """
        <style>
        /* Forzar modo claro */
        html, body, [data-testid="stAppViewContainer"], .stApp {
            color-scheme: light !important;
        }

        /* Fondo suave */
        .stApp {
            background: linear-gradient(180deg, #fff7f0 0%, #ffffff 40%);
        }

        /* Títulos */
        .titulo-principal {
            font-size: 2.1rem;
            font-weight: 700;
            text-align: center;
            color: #234;
            margin-bottom: 0.2rem;
        }
        .subtitulo {
            text-align: center;
            color: #555;
            font-size: 0.95rem;
            margin-bottom: 1.2rem;
        }

        /* Tarjetas */
        .card {
            background-color: #ffffff;
            padding: 1.2rem 1rem;
            border-radius: 0.8rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border: 1px solid #f0e0d2;
        }

        /* Botón principal más vistoso */
        .stButton>button[kind="primary"] {
            background: linear-gradient(135deg, #ff7f50, #ff4b8b);
            color: white;
            border-radius: 999px;
            padding: 0.55rem 1.4rem;
            border: none;
            font-weight: 600;
            font-size: 0.95rem;
            box-shadow: 0 3px 10px rgba(0,0,0,0.18);
        }
        .stButton>button[kind="primary"]:hover {
            filter: brightness(1.05);
            transform: translateY(-1px);
            box-shadow: 0 5px 14px rgba(0,0,0,0.25);
        }

        /* Tabla de cupos más centrada */
        .cuadro-cupos table {
            width: 100%;
        }
        .cuadro-cupos th, .cuadro-cupos td {
            text-align: center !important;
            font-size: 0.85rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---- Portada ----
    if Path(IMAGEN_PORTADA).exists():
        st.image(IMAGEN_PORTADA, use_column_width=True)
    st.markdown(
        '<div class="titulo-principal">🎄 Aportes Posada Territorial 2025 🎁</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="subtitulo">Registra tu piqueo y tus bebidas para organizar mejor la mesa ✨</div>',
        unsafe_allow_html=True,
    )

    # ---- Aviso importante ----
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
    conteo_piqueos = contar_piqueos(df_aportes)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Layout ----
    col_izq, col_der = st.columns([1.2, 0.8])

    # ---------- DERECHA: OPCIONES Y CUPOS ----------
    with col_der:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🍽️ Opciones y cupos (piqueos)")

        filas = []
        for p, maximo in PIQUEO_CUPOS_MAX.items():
            usados = conteo_piqueos[p]
            quedan = maximo - usados
            estado = "✅ Disponible" if quedan > 0 else "🚫 LLENO"
            filas.append(
                {
                    "Piqueo": p,
                    "Registradas": usados,
                    "Máx": maximo,
                    "Quedan": max(0, quedan),
                    "Estado": estado,
                }
            )

        df_cupos = pd.DataFrame(filas)
        # Estilo: sin índice y centrado
        styler = df_cupos.style.hide(axis="index")
        st.markdown('<div class="cuadro-cupos">', unsafe_allow_html=True)
        st.table(styler)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------- IZQUIERDA: FORMULARIO ----------
    with col_izq:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📝 Registrar tu aporte")

        with st.form("form_aporte"):
            # Nombre
            nombre = st.selectbox("Selecciona tu nombre:", PARTICIPANTES, key="nombre")

            # --- Piqueo ---
            st.markdown("#### 🧀 Piqueo")
            piqueo_sel = st.radio(
                "¿Qué piqueo vas a llevar?",
                LISTA_PIQUEOS,
                key="piqueo_sel",
            )
            piqueo_otro = ""
            if piqueo_sel == "Otro (indicar)":
                piqueo_otro = st.text_input(
                    "Indica el piqueo:",
                    key="piqueo_otro",
                    placeholder="Ejemplo: hamburguesitas, pizza, etc.",
                )

            cant_piqueo = st.number_input(
                "Cantidad de piqueo (unidades / porciones):",
                min_value=0,
                step=1,
                value=0,
                key="cant_piqueo",
            )

            # --- Bebida alcohólica ---
            st.markdown("#### 🍷 Bebida alcohólica (opcional)")
            beb_alc_sel = st.radio(
                "Si llevarás bebida alcohólica, elige una:",
                LISTA_BEBIDAS_ALC,
                key="beb_alc_sel",
            )
            beb_alc_otro = ""
            if beb_alc_sel == "Otro (indicar)":
                beb_alc_otro = st.text_input(
                    "Indica la bebida alcohólica:",
                    key="beb_alc_otro",
                    placeholder="Ejemplo: sangría, whisky, etc.",
                )
            cant_beb_alc = st.number_input(
                "Cantidad (botellas / six pack / unidades):",
                min_value=0,
                step=1,
                value=0,
                key="cant_beb_alc",
            )

            # --- Bebida no alcohólica ---
            st.markdown("#### 🥤 Bebida no alcohólica (opcional)")
            beb_noalc_sel = st.radio(
                "Si llevarás bebida no alcohólica, elige una:",
                LISTA_BEBIDAS_NO_ALC,
                key="beb_noalc_sel",
            )
            beb_noalc_otro = ""
            if beb_noalc_sel == "Otro (indicar)":
                beb_noalc_otro = st.text_input(
                    "Indica la bebida no alcohólica:",
                    key="beb_noalc_otro",
                    placeholder="Ejemplo: ponche, jugo de maracuyá, etc.",
                )
            cant_beb_noalc = st.number_input(
                "Cantidad (botellas / litros / unidades):",
                min_value=0,
                step=1,
                value=0,
                key="cant_beb_noalc",
            )

            enviado = st.form_submit_button("✅ Registrar aporte", use_container_width=True)

        # ---------- PROCESAR ENVÍO ----------
        if enviado:
            # Validación nombre
            if not nombre.strip():
                st.error("Por favor selecciona tu nombre.")
                st.stop()

            # Evitar duplicados
            if not df_aportes.empty and nombre in df_aportes["nombre"].values:
                st.error("Ya registraste tu aporte antes. Si necesitas cambiarlo, avisa a la organización.")
                st.stop()

            # Al menos una bebida
            if beb_alc_sel == "Ninguna" and beb_noalc_sel == "Ninguna":
                st.error("Elige al menos una bebida (alcohólica o no alcohólica).")
                st.stop()

            # Piqueo final
            if piqueo_sel == "Otro (indicar)":
                if not piqueo_otro.strip():
                    st.error("Especifica qué piqueo llevarás en 'Otro (indicar)'.")
                    st.stop()
                piqueo_final = piqueo_otro.strip()
            else:
                piqueo_final = piqueo_sel
                # Validar cupos si tiene límite
                if piqueo_final in PIQUEO_CUPOS_MAX:
                    usados = conteo_piqueos[piqueo_final]
                    if usados >= PIQUEO_CUPOS_MAX[piqueo_final]:
                        st.error("Ese piqueo ya alcanzó el máximo de personas. Por favor elige otro.")
                        st.stop()

            # Bebida alcohólica final
            if beb_alc_sel == "Ninguna":
                beb_alc_final = ""
                cant_beb_alc_final = 0
            else:
                if beb_alc_sel == "Otro (indicar)":
                    if not beb_alc_otro.strip():
                        st.error("Especifica qué bebida alcohólica llevarás en 'Otro (indicar)'.")
                        st.stop()
                    beb_alc_final = beb_alc_otro.strip()
                else:
                    beb_alc_final = beb_alc_sel
                cant_beb_alc_final = int(cant_beb_alc)

            # Bebida no alcohólica final
            if beb_noalc_sel == "Ninguna":
                beb_noalc_final = ""
                cant_beb_noalc_final = 0
            else:
                if beb_noalc_sel == "Otro (indicar)":
                    if not beb_noalc_otro.strip():
                        st.error("Especifica qué bebida no alcohólica llevarás en 'Otro (indicar)'.")
                        st.stop()
                    beb_noalc_final = beb_noalc_otro.strip()
                else:
                    beb_noalc_final = beb_noalc_sel
                cant_beb_noalc_final = int(cant_beb_noalc)

            # Validar cantidades
            if cant_piqueo <= 0:
                st.error("Por favor indica la cantidad de piqueo (mayor a 0).")
                st.stop()
            if beb_alc_final and cant_beb_alc_final <= 0:
                st.error("Si vas a llevar bebida alcohólica, indica una cantidad mayor a 0.")
                st.stop()
            if beb_noalc_final and cant_beb_noalc_final <= 0:
                st.error("Si vas a llevar bebida no alcohólica, indica una cantidad mayor a 0.")
                st.stop()

            # Crear registro
            nuevo = {
                "nombre": nombre.strip(),
                "piqueo": piqueo_final,
                "cant_piqueo": int(cant_piqueo),
                "bebida_alcoholica": beb_alc_final,
                "cant_bebida_alcoholica": cant_beb_alc_final,
                "bebida_no_alcoholica": beb_noalc_final,
                "cant_bebida_no_alcoholica": cant_beb_noalc_final,
            }

            df_aportes = pd.concat([df_aportes, pd.DataFrame([nuevo])], ignore_index=True)
            guardar_aportes(df_aportes)

            msg = f"¡Listo, {nombre}! Llevarás **{int(cant_piqueo)}** de **{piqueo_final}**"
            if beb_alc_final:
                msg += f", **{cant_beb_alc_final}** de **{beb_alc_final}**"
            if beb_noalc_final:
                msg += f", y **{cant_beb_noalc_final}** de **{beb_noalc_final}**"
            st.success(msg + " 🎉")

            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ---- APORTES REGISTRADOS ----
    if not df_aportes.empty:
        st.subheader("📋 Aportes registrados hasta ahora")

        df_mostrar = df_aportes.copy()

        # Convertir cantidades a int (para que no salgan 4.0)
        for col in [
            "cant_piqueo",
            "cant_bebida_alcoholica",
            "cant_bebida_no_alcoholica",
        ]:
            df_mostrar[col] = (
                pd.to_numeric(df_mostrar[col], errors="coerce")
                .fillna(0)
                .astype(int)
            )

        df_mostrar.rename(
            columns={
                "nombre": "Nombre",
                "piqueo": "Piqueo",
                "cant_piqueo": "Cant. piqueo",
                "bebida_alcoholica": "Bebida alcohólica",
                "cant_bebida_alcoholica": "Cant. beb. alcohólica",
                "bebida_no_alcoholica": "Bebida no alcohólica",
                "cant_bebida_no_alcoholica": "Cant. beb. no alcohólica",
            },
            inplace=True,
        )

        df_mostrar = df_mostrar.sort_values("Nombre").reset_index(drop=True)
        st.dataframe(df_mostrar, use_container_width=True, hide_index=True)

        # Quiénes faltan
        nombres_ya = set(df_aportes["nombre"].tolist())
        faltan = [n for n in PARTICIPANTES if n not in nombres_ya]
        if faltan:
            st.markdown(
                """
                <div style="
                    background-color:#fffbe6;
                    padding:10px 14px;
                    border-radius:8px;
                    border:1px solid #ffe58f;
                    margin-top:12px;">
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                "**Faltan registrar:** " + ", ".join(faltan),
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.success("🎉 ¡Todos los participantes ya registraron su aporte!")


if __name__ == "__main__":
    main()