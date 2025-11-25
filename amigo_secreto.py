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

# -------- Recetas de tragos (para sugerencias) --------
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

# ---------- PACKS DE BEBIDAS ----------
# tipo: "alcoholico" o "no_alcoholico"
# base: para la condición de cerveza/vino y resumen
PACKS = {
    "Pack 1 – Chilcano clásico": {
        "tipo": "alcoholico",
        "base": "pisco",
        "detalle": "Pisco + ginger ale + limón + hielo (coordinar entre las personas del pack).",
    },
    "Pack 2 – Pisco sour": {
        "tipo": "alcoholico",
        "base": "pisco",
        "detalle": "Pisco + limón + huevos + azúcar + hielo (coordinar; requiere licuadora/coctelera).",
    },
    "Pack 3 – Mojito": {
        "tipo": "alcoholico",
        "base": "ron",
        "detalle": "Ron + agua con gas + hierbabuena + limón + azúcar + hielo.",
    },
    "Pack 4 – Cuba libre": {
        "tipo": "alcoholico",
        "base": "ron",
        "detalle": "Ron + gaseosa cola + limón.",
    },
    "Pack 5 – Sangría": {
        "tipo": "alcoholico",
        "base": "vino",
        "detalle": "Vino tinto + gaseosa + frutas + azúcar.",
    },
    "Pack 6 – Cerveza": {
        "tipo": "alcoholico",
        "base": "cerveza",
        "detalle": "Six-pack de cerveza + hielo. Se enfría en la refri del local.",
    },
    "Pack 7 – Sin alcohol (gaseosas, agua, jugos)": {
        "tipo": "no_alcoholico",
        "base": "",
        "detalle": "Gaseosas, agua, jugos, hielo u otros ingredientes sin alcohol.",
    },
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
        "pack_codigo",
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
    """Devuelve cantidad para el piqueo según el tipo."""
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
        if beb_alc and cant_alc > 0:
            tokens.add(beb_alc)

        beb_noalc = normalizar(row.get("bebida_no_alcoholica", ""))
        cant_noalc = safe_int(row.get("cant_bebida_no_alcoholica", 0))
        if beb_noalc and cant_noalc > 0:
            tokens.add(beb_noalc)

    return tokens

def capacidad_pack(num_packs: int) -> int:
    """Devuelve el cupo por pack según cuántos packs distintos haya en total."""
    if num_packs <= 0:
        return 0
    if num_packs == 1:
        return 18
    if num_packs == 2:
        return 9
    if num_packs == 3:
        return 6
    if num_packs == 4:
        return 5  # ejemplo 4-5-5-4
    return 5

def flags_packs(codigos):
    """Devuelve (hay_no_alcoholico, hay_cerveza_o_vino)."""
    hay_no_alc = False
    hay_cerv_vino = False
    for c in codigos:
        meta = PACKS.get(c)
        if not meta:
            continue
        if meta.get("tipo") == "no_alcoholico":
            hay_no_alc = True
        if meta.get("base") in ("cerveza", "vino"):
            hay_cerv_vino = True
    return hay_no_alc, hay_cerv_vino

def resumen_packs(df_aportes: pd.DataFrame):
    if df_aportes.empty:
        return pd.DataFrame(), 0, False, False

    df = df_aportes.copy()
    df["pack_codigo"] = df["pack_codigo"].astype(str).str.strip()
    df = df[df["pack_codigo"] != ""]
    if df.empty:
        return pd.DataFrame(), 0, False, False

    packs_activos = sorted(df["pack_codigo"].unique().tolist())
    num_packs = len(packs_activos)
    capacidad = capacidad_pack(num_packs)
    hay_no_alc, hay_cerv_vino = flags_packs(packs_activos)

    filas = []
    for pack in packs_activos:
        sub = df[df["pack_codigo"] == pack]
        personas = sub["nombre"].nunique()
        vacantes = max(0, capacidad - personas)
        estado = "Completo ✅" if personas >= capacidad else f"En formación (faltan {vacantes})"
        filas.append(
            {
                "Pack": pack,
                "Personas en el pack": personas,
                "Cupo máximo por pack": capacidad,
                "Vacantes": vacantes,
                "Estado": estado,
            }
        )

    df_res = pd.DataFrame(filas)
    return df_res, num_packs, hay_no_alc, hay_cerv_vino


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
    st.markdown('<div class="subtitulo">Registra tu piqueo y tu pack de bebidas ✨</div>', unsafe_allow_html=True)

    # ---- TARJETA DE EXPLICACIÓN GENERAL ----
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
        ⚠️ <strong>¿Cómo nos organizamos?</strong><br>
        Somos <strong>18 personas</strong>.
        <ul>
          <li><strong>Piqueos:</strong> Se lleva en <strong>presentación grande</strong> 
          (bandejas, fracciones de ciento o bolsas grandes). Hay cupos para cada tipo de piqueo y, en total, 
          trataremos de no pasar de <strong>6 bolsas grandes</strong> de snacks.</li>
          <li><strong>Bebidas:</strong> Funcionan por <strong>packs</strong>. 
          Cada pack lo comparten varias personas. Dependiendo de cuántos packs haya en total:
            <ul>
              <li>Si hay <strong>3 packs</strong>, cada pack se reparte entre <strong>6 personas</strong> aprox.</li>
              <li>Si llegamos a <strong>4 packs</strong>, se reparte algo así como <strong>4, 5, 5 y 4 personas</strong> por pack.</li>
            </ul>
          </li>
          <li>Las personas que eligen el <strong>mismo pack</strong> forman un mini-equipo y deben 
          <strong>coordinar entre ellas</strong> para dividir gastos y acordar quién lleva qué 
          (botellas, mezclas, hielo, limón, etc.).</li>
          <li>No necesitamos demasiados packs distintos. En general, con <strong>3 packs</strong> diferentes es suficiente para los 18. 
          Solo si hay al menos un pack de <strong>Cerveza o Vino</strong> y también un pack 
          <strong>sin alcohol</strong>, se permite llegar a <strong>4 packs</strong> en total.</li>
          <li>Las cervezas se pueden enfriar en la <strong>refri del local</strong>.</li>
        </ul>
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

    # ---------- PACKS DE BEBIDAS ----------
    st.markdown("### 🍹 Packs de bebidas")

    pack_opciones = ["(Elige un pack)"] + list(PACKS.keys())
    pack_sel = st.selectbox(
        "Elige el pack de bebidas con el que quieres sumarte:",
        pack_opciones,
        key="pack_sel",
    )

    # info sobre packs ya registrados
    packs_actuales = set()
    if not df_aportes.empty:
        packs_actuales = set(df_aportes["pack_codigo"].astype(str).str.strip())
        packs_actuales.discard("")

    pack_codigo = ""
    beb_alc_final = ""
    cant_beb_alc_final = 0
    beb_noalc_final = ""
    cant_beb_noalc_final = 0

    if pack_sel and pack_sel != "(Elige un pack)":
        pack_codigo = pack_sel

        # packs si esta persona también entra a este pack
        packs_potenciales = set(packs_actuales)
        packs_potenciales.add(pack_sel)
        num_pot = len(packs_potenciales)
        cap_pot = capacidad_pack(num_pot)
        hay_no_alc, hay_cerv_vino = flags_packs(packs_potenciales)

        if num_pot > 4:
            st.error(
                "Con este pack se pasarían de 4 packs distintos. "
                "Elige uno de los packs que ya existen."
            )

        if num_pot == 4 and (not hay_no_alc or not hay_cerv_vino):
            st.warning(
                "Para tener 4 packs distintos, debe haber al menos un pack sin alcohol "
                "y al menos un pack de cerveza o vino. Con esta combinación no se cumple."
            )

        personas_actuales_pack = 0
        if not df_aportes.empty:
            personas_actuales_pack = df_aportes.loc[
                df_aportes["pack_codigo"] == pack_sel, "nombre"
            ].nunique()

        vacantes = max(0, cap_pot - personas_actuales_pack)

        st.markdown(
            f"Actualmente este pack tiene <strong>{personas_actuales_pack}</strong> persona(s) registrada(s). "
            f"Este pack puede tener hasta <strong>{cap_pot}</strong> personas. "
            f"Hay espacio para <strong>{vacantes}</strong> más (contándote a ti).",
            unsafe_allow_html=True,
        )

        meta = PACKS.get(pack_sel, {})
        detalle = meta.get("detalle", "")
        if detalle:
            st.markdown(f"**¿Qué implica este pack?** {detalle}")

        # definimos una unidad simple para el resumen de bebidas
        tipo = meta.get("tipo", "alcoholico")
        base = meta.get("base", "")
        if tipo == "alcoholico":
            beb_alc_final = base if base else "Bebida alcohólica"
            cant_beb_alc_final = 1
            beb_noalc_final = ""
            cant_beb_noalc_final = 0
        else:
            beb_alc_final = ""
            cant_beb_alc_final = 0
            beb_noalc_final = "Pack sin alcohol / ingredientes"
            cant_beb_noalc_final = 1

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

        # Validación de pack
        if not pack_codigo:
            st.error("Elige un pack de bebidas.")
            st.stop()

        # packs potenciales con este registro
        packs_potenciales = set(packs_actuales)
        packs_potenciales.add(pack_codigo)
        num_pot = len(packs_potenciales)
        cap_pot = capacidad_pack(num_pot)
        hay_no_alc, hay_cerv_vino = flags_packs(packs_potenciales)

        if num_pot > 4:
            st.error(
                "Con este pack se pasarían de 4 packs distintos. "
                "Por favor, elige uno de los packs ya existentes."
            )
            st.stop()

        if num_pot == 4 and (not hay_no_alc or not hay_cerv_vino):
            st.error(
                "Para tener 4 packs distintos debe haber al menos un pack sin alcohol "
                "y al menos un pack de cerveza o vino. Con esta combinación no se cumple."
            )
            st.stop()

        personas_actuales_pack = 0
        if not df_aportes.empty:
            personas_actuales_pack = df_aportes.loc[
                df_aportes["pack_codigo"] == pack_codigo, "nombre"
            ].nunique()

        if personas_actuales_pack >= cap_pot:
            st.error("Este pack ya llegó a su máximo de personas. Elige otro pack.")
            st.stop()

        if (not beb_alc_final and not beb_noalc_final) or (
            beb_alc_final and cant_beb_alc_final <= 0
        ) or (beb_noalc_final and cant_beb_noalc_final <= 0):
            st.error("Hubo un problema al leer tu pack. Vuelve a seleccionarlo.")
            st.stop()

        nuevo = {
            "nombre": nombre.strip(),
            "piqueo": piqueo_final,
            "tipo_piqueo": tipo_piqueo_final,
            "cant_piqueo": int(cant_piqueo),
            "bebida_alcoholica": beb_alc_final,
            "cant_bebida_alcoholica": int(cant_beb_alc_final),
            "bebida_no_alcoholica": beb_noalc_final,
            "cant_bebida_no_alcoholica": int(cant_beb_noalc_final),
            "pack_codigo": pack_codigo,
        }

        df_aportes = pd.concat([df_aportes, pd.DataFrame([nuevo])], ignore_index=True)
        guardar_aportes(df_aportes)

        msg = f"¡Listo, {nombre}! Llevarás *{int(cant_piqueo)}* de *{piqueo_final}*"
        if beb_alc_final:
            if "cerveza" in normalizar(beb_alc_final):
                msg += f", *{cant_beb_alc_final}* aporte(s) de *{beb_alc_final}*"
            else:
                msg += f", *{cant_beb_alc_final}* aporte(s) de *{beb_alc_final}*"
        if beb_noalc_final:
            msg += f", y *{cant_beb_noalc_final}* de *{beb_noalc_final}*"

        msg += f" (Pack elegido: {pack_codigo})."
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

    # ---------- RESUMEN DE PACKS DE BEBIDAS ----------
    st.markdown("---")
    st.subheader("🍹 Resumen de packs de bebidas")

    df_packs, num_packs, hay_no_alc, hay_cerv_vino = resumen_packs(df_aportes)

    if df_packs.empty:
        st.markdown(
            "<p style='color:#777;'>Todavía nadie ha registrado packs de bebidas.</p>",
            unsafe_allow_html=True,
        )
    else:
        st.dataframe(df_packs, use_container_width=True, hide_index=True)

        texto_extra = (
            f"<br>Actualmente hay <strong>{num_packs}</strong> pack(s) de bebidas distintos registrados."
        )
        if num_packs > 4:
            texto_extra += " Esto supera el límite sugerido, revisen si pueden concentrar packs."
        elif num_packs > 3 and not hay_no_alc:
            texto_extra += " Consideren que al menos un pack debería ser sin alcohol."
        elif num_packs == 4 and not hay_cerv_vino:
            texto_extra += " Para 4 packs se espera que uno sea de cerveza o vino."

        st.markdown(
            f"""
            <div style="margin-top:6px;font-size:0.9rem;color:#555;text-align:justify;">
            💡 Cada persona elige un pack y se suma a ese grupo. 
            Las personas del mismo pack se organizan entre ellas para repartir qué lleva cada una 
            y dividir gastos de manera justa.
            {texto_extra}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---------- TRAGOS POSIBLES ----------
    st.markdown("---")
    st.subheader("🍸 Tragos posibles con lo que ya hay")

    tokens = ingredientes_disponibles(df_aportes)
    if not tokens:
        st.markdown(
            "<p style='color:#777;'>Aún no hay suficientes bebidas/ingredientes registrados para sugerir tragos.</p>",
            unsafe_allow_html=True,
        )
    else:
        for base, recetas in RECIPES.items():
            base_token = normalizar(base)
            if base_token not in tokens:
                continue
            st.markdown(f"*Con {base.lower()} se puede preparar:*")
            for nombre_trago, reqs in recetas.items():
                faltan = [r for r in reqs if normalizar(r) not in tokens]
                if not faltan:
                    st.markdown(f"- ✅ {nombre_trago}")
                else:
                    st.markdown(f"- ℹ️ {nombre_trago}: faltarían *{', '.join(faltan)}*")

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
                "bebida_alcoholica": "Bebida alcohólica (base)",
                "cant_bebida_alcoholica": "Aportes beb. alcohólica",
                "bebida_no_alcoholica": "Bebida no alcohólica / ingrediente",
                "cant_bebida_no_alcoholica": "Aportes sin alcohol",
                "pack_codigo": "Pack elegido",
            },
            inplace=True,
        )

        st.dataframe(df_mostrar, use_container_width=True, hide_index=True)

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