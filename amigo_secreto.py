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

LISTA_BEBIDAS_ALC = [
    "Pisco",
    "Cerveza",
    "Vino",
    "Ron",
    "Otro (indicar)",
]

LISTA_BEBIDAS_NO_ALC = [
    "Gaseosa",
    "Everest o ginger",
    "Agua",
    "Hielo",
    "Limón",
    "Otro (indicar)",
]

# ------------ CLASIFICACIÓN DE PIQUEOS ------------
PIQUEO_TIPO_DEFAULT = {
    "Alfajores": "Dulce",
    "Petipan de pollo": "Preparado",
    "Empanaditas surtidas": "Preparado",
    "Cheetos y chizitos": "Snack en bolsa",
    "Waffers y dulces": "Dulce",
    "Minitriples de jamón y queso": "Preparado",
    "Tamal": "Preparado",
    "Papás, chifles, camotes y chifles": "Snack en bolsa",
}

PIQUEO_UNIDAD = {
    "Alfajores": "unidades (12–25)",
    "Petipan de pollo": "fracción de ciento",
    "Empanaditas surtidas": "fracción de ciento",
    "Cheetos y chizitos": "bolsas grandes",
    "Waffers y dulces": "porciones / paquetitos",
    "Minitriples de jamón y queso": "fracción de ciento",
    "Tamal": "unidades",
    "Papás, chifles, camotes y chifles": "bolsas grandes",
}

PIQUEO_MAX_TEXTO = {
    "Alfajores": "≈25 unidades en total",
    "Petipan de pollo": "≈40 unidades en total",
    "Empanaditas surtidas": "≈25 unidades en total",
    "Cheetos y chizitos": "Grupo snacks: máx. 6 bolsas",
    "Waffers y dulces": "≈12 porciones",
    "Minitriples de jamón y queso": "≈40 unidades en total",
    "Tamal": "≈10 unidades",
    "Papás, chifles, camotes y chifles": "Grupo snacks: máx. 6 bolsas",
}

# Cupos máximos (personas que pueden elegir ese piqueo)
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

# Config de cantidades por piqueo
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

BAG_PIQUEOS = ["Cheetos y chizitos", "Papás, chifles, camotes y chifles"]
MAX_BOLSAS_GRUPO = 6  # bolsas grandes totales de snacks

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
        "Tinto de verano": ["vino", "gaseosa", "hielo"],
        "Sangría": ["vino", "frutas", "gaseosa", "azúcar", "hielo"],
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
        "tipo_piqueo",
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

def contar_bolsas(df_aportes: pd.DataFrame):
    if df_aportes.empty:
        return 0
    df_tmp = df_aportes.copy()
    df_tmp["cant_piqueo"] = df_tmp["cant_piqueo"].apply(safe_int)
    mask = (df_tmp["piqueo"].isin(BAG_PIQUEOS)) | (df_tmp["tipo_piqueo"] == "Snack en bolsa")
    return int(df_tmp.loc[mask, "cant_piqueo"].sum())

def obtener_cantidad_piqueo(piqueo_sel: str):
    """Devuelve cantidad y etiqueta para el campo, según el tipo."""
    if not piqueo_sel:
        return 0, ""

    if piqueo_sel not in PIQUEO_CONFIG:
        label = "Cantidad de piqueo (unidades / porciones):"
        cant = st.number_input(
            label,
            min_value=0,
            step=1,
            value=0,
            key="cant_piqueo_generico",
        )
        return int(cant), label

    cfg = PIQUEO_CONFIG[piqueo_sel]
    tipo = cfg["unit_type"]

    if tipo == "fraction_ciento":
        label = "Cantidad (fracción de ciento):"
        opcion = st.selectbox(
            label,
            list(cfg["fraction_options"].keys()),
            key=f"frac_{piqueo_sel}",
        )
        unidades = cfg["fraction_options"][opcion]
        unidades = min(unidades, cfg["person_max"])
        return int(unidades), label

    if tipo == "bags":
        label = "Cantidad (bolsas grandes):"
        cant = st.number_input(
            label,
            min_value=0,
            max_value=cfg["person_max"],
            step=1,
            value=0,
            key=f"bags_{piqueo_sel}",
        )
        return int(cant), label

    # units
    label = "Cantidad (unidades):"
    cant = st.number_input(
        label,
        min_value=0,
        max_value=cfg["person_max"],
        step=1,
        value=0,
        key=f"units_{piqueo_sel}",
    )
    return int(cant), label

def ingredientes_disponibles(df_aportes: pd.DataFrame):
    tokens = set()
    if df_aportes.empty:
        return tokens

    for _, row in df_aportes.iterrows():
        beb_alc = normalizar(row.get("bebida_alcoholica", ""))
        cant_alc = safe_int(row.get("cant_bebida_alcoholica", 0))
        if beb_alc and cant_alc > 0 and beb_alc in BEBIDA_ALC_TOKENS:
            tokens.add(BEBIDA_ALC_TOKENS[beb_alc])

        beb_noalc = normalizar(row.get("bebida_no_alcoholica", ""))
        cant_noalc = safe_int(row.get("cant_bebida_no_alcoholica", 0))
        if beb_noalc and cant_noalc > 0 and beb_noalc in BEBIDA_NOALC_TOKENS:
            tokens.add(BEBIDA_NOALC_TOKENS[beb_noalc])

    return tokens

def resumen_bebidas(df_aportes: pd.DataFrame):
    """Totales simples de bebidas (lo declarado por las personas)."""
    if df_aportes.empty:
        return 0, 0
    df_tmp = df_aportes.copy()
    df_tmp["cant_bebida_alcoholica"] = df_tmp["cant_bebida_alcoholica"].apply(safe_int)
    df_tmp["cant_bebida_no_alcoholica"] = df_tmp["cant_bebida_no_alcoholica"].apply(safe_int)
    total_alc = int(df_tmp["cant_bebida_alcoholica"].sum())
    total_noalc = int(df_tmp["cant_bebida_no_alcoholica"].sum())
    return total_alc, total_noalc

def estado_rango(total, minimo, maximo):
    if total < minimo:
        return f"Por debajo del mínimo ⚠️"
    if total > maximo:
        return f"Por encima del máximo ⚠️"
    return "Dentro del rango ✅"

# ---------- APP STREAMLIT ----------

def main():
    st.set_page_config(
        page_title="Aportes Posada Territorial 2025",
        page_icon="🎄",
        layout="centered",
    )

    # ---- ESTILOS / MODO CLARO ----
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
            margin-bottom: 1.2rem;
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
        .dataframe th, .dataframe td {
            white-space: nowrap;
            text-align: center !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if Path(IMAGEN_PORTADA).exists():
        st.image(IMAGEN_PORTADA, use_column_width=True)

    st.markdown('<div class="titulo-principal">🎄 Aportes Posada Territorial 2025</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo">Registra tu piqueo y bebida de forma ordenada ✨</div>', unsafe_allow_html=True)

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
            ⚠️ <strong>Sugerencia general:</strong><br>
            Somos <strong>18 personas</strong>. Para que todos puedan probar de todo sin que sobre demasiado,
            la idea es que los piqueos vengan en <strong>presentaciones grandes o para compartir</strong>
            (bolsas familiares, fracciones de ciento, bandejas), y que en total no superemos, por ejemplo,
            <strong>6 bolsas grandes de snacks</strong> y una cantidad razonable de dulces y preparados.
        </div>
        """,
        unsafe_allow_html=True,
    )

    df_aportes = cargar_aportes()
    conteo_piqueos = contar_piqueos(df_aportes)

    # ---------- FORMULARIO ----------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📝 Registrar aporte")

    nombre = st.selectbox(
        "Selecciona tu nombre:",
        sorted(PARTICIPANTES),
        key="nombre",
    )

    # ---- Piqueo ----
    st.markdown("#### 🧀 Piqueo")
    piqueo_sel = st.radio(
        "¿Qué piqueo vas a llevar?",
        LISTA_PIQUEOS,
        index=None,
        key="piqueo_sel",
    )

    piqueo_otro = ""
    tipo_piqueo = ""
    if piqueo_sel == "Otro (indicar)":
        piqueo_otro = st.text_input("Indica el piqueo:", key="piqueo_otro")
        tipo_piqueo = st.radio(
            "¿Qué tipo de piqueo es?",
            ["Snack en bolsa", "Preparado", "Dulce"],
            horizontal=True,
            key="tipo_piqueo_otro",
        )
    elif piqueo_sel:
        tipo_piqueo = PIQUEO_TIPO_DEFAULT.get(piqueo_sel, "")

    if piqueo_sel:
        cant_piqueo, _ = obtener_cantidad_piqueo(piqueo_sel)
    else:
        cant_piqueo = 0

    # ---- Bebida alcohólica ----
    st.markdown("#### 🍷 Bebida alcohólica (opcional)")
    beb_alc_raw = st.selectbox(
        "Si llevarás bebida alcohólica, elige una (o deja vacío):",
        ["(Sin bebida alcohólica)"] + LISTA_BEBIDAS_ALC,
        key="beb_alc_raw",
    )
    beb_alc_sel = "" if beb_alc_raw == "(Sin bebida alcohólica)" else beb_alc_raw

    beb_alc_otro = ""
    if beb_alc_sel == "Otro (indicar)":
        beb_alc_otro = st.text_input("¿Cuál bebida alcohólica?", key="beb_alc_otro")

    if beb_alc_sel == "Cerveza":
        cant_beb_alc = st.number_input(
            "Cantidad (six-pack de cerveza):",
            min_value=0,
            step=1,
            value=0,
            key="cant_beb_alc",
        )
    elif beb_alc_sel:
        # Aquí solo botellas, como pediste
        cant_beb_alc = st.number_input(
            "Cantidad (botellas):",
            min_value=0,
            step=1,
            value=0,
            key="cant_beb_alc",
        )
    else:
        cant_beb_alc = 0

    # ---- Bebida no alcohólica / ingredientes ----
    st.markdown("#### 🥤 Bebida no alcohólica / ingredientes")
    beb_noalc_raw = st.selectbox(
        "Si llevarás bebida no alcohólica o ingredientes, elige una (o deja vacío):",
        ["(Sin bebida no alcohólica / ingrediente)"] + LISTA_BEBIDAS_NO_ALC,
        key="beb_noalc_raw",
    )
    beb_noalc_sel = "" if beb_noalc_raw == "(Sin bebida no alcohólica / ingrediente)" else beb_noalc_raw

    beb_noalc_otro = ""
    if beb_noalc_sel == "Otro (indicar)":
        beb_noalc_otro = st.text_input("¿Cuál bebida / ingrediente?", key="beb_noalc_otro")

    if beb_noalc_sel:
        if beb_noalc_sel == "Hielo":
            label_noalc = "Cantidad (bolsas de hielo):"
        elif beb_noalc_sel == "Gaseosa":
            label_noalc = "Cantidad (botellas de gaseosa):"
        elif beb_noalc_sel == "Everest o ginger":
            label_noalc = "Cantidad (botellas):"
        elif beb_noalc_sel == "Agua":
            # Agua: explicitamente litros o botellas
            label_noalc = "Cantidad de agua (en litros):"
        elif beb_noalc_sel == "Limón":
            label_noalc = "Cantidad (kg de limón):"
        else:
            label_noalc = "Cantidad:"

        cant_beb_noalc = st.number_input(
            label_noalc,
            min_value=0,
            step=1,
            value=0,
            key="cant_beb_noalc",
        )
    else:
        cant_beb_noalc = 0

    enviado = st.button("✅ Registrar aporte", use_container_width=True, key="btn_registrar")

    # ---------- PROCESAR ----------
    if enviado:
        if not nombre.strip():
            st.error("Selecciona tu nombre.")
            st.stop()

        if not df_aportes.empty and nombre in df_aportes["nombre"].values:
            st.error("Ya registraste tu aporte antes.")
            st.stop()

        if not piqueo_sel:
            st.error("Elige un piqueo.")
            st.stop()

        if piqueo_sel == "Otro (indicar)":
            if not piqueo_otro.strip():
                st.error("Indica qué piqueo llevarás.")
                st.stop()
            if not tipo_piqueo:
                st.error("Indica el tipo de piqueo (snack en bolsa, preparado o dulce).")
                st.stop()
            piqueo_final = piqueo_otro.strip()
            tipo_piqueo_final = tipo_piqueo
        else:
            piqueo_final = piqueo_sel
            tipo_piqueo_final = PIQUEO_TIPO_DEFAULT.get(piqueo_sel, "")
            if piqueo_final in PIQUEO_CUPOS_MAX:
                usados = conteo_piqueos[piqueo_final]
                if usados >= PIQUEO_CUPOS_MAX[piqueo_final]:
                    st.error("Ese piqueo ya llegó a su máximo de personas.")
                    st.stop()

        if cant_piqueo <= 0:
            st.error("Indica la cantidad de piqueo (mayor a 0).")
            st.stop()

        if tipo_piqueo_final == "Snack en bolsa":
            bolsas_actuales = contar_bolsas(df_aportes)
            if bolsas_actuales + cant_piqueo > MAX_BOLSAS_GRUPO:
                st.error(
                    f"Con esas bolsas se superaría el máximo total de {MAX_BOLSAS_GRUPO} bolsas grandes "
                    f"para snacks. Actualmente ya hay {bolsas_actuales}."
                )
                st.stop()

        # Bebida alcohólica
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

        # Bebida no alcohólica
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

        if (not beb_alc_final or cant_beb_alc_final <= 0) and (
            not beb_noalc_final or cant_beb_noalc_final <= 0
        ):
            st.error("Debes registrar al menos una bebida (alcohólica o no alcohólica).")
            st.stop()

        nuevo = {
            "nombre": nombre.strip(),
            "piqueo": piqueo_final,
            "tipo_piqueo": tipo_piqueo_final,
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
                msg += f", **{cant_beb_alc_final}** botellas de **{beb_alc_final}**"
        if beb_noalc_final:
            msg += f", y **{cant_beb_noalc_final}** de **{beb_noalc_final}**"

        st.success(msg + " 🎉")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- CUPOS PIQUEOS ----------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🍽️ Cupos y límites por piqueo")

    filas = []
    for p, maximo in PIQUEO_CUPOS_MAX.items():
        usados = conteo_piqueos[p]
        tipo = PIQUEO_TIPO_DEFAULT.get(p, "")
        unidad = PIQUEO_UNIDAD.get(p, "")
        max_txt = PIQUEO_MAX_TEXTO.get(p, "")
        ok = usados < maximo
        filas.append(
            {
                "Piqueo": p,
                "Tipo": tipo,
                "Unidad": unidad,
                "Máx. sugerido": max_txt,
                "Personas registradas": usados,
                "Estado": "Disponible ✅" if ok else "Lleno 🚫",
            }
        )

    df_cupos = pd.DataFrame(filas)
    st.dataframe(df_cupos, use_container_width=True, hide_index=True)

    bolsas_actuales = contar_bolsas(df_aportes)
    st.markdown(
        f"""
        <div style="margin-top:8px;font-size:0.9rem;color:#555;">
        🧃 <strong>Snacks en bolsa (Cheetos, papas, chifles, camotes y similares):</strong><br>
        Máximo total sugerido: <strong>{MAX_BOLSAS_GRUPO} bolsas grandes</strong> entre todos.<br>
        Actualmente ya se han registrado <strong>{bolsas_actuales}</strong> bolsas.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------- RESUMEN DE BEBIDAS ----------
    st.markdown("---")
    st.subheader("🥤 Resumen de bebidas (cupos sugeridos)")

    total_alc, total_noalc = resumen_bebidas(df_aportes)

    # Rango sugerido para 18 personas (simple y equilibrado)
    RANGO_ALC = (6, 15)      # botellas / six-pack declarados
    RANGO_NOALC = (10, 22)   # botellas / litros / unidades

    filas_beb = [
        {
            "Tipo": "Bebidas alcohólicas",
            "Cantidad registrada": total_alc,
            "Rango sugerido": f"{RANGO_ALC[0]} – {RANGO_ALC[1]}",
            "Estado": estado_rango(total_alc, *RANGO_ALC),
        },
        {
            "Tipo": "Bebidas no alcohólicas / ingredientes",
            "Cantidad registrada": total_noalc,
            "Rango sugerido": f"{RANGO_NOALC[0]} – {RANGO_NOALC[1]}",
            "Estado": estado_rango(total_noalc, *RANGO_NOALC),
        },
    ]

    df_beb = pd.DataFrame(filas_beb)
    st.dataframe(df_beb, use_container_width=True, hide_index=True)

    st.markdown(
        """
        <div style="margin-top:6px;font-size:0.9rem;color:#555;">
        💡 La idea es que haya <strong>suficiente bebida sin alcohol</strong> para preparar jugos, chilcanos,
        sangrías, etc., y que la cantidad de alcohol sea razonable para 18 personas.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------- TRAGOS POSIBLES ----------
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

    # ---------- REGISTROS, FALTAN Y DESCARGA ----------
    if not df_aportes.empty:
        st.markdown('<div class="card">', unsafe_allow_html=True)
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
                "tipo_piqueo": "Tipo de piqueo",
                "cant_piqueo": "Cant. piqueo",
                "bebida_alcoholica": "Bebida alcohólica",
                "cant_bebida_alcoholica": "Cant. beb. alcohólica",
                "bebida_no_alcoholica": "Bebida no alcohólica / ingrediente",
                "cant_bebida_no_alcoholica": "Cant. beb. no alcohólica / ingr.",
            },
            inplace=True,
        )

        st.dataframe(df_mostrar, use_container_width=True, hide_index=True)

        # Botón descarga
        csv_bytes = df_aportes.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Descargar registros en CSV",
            data=csv_bytes,
            file_name="aportes_posada.csv",
            mime="text/csv",
        )

        nombres_ya = set(df_aportes["nombre"].tolist())
        faltan = [n for n in sorted(PARTICIPANTES) if n not in nombres_ya]
        if faltan:
            st.markdown(
                f"""
                <div style="
                    background-color:#ffecec;
                    padding:10px 14px;
                    border-radius:8px;
                    border:1px solid #ff4d4f;
                    margin-top:12px;
                    color:#a8071a;
                    font-size:0.95rem;">
                    🔴 <strong>Faltan registrar sus aportes:</strong><br>
                    {", ".join(faltan)}
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()