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

# --------- LISTAS ---------
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

# SIN "Ninguna", ya lo manejamos con la opción vacía del selectbox
LISTA_BEBIDAS_ALC = [
    "Pisco",
    "Cerveza",
    "Vino tinto",
    "Ron",
    "Otro (indicar)",
]

LISTA_BEBIDAS_NO_ALC = [
    "Gaseosa",
    "Everest",
    "Agua",
    "Hielo",
    "Limón",
    "Otro (indicar)",
]

# Cupos máximos por piqueo (número de PERSONAS que pueden llevar ese piqueo)
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

# Config de cantidades por tipo de piqueo (1/8, 1/4, bolsas, unidades)
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
        "person_max": 3,   # bolsas por persona
    },
    "Papás, chifles, camotes y chifles": {
        "unit_type": "bags",
        "person_max": 3,
    },
    "Tamal": {
        "unit_type": "units",
        "person_max": 4,   # tamales por persona
    },
    "Waffers y dulces": {
        "unit_type": "units",
        "person_max": 12,  # porciones por persona
    },
}

# -------- Recetas de tragos (para mostrar "qué falta") --------
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
    except Exception:
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
    """Devuelve la cantidad de piqueo según su tipo (fracción, bolsas, unidades)."""
    if piqueo_sel not in PIQUEO_CONFIG:
        cant = st.number_input(
            "Cantidad de piqueo (unidades / porciones):",
            min_value=0,
            step=1,
            value=0,
            key="cant_piqueo_generico",
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
            min_value=0,
            max_value=cfg["person_max"],
            step=1,
            value=0,
            key=f"bags_{piqueo_sel}",
        )
        return int(cant)

    # units
    cant = st.number_input(
        "Cantidad (unidades):",
        min_value=0,
        max_value=cfg["person_max"],
        step=1,
        value=0,
        key=f"units_{piqueo_sel}",
    )
    return int(cant)

def ingredientes_disponibles(df_aportes: pd.DataFrame):
    """Tokens de ingredientes/bebidas disponibles según lo registrado."""
    tokens = set()
    if df_aportes.empty:
        return tokens

    for _, row in df_aportes.iterrows():
        # Bebida alcohólica
        beb_alc = normalizar(row.get("bebida_alcoholica", ""))
        cant_alc = safe_int(row.get("cant_bebida_alcoholica", 0))
        if beb_alc and cant_alc > 0 and beb_alc in BEBIDA_ALC_TOKENS:
            tokens.add(BEBIDA_ALC_TOKENS[beb_alc])

        # Bebida / ingrediente no alcohólico
        beb_noalc = normalizar(row.get("bebida_no_alcoholica", ""))
        cant_noalc = safe_int(row.get("cant_bebida_no_alcoholica", 0))
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
        /* Evitar que los headers se rompan verticalmente */
        .dataframe th, .dataframe td {
            white-space: nowrap;
            text-align: center !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Portada
    if Path(IMAGEN_PORTADA).exists():
        st.image(IMAGEN_PORTADA, use_column_width=True)

    st.markdown('<div class="titulo-principal">🎄 Aportes Posada Territorial 2025</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo">Registra tu aporte ✨</div>', unsafe_allow_html=True)

    df_aportes = cargar_aportes()
    conteo_piqueos = contar_piqueos(df_aportes)

    col_izq, col_der = st.columns([1.2, 0.8])

    # ---------- DERECHA: CUPOS + TRAGOS ----------
    with col_der:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🍽️ Cupos por piqueo")

        filas = []
        for p, maximo in PIQUEO_CUPOS_MAX.items():
            usados = conteo_piqueos[p]
            quedan = maximo - usados
            ok = quedan > 0
            filas.append(
                {
                    "Piqueo": p,
                    "Registrados": usados,
                    "Máx. personas": maximo,
                    "Quedan": max(quedan, 0),
                    "✓": "✅" if ok else "🚫",
                    "Estado": "Disponible" if ok else "Lleno",
                }
            )

        df_cupos = pd.DataFrame(filas)
        df_cupos = df_cupos[["Piqueo", "Registrados", "Máx. personas", "Quedan", "✓", "Estado"]]
        st.dataframe(df_cupos, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("🍹 Tragos posibles con lo que ya hay")

        tokens = ingredientes_disponibles(df_aportes)
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
                for nombre_trago, reqs in recetas.items():
                    faltan = [r for r in reqs if r not in tokens]
                    if not faltan:
                        st.markdown(f"- ✅ {nombre_trago}")
                    else:
                        st.markdown(f"- ℹ️ {nombre_trago}: faltarían **{', '.join(faltan)}**")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- IZQUIERDA: FORMULARIO ----------
    with col_izq:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📝 Registrar aporte")

        with st.form("form_aporte"):
            nombre = st.selectbox("Selecciona tu nombre:", PARTICIPANTES)

            # ---- Piqueo ----
            st.markdown("#### 🧀 Piqueo")
            piqueo_sel = st.radio("¿Qué piqueo vas a llevar?", LISTA_PIQUEOS)

            piqueo_otro = ""
            if piqueo_sel == "Otro (indicar)":
                piqueo_otro = st.text_input("Indica el piqueo:")

            cant_piqueo = obtener_cantidad_piqueo(piqueo_sel)

            # ---- Bebida alcohólica (opcional) ----
            st.markdown("#### 🍷 Bebida alcohólica (opcional)")
            beb_alc_raw = st.selectbox(
                "Si llevarás bebida alcohólica, elige una (o deja vacío):",
                ["(Sin bebida alcohólica)"] + LISTA_BEBIDAS_ALC,
            )
            beb_alc_sel = "" if beb_alc_raw == "(Sin bebida alcohólica)" else beb_alc_raw

            beb_alc_otro = ""
            if beb_alc_sel == "Otro (indicar)":
                beb_alc_otro = st.text_input("¿Cuál bebida alcohólica?")

            if beb_alc_sel == "Cerveza":
                cant_beb_alc = st.number_input(
                    "Cantidad (six-pack de cerveza):",
                    min_value=0,
                    step=1,
                    value=0,
                )
            elif beb_alc_sel:
                cant_beb_alc = st.number_input(
                    "Cantidad (botellas / unidades):",
                    min_value=0,
                    step=1,
                    value=0,
                )
            else:
                cant_beb_alc = 0

            # ---- Bebida no alcohólica / ingredientes ----
            st.markdown("#### 🥤 Bebida no alcohólica / ingredientes")
            beb_noalc_raw = st.selectbox(
                "Si llevarás bebida no alcohólica o ingredientes, elige una (o deja vacío):",
                ["(Sin bebida no alcohólica / ingrediente)"] + LISTA_BEBIDAS_NO_ALC,
            )
            beb_noalc_sel = "" if beb_noalc_raw == "(Sin bebida no alcohólica / ingrediente)" else beb_noalc_raw

            beb_noalc_otro = ""
            if beb_noalc_sel == "Otro (indicar)":
                beb_noalc_otro = st.text_input("¿Cuál bebida / ingrediente?")

            if beb_noalc_sel:
                cant_beb_noalc = st.number_input(
                    "Cantidad (botellas / litros / unidades):",
                    min_value=0,
                    step=1,
                    value=0,
                )
            else:
                cant_beb_noalc = 0

            enviado = st.form_submit_button("✅ Registrar aporte", use_container_width=True)

        # ---------- PROCESAR ENVÍO ----------
        if enviado:
            # Validación nombre
            if not nombre.strip():
                st.error("Selecciona tu nombre.")
                st.stop()

            # Evitar duplicados
            if not df_aportes.empty and nombre in df_aportes["nombre"].values:
                st.error("Ya registraste tu aporte antes.")
                st.stop()

            # Validar piqueo
            if piqueo_sel == "Otro (indicar)":
                if not piqueo_otro.strip():
                    st.error("Indica qué piqueo llevarás.")
                    st.stop()
                piqueo_final = piqueo_otro.strip()
            else:
                piqueo_final = piqueo_sel
                if piqueo_final in PIQUEO_CUPOS_MAX:
                    usados = conteo_piqueos[piqueo_final]
                    if usados >= PIQUEO_CUPOS_MAX[piqueo_final]:
                        st.error("Ese piqueo ya llegó a su máximo de personas.")
                        st.stop()

            if cant_piqueo <= 0:
                st.error("Indica la cantidad de piqueo (mayor a 0).")
                st.stop()

            # ---- Construir bebida alcohólica final ----
            if not beb_alc_sel:
                beb_alc_final = ""
                cant_beb_alc_final = 0
            else:
                if beb_alc_sel == "Otro (indicar)":
                    if not beb_alc_otro.strip():
                        st.error("Especifica qué bebida alcohólica llevarás.")
                        st.stop()
                    beb_alc_final = beb_alc_otro.strip()
                else:
                    beb_alc_final = beb_alc_sel

                if cant_beb_alc <= 0:
                    st.error("Indica una cantidad mayor a 0 para la bebida alcohólica o deja la opción vacía.")
                    st.stop()
                cant_beb_alc_final = int(cant_beb_alc)

            # ---- Construir bebida no alcohólica final ----
            if not beb_noalc_sel:
                beb_noalc_final = ""
                cant_beb_noalc_final = 0
            else:
                if beb_noalc_sel == "Otro (indicar)":
                    if not beb_noalc_otro.strip():
                        st.error("Especifica qué bebida no alcohólica / ingrediente llevarás.")
                        st.stop()
                    beb_noalc_final = beb_noalc_otro.strip()
                else:
                    beb_noalc_final = beb_noalc_sel

                if cant_beb_noalc <= 0:
                    st.error("Indica una cantidad mayor a 0 para la bebida no alcohólica / ingrediente o deja la opción vacía.")
                    st.stop()
                cant_beb_noalc_final = int(cant_beb_noalc)

            # Validar que haya AL MENOS una bebida (alc o no)
            if (not beb_alc_final or cant_beb_alc_final <= 0) and (
                not beb_noalc_final or cant_beb_noalc_final <= 0
            ):
                st.error("Debes registrar al menos una bebida (alcohólica o no alcohólica) con cantidad mayor a 0.")
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
                if normalizar(beb_alc_final) == "cerveza":
                    msg += f", **{cant_beb_alc_final}** six-pack de **{beb_alc_final}**"
                else:
                    msg += f", **{cant_beb_alc_final}** de **{beb_alc_final}**"
            if beb_noalc_final:
                msg += f", y **{cant_beb_noalc_final}** de **{beb_noalc_final}**"

            st.success(msg + " 🎉")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ---- APORTES REGISTRADOS ----
    if not df_aportes.empty:
        st.subheader("📋 Aportes registrados")

        df_mostrar = df_aportes.copy()
        for col in [
            "cant_piqueo",
            "cant_bebida_alcoholica",
            "cant_bebida_no_alcoholica",
        ]:
            df_mostrar[col] = df_mostrar[col].apply(safe_int)

        df_mostrar.rename(
            columns={
                "nombre": "Nombre",
                "piqueo": "Piqueo",
                "cant_piqueo": "Cant. piqueo",
                "bebida_alcoholica": "Bebida alcohólica",
                "cant_bebida_alcoholica": "Cant. beb. alcohólica",
                "bebida_no_alcoholica": "Bebida no alcohólica / ingrediente",
                "cant_bebida_no_alcoholica": "Cant. beb. no alcohólica / ingr.",
            },
            inplace=True,
        )

        st.dataframe(df_mostrar, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()