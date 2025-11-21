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
    "Vino tinto",
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
}

# Config de tipos de cantidad por piqueo
PIQUEO_CONFIG = {
    "Alfajores": {
        "unit_type": "fraction_ciento",
        "fraction_options": {
            "1/8 de ciento (12 unidades)": 12,
            "1/4 de ciento (25 unidades)": 25,
        },
        "person_max": 25,
    },
    "Petipan de pollo": {
        "unit_type": "fraction_ciento",
        "fraction_options": {
            "1/8 de ciento (12 unidades)": 12,
            "1/4 de ciento (25 unidades)": 25,
        },
        "person_max": 25,
    },
    "Empanaditas surtidas": {
        "unit_type": "fraction_ciento",
        "fraction_options": {
            "1/8 de ciento (12 unidades)": 12,
            "1/4 de ciento (25 unidades)": 25,
        },
        "person_max": 25,
    },
    "Minitriples de jamón y queso": {
        "unit_type": "fraction_ciento",
        "fraction_options": {
            "1/8 de ciento (12 unidades)": 12,
            "1/4 de ciento (25 unidades)": 25,
        },
        "person_max": 25,
    },
    "Cheetos y chizitos": {
        "unit_type": "bags",
        "person_max": 3,
    },
    "Papás, chifles, camotes y chifles": {
        "unit_type": "bags",
        "person_max": 3,
    },
    "Tamal": {
        "unit_type": "units",
        "person_max": 4,
    },
    "Waffers y dulces": {
        "unit_type": "units",
        "person_max": 12,
    },
}

# -------- Recetas de tragos --------
RECIPES = {
    "Pisco": {
        "Chilcano clásico": ["pisco", "ginger ale", "limón", "hielo"],
        "Chilcano de maracuyá": [
            "pisco",
            "maracuyá",
            "limón",
            "azúcar",
            "ginger ale",
            "hielo",
        ],
    },
    "Vino tinto": {
        "Tinto de verano": ["vino tinto", "gaseosa", "hielo"],
        "Sangría": ["vino tinto", "frutas", "gaseosa", "azúcar", "hielo"],
    },
    "Ron": {
        "Mojito": ["ron", "hierbabuena", "limón", "azúcar", "agua con gas", "hielo"],
        "Cuba libre": ["ron", "gaseosa cola", "hielo", "limón"],
    },
    "Whisky": {
        "Whisky solo": ["whisky", "hielo"],
    },
    "Cerveza": {
        "Cerveza sola": ["cerveza"],
    },
}

BEBIDA_ALC_TOKENS = {
    "pisco": "pisco",
    "cerveza": "cerveza",
    "vino tinto": "vino tinto",
    "vino": "vino tinto",
    "ron": "ron",
}

BEBIDA_NOALC_TOKENS = {
    "gaseosa": "gaseosa",
    "everest": "ginger ale",
    "agua": "agua",
    "hielo": "hielo",
    "limón": "limón",
}

# ---------- UTILIDADES ----------

def normalizar(s: str) -> str:
    if not isinstance(s, str):
        return ""
    return s.strip().lower()

def safe_int(value):
    try:
        num = pd.to_numeric(value, errors="coerce")
        if pd.isna(num):
            return 0
        return int(num)
    except:
        return 0

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

def obtener_cantidad_piqueo(piqueo_sel: str):
    if piqueo_sel not in PIQUEO_CONFIG:
        cant = st.number_input(
            "Cantidad de piqueo (unidades / porciones):",
            min_value=0, step=1, value=0,
            key="cant_piqueo_generico"
        )
        return int(cant)

    cfg = PIQUEO_CONFIG[piqueo_sel]
    tipo = cfg["unit_type"]

    if tipo == "fraction_ciento":
        opcion = st.selectbox(
            "Cantidad (fracción de ciento):",
            list(cfg["fraction_options"].keys()),
            key=f"frac_{piqueo_sel}",
        )
        unidades = cfg["fraction_options"][opcion]
        unidades = min(unidades, cfg["person_max"])
        return int(unidades)

    if tipo == "bags":
        cant = st.number_input(
            "Cantidad de bolsas:",
            min_value=0, max_value=cfg["person_max"],
            step=1, value=0,
            key=f"bags_{piqueo_sel}",
        )
        return int(cant)

    cant = st.number_input(
        "Cantidad (unidades):",
        min_value=0, max_value=cfg["person_max"],
        step=1, value=0,
        key=f"units_{piqueo_sel}",
    )
    return int(cant)

def ingredientes_disponibles(df):
    tokens = set()
    if df.empty:
        return tokens

    for _, row in df.iterrows():
        # Alcohólica
        beb_alc = normalizar(row["bebida_alcoholica"])
        cant_alc = safe_int(row["cant_bebida_alcoholica"])
        if beb_alc and cant_alc > 0 and beb_alc in BEBIDA_ALC_TOKENS:
            tokens.add(BEBIDA_ALC_TOKENS[beb_alc])

        # No alcohólica
        beb_noalc = normalizar(row["bebida_no_alcoholica"])
        cant_noalc = safe_int(row["cant_bebida_no_alcoholica"])
        if beb_noalc and cant_noalc > 0 and beb_noalc in BEBIDA_NOALC_TOKENS:
            tokens.add(BEBIDA_NOALC_TOKENS[beb_noalc])

    return tokens

# ---------- APP STREAMLIT ----------

def main():
    st.set_page_config(
        page_title="Aportes Posada Territorial 2025",
        page_icon="🎄",
        layout="centered",
    )

    # ---- ESTILOS ----
    st.markdown(
        """
        <style>
        html, body, [data-testid="stAppViewContainer"], .stApp {
            color-scheme: light !important;
        }
        .stApp {
            background: linear-gradient(180deg, #fff7f0 0%, #ffffff 40%);
        }
        .titulo-principal {
            font-size: 2.1rem;
            font-weight: 700;
            text-align: center;
            color: #234;
        }
        .subtitulo {
            text-align: center;
            color: #555;
            font-size: 0.95rem;
            margin-bottom: 1.2rem;
        }
        .card {
            background-color: #ffffff;
            padding: 1.2rem 1rem;
            border-radius: 0.8rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border: 1px solid #f0e0d2;
        }
        .stButton>button[kind="primary"] {
            background: linear-gradient(135deg, #ff7f50, #ff4b8b);
            color: white;
            border-radius: 999px;
            padding: 0.55rem 1.4rem;
            border: none;
            font-weight: 600;
        }
        .stButton>button[kind="primary"]:hover {
            filter: brightness(1.05);
            transform: translateY(-1px);
        }
        .cuadro-cupos th, .cuadro-cupos td {
            text-align: center !important;
            font-size: 0.9rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if Path(IMAGEN_PORTADA).exists():
        st.image(IMAGEN_PORTADA, use_column_width=True)

    st.markdown('<div class="titulo-principal">🎄 Aportes Posada Territorial 2025</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo">Registra tu aporte ✨</div>', unsafe_allow_html=True)

    df = cargar_aportes()
    conteo = contar_piqueos(df)

    col_izq, col_der = st.columns([1.2, 0.8])

    # -------- DERECHA --------
    with col_der:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🍽️ Cupos por piqueo")

        filas = []
        for p, maximo in PIQUEO_CUPOS_MAX.items():
            usados = conteo[p]
            quedan = maximo - usados
            estado = "✅ Disponible" if quedan > 0 else "🚫 LLENO"
            filas.append({
                "Piqueo": p,
                "Registrados": usados,
                "Máx": maximo,
                "Quedan": max(quedan, 0),
                "Estado": estado
            })

        df_cupos = pd.DataFrame(filas)
        st.table(df_cupos.style.hide(axis="index"))

        st.markdown("---")
        st.subheader("🍹 Tragos posibles con lo que ya hay")

        tokens = ingredientes_disponibles(df)

        if not tokens:
            st.markdown(
                "<p style='color:#777;'>Aún no hay bebidas suficientes para sugerir tragos.</p>",
                unsafe_allow_html=True,
            )
        else:
            for base, recetas in RECIPES.items():
                base_token = normalizar(base)
                if base_token not in tokens:
                    continue

                st.markdown(f"**Con {base.lower()} se puede preparar:**")
                for nombre, reqs in recetas.items():
                    faltan = [r for r in reqs if r not in tokens]
                    if not faltan:
                        st.markdown(f"- ✅ {nombre}")
                    else:
                        st.markdown(f"- ℹ️ {nombre}: faltarían **{', '.join(faltan)}**")

        st.markdown("</div>", unsafe_allow_html=True)

    # -------- IZQUIERDA --------
    with col_izq:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📝 Registrar aporte")

        with st.form("form"):
            nombre = st.selectbox("Selecciona tu nombre:", PARTICIPANTES)

            st.markdown("#### 🧀 Piqueo")
            piqueo_sel = st.radio("¿Qué piqueo vas a llevar?", LISTA_PIQUEOS)

            piqueo_otro = ""
            if piqueo_sel == "Otro (indicar)":
                piqueo_otro = st.text_input("Indica el piqueo:")

            cant_piqueo = obtener_cantidad_piqueo(piqueo_sel)

            st.markdown("#### 🍷 Bebida alcohólica (opcional)")
            beb_alc_sel = st.radio("Bebida alcohólica:", LISTA_BEBIDAS_ALC)

            beb_alc_otro = ""
            if beb_alc_sel == "Otro (indicar)":
                beb_alc_otro = st.text_input("¿Cuál bebida alcohólica?")

            if beb_alc_sel == "Cerveza":
                cant_beb_alc = st.number_input("Six-pack de cerveza:", min_value=0, step=1)
            else:
                cant_beb_alc = st.number_input("Cantidad (botellas):", min_value=0, step=1)

            st.markdown("#### 🥤 Bebida no alcohólica / ingredientes")
            beb_noalc_sel = st.radio("Bebida no alcohólica:", LISTA_BEBIDAS_NO_ALC)

            beb_noalc_otro = ""
            if beb_noalc_sel == "Otro (indicar)":
                beb_noalc_otro = st.text_input("¿Cuál ingrediente / bebida?")

            cant_beb_noalc = st.number_input("Cantidad:", min_value=0, step=1)

            enviar = st.form_submit_button("Registrar aporte")

        # Validación & guardado
        if enviar:
            if not nombre:
                st.error("Selecciona tu nombre.")
                st.stop()

            if not df.empty and nombre in df["nombre"].values:
                st.error("Ya registraste tu aporte antes.")
                st.stop()

            if beb_alc_sel == "Ninguna" and beb_noalc_sel == "Ninguna":
                st.error("Debes registrar al menos una bebida.")
                st.stop()

            if cant_piqueo <= 0:
                st.error("Indica la cantidad de piqueo.")
                st.stop()

            if piqueo_sel == "Otro (indicar)":
                if not piqueo_otro:
                    st.error("Indica qué piqueo llevarás.")
                    st.stop()
                piqueo_final = piqueo_otro
            else:
                piqueo_final = piqueo_sel
                if piqueo_final in PIQUEO_CUPOS_MAX:
                    if conteo[piqueo_final] >= PIQUEO_CUPOS_MAX[piqueo_final]:
                        st.error("Ese piqueo ya llegó a su máximo.")
                        st.stop()

            # Bebida alcohólica
            if beb_alc_sel == "Ninguna":
                beb_alc_final, cant_alc_final = "", 0
            else:
                beb_alc_final = beb_alc_otro if beb_alc_sel == "Otro (indicar)" else beb_alc_sel
                if cant_beb_alc <= 0:
                    st.error("Indica la cantidad de bebida alcohólica.")
                    st.stop()
                cant_alc_final = int(cant_beb_alc)

            # Bebida no alcohólica
            if beb_noalc_sel == "Ninguna":
                beb_noalc_final, cant_noalc_final = "", 0
            else:
                beb_noalc_final = beb_noalc_otro if beb_noalc_sel == "Otro (indicar)" else beb_noalc_sel
                if cant_beb_noalc <= 0:
                    st.error("Indica la cantidad de bebida no alcohólica.")
                    st.stop()
                cant_noalc_final = int(cant_beb_noalc)

            nuevo = {
                "nombre": nombre,
                "piqueo": piqueo_final,
                "cant_piqueo": int(cant_piqueo),
                "bebida_alcoholica": beb_alc_final,
                "cant_bebida_alcoholica": cant_alc_final,
                "bebida_no_alcoholica": beb_noalc_final,
                "cant_bebida_no_alcoholica": cant_noalc_final,
            }

            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            guardar_aportes(df)

            st.success("¡Aporte registrado con éxito!")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    # Tabla final
    if not df.empty:
        df_final = df.copy()
        for c in ["cant_piqueo", "cant_bebida_alcoholica", "cant_bebida_no_alcoholica"]:
            df_final[c] = safe_int(df_final[c])

        st.subheader("📋 Aportes registrados")
        st.dataframe(df_final, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()