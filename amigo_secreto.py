import csv
from pathlib import Path

import pandas as pd
import streamlit as st

# ---------- CONFIGURACIÓN ----------
ARCHIVO_APORTES = Path("aportes.csv")
IMAGEN_PORTADA = "portada_posada.jpeg"

PARTICIPANTES = [
    "Katherine Silvestre", "Marden Ferruzo", "Rocio Dominguez", "George Aliaga",
    "Janet Rivera", "Ana Raez", "Israel Juarez", "Luis Moreano",
    "Yessevel Calvo", "Yelitza Arias", "Eduardo Pinto", "Millary Antunez",
    "Manuel Reyes", "Vladimir Tucto", "Rocio Arango", "Axel Fuentes",
    "Camila Alva", "Ricardo Céspedes",
]

LISTA_PIQUEOS = [
    "Alfajores", "Petipan de pollo", "Empanaditas surtidas", "Cheetos y chizitos",
    "Waffers y dulces", "Minitriples de jamón y queso", "Tamal",
    "Papás, chifles, camotes y chifles", "Otro (indicar)"
]

LISTA_BEBIDAS_ALC = ["Pisco", "Cerveza", "Vino tinto", "Ron", "Otro (indicar)"]
LISTA_BEBIDAS_NO_ALC = ["Gaseosa", "Everest", "Agua", "Hielo", "Limón", "Otro (indicar)"]

PIQUEO_TIPO_DEFAULT = {
    "Alfajores": "Dulce", "Petipan de pollo": "Preparado",
    "Empanaditas surtidas": "Preparado", "Cheetos y chizitos": "Snack en bolsa",
    "Waffers y dulces": "Dulce", "Minitriples de jamón y queso": "Preparado",
    "Tamal": "Preparado", "Papás, chifles, camotes y chifles": "Snack en bolsa"
}

PIQUEO_UNIDAD = {
    "Alfajores": "unidades (12–25)", "Petipan de pollo": "fracción de ciento",
    "Empanaditas surtidas": "fracción de ciento", "Cheetos y chizitos": "bolsas grandes",
    "Waffers y dulces": "porciones / paquetitos",
    "Minitriples de jamón y queso": "fracción de ciento",
    "Tamal": "unidades", "Papás, chifles, camotes y chifles": "bolsas grandes"
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

PIQUEO_CUPOS_MAX = {
    "Alfajores": 3, "Petipan de pollo": 2, "Empanaditas surtidas": 3,
    "Cheetos y chizitos": 2, "Waffers y dulces": 2,
    "Minitriples de jamón y queso": 2, "Tamal": 2,
    "Papás, chifles, camotes y chifles": 3
}

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
    "Cheetos y chizitos": {"unit_type": "bags", "person_max": 3},
    "Papás, chifles, camotes y chifles": {"unit_type": "bags", "person_max": 3},
    "Tamal": {"unit_type": "units", "person_max": 4},
    "Waffers y dulces": {"unit_type": "units", "person_max": 12},
}

BAG_PIQUEOS = ["Cheetos y chizitos", "Papás, chifles, camotes y chifles"]
MAX_BOLSAS_GRUPO = 6

RECIPES = {
    "Pisco": {
        "Chilcano clásico": ["pisco", "ginger ale", "limón", "hielo"],
        "Chilcano de maracuyá": ["pisco", "maracuyá", "limón", "azúcar", "ginger ale", "hielo"],
    },
    "Vino tinto": {
        "Tinto de verano": ["vino tinto", "gaseosa", "hielo"],
        "Sangría": ["vino tinto", "frutas", "gaseosa", "azúcar", "hielo"],
    },
    "Ron": {
        "Mojito": ["ron", "hierbabuena", "limón", "azúcar", "agua con gas", "hielo"],
        "Cuba libre": ["ron", "gaseosa cola", "hielo", "limón"],
    },
    "Whisky": {"Whisky solo": ["whisky", "hielo"]},
    "Cerveza": {"Cerveza sola": ["cerveza"]},
}

BEBIDA_ALC_TOKENS = {
    "pisco": "pisco", "cerveza": "cerveza",
    "vino tinto": "vino tinto", "vino": "vino tinto",
    "ron": "ron",
}

BEBIDA_NOALC_TOKENS = {
    "gaseosa": "gaseosa", "everest": "ginger ale",
    "agua": "agua", "hielo": "hielo", "limón": "limón",
}

# -------- UTILIDADES --------

def normalizar(s: str) -> str:
    return s.strip().lower() if isinstance(s, str) else ""

def safe_int(v):
    try:
        val = pd.to_numeric(v, errors="coerce")
        return int(val) if not pd.isna(val) else 0
    except:
        return 0

def cargar_aportes():
    columnas = [
        "nombre", "piqueo", "tipo_piqueo", "cant_piqueo",
        "bebida_alcoholica", "cant_bebida_alcoholica",
        "bebida_no_alcoholica", "cant_bebida_no_alcoholica",
    ]
    if ARCHIVO_APORTES.exists():
        df = pd.read_csv(ARCHIVO_APORTES, dtype=str)
        for c in columnas:
            if c not in df.columns:
                df[c] = ""
        return df[columnas]
    else:
        return pd.DataFrame(columns=columnas)

def guardar_aportes(df):
    df.to_csv(ARCHIVO_APORTES, index=False, encoding="utf-8")

def contar_piqueos(df):
    conteo = {p: 0 for p in PIQUEO_CUPOS_MAX.keys()}
    if not df.empty:
        for p in df["piqueo"]:
            if p in conteo:
                conteo[p] += 1
    return conteo

def contar_bolsas(df):
    if df.empty:
        return 0
    df2 = df.copy()
    df2["cant_piqueo"] = df2["cant_piqueo"].apply(safe_int)
    mask = (df2["piqueo"].isin(BAG_PIQUEOS)) | (df2["tipo_piqueo"] == "Snack en bolsa")
    return int(df2.loc[mask, "cant_piqueo"].sum())

def obtener_cantidad_piqueo(piqueo):
    if piqueo not in PIQUEO_CONFIG:
        label = "Cantidad (unidades / porciones):"
        cant = st.number_input(label, min_value=0, step=1)
        return cant, label

    cfg = PIQUEO_CONFIG[piqueo]
    tipo = cfg["unit_type"]

    if tipo == "fraction_ciento":
        label = "Cantidad (fracción de ciento):"
        opcion = st.selectbox(label, list(cfg["fraction_options"].keys()))
        return cfg["fraction_options"][opcion], label

    if tipo == "bags":
        label = "Cantidad (bolsas grandes):"
        cant = st.number_input(label, min_value=0, max_value=cfg["person_max"], step=1)
        return cant, label

    label = "Cantidad (unidades):"
    cant = st.number_input(label, min_value=0, max_value=cfg["person_max"], step=1)
    return cant, label

def ingredientes_disponibles(df):
    tokens = set()
    if df.empty:
        return tokens
    df2 = df.copy()
    for _, row in df2.iterrows():
        alc = normalizar(row["bebida_alcoholica"])
        if alc in BEBIDA_ALC_TOKENS and safe_int(row["cant_bebida_alcoholica"]) > 0:
            tokens.add(BEBIDA_ALC_TOKENS[alc])

        noalc = normalizar(row["bebida_no_alcoholica"])
        if noalc in BEBIDA_NOALC_TOKENS and safe_int(row["cant_bebida_no_alcoholica"]) > 0:
            tokens.add(BEBIDA_NOALC_TOKENS[noalc])
    return tokens

def resumen_bebidas(df):
    if df.empty:
        return 0, 0
    df2 = df.copy()
    df2["cant_bebida_alcoholica"] = df2["cant_bebida_alcoholica"].apply(safe_int)
    df2["cant_bebida_no_alcoholica"] = df2["cant_bebida_no_alcoholica"].apply(safe_int)
    return int(df2["cant_bebida_alcoholica"].sum()), int(df2["cant_bebida_no_alcoholica"].sum())

def estado_rango(total, minimo, maximo):
    if total < minimo: return "Por debajo del rango ⚠️"
    if total > maximo: return "Por encima del rango ⚠️"
    return "Dentro del rango ✔️"


# ---------- APP ----------
def main():
    st.set_page_config(page_title="Aportes Posada 2025", page_icon="🎄")

    # Estilos
    st.markdown("""
        <style>
        html, body, .stApp { color-scheme: light !important; }
        .stApp { background: #fff7f0; }
        </style>
    """, unsafe_allow_html=True)

    if Path(IMAGEN_PORTADA).exists():
        st.image(IMAGEN_PORTADA, use_column_width=True)

    st.markdown("<h2 style='text-align:center;'>🎄 Aportes Posada Territorial 2025</h2>", unsafe_allow_html=True)

    # --- SUGERENCIA GENERAL NUEVA ---
    st.markdown("""
    <div style="
        background-color:#fff2e6;
        padding:14px 20px;
        border-radius:10px;
        border:1px solid #f5c09a;
        font-size:0.97rem;
        color:#5a3c2c;
        margin-top:15px;
        text-align:justify;">

        ⚠️ <strong>Sugerencia general de piqueos y bebidas para 18 personas</strong><br><br>

        <strong>🧀 Piqueos:</strong><br>
        Que los piqueos vengan en presentaciones grandes:
        <ul>
            <li><strong>Snacks:</strong> máximo 6 bolsas grandes en total.</li>
            <li><strong>Dulces/preparados:</strong> porciones suficientes para todos.</li>
        </ul>

        <strong>🥤 Bebidas sugeridas:</strong>
        <ul>
            <li><strong>🍻 Cerveza:</strong> 5–6 six-packs (24–36 cervezas).</li>
            <li><strong>🍷 Vino tinto:</strong> 4 botellas (3 si es solo para tragos).</li>
            <li><strong>🥃 Licores:</strong> 3–4 botellas combinadas (pisco + ron + whisky/vodka).</li>
            <li><strong>🥤 Sin alcohol:</strong> 6 botellas grandes (gaseosa, ginger ale, agua).</li>
        </ul>

    </div>
    """, unsafe_allow_html=True)

    df = cargar_aportes()
    conteo = contar_piqueos(df)

    # --- FORMULARIO ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📝 Registrar aporte")

    nombre = st.selectbox("Selecciona tu nombre:", sorted(PARTICIPANTES))

    st.markdown("#### 🧀 Piqueo")
    piqueo_sel = st.radio("¿Qué piqueo vas a llevar?", LISTA_PIQUEOS, index=None)

    if piqueo_sel == "Otro (indicar)":
        piqueo_otro = st.text_input("Indica el piqueo:")
        tipo_piqueo = st.radio("Tipo:", ["Snack en bolsa", "Preparado", "Dulce"], horizontal=True)
    else:
        piqueo_otro = ""
        tipo_piqueo = PIQUEO_TIPO_DEFAULT.get(piqueo_sel, "")

    cant_piqueo = 0
    if piqueo_sel:
        cant_piqueo, _ = obtener_cantidad_piqueo(piqueo_sel)

    # BEBIDAS ALC
    st.markdown("#### 🍷 Bebida alcohólica (opcional)")
    beb_alc_raw = st.selectbox("Elige:", ["(Sin bebida alcohólica)"] + LISTA_BEBIDAS_ALC)
    beb_alc_sel = "" if beb_alc_raw == "(Sin bebida alcohólica)" else beb_alc_raw

    if beb_alc_sel == "Otro (indicar)":
        beb_alc_otro = st.text_input("¿Cuál bebida alcohólica?")
    else:
        beb_alc_otro = ""

    if beb_alc_sel == "Cerveza":
        cant_beb_alc = st.number_input("Cantidad (six-pack):", min_value=0, step=1)
    elif beb_alc_sel:
        cant_beb_alc = st.number_input("Cantidad (botellas):", min_value=0, step=1)
    else:
        cant_beb_alc = 0

    # BEBIDAS NO ALC
    st.markdown("#### 🥤 Bebida no alcohólica / ingredientes")
    beb_noalc_raw = st.selectbox("Elige:", ["(Sin bebida no alcohólica / ingrediente)"] + LISTA_BEBIDAS_NO_ALC)
    beb_noalc_sel = "" if beb_noalc_raw == "(Sin bebida no alcohólica / ingrediente)" else beb_noalc_raw

    if beb_noalc_sel == "Otro (indicar)":
        beb_noalc_otro = st.text_input("¿Cuál bebida / ingrediente?")
    else:
        beb_noalc_otro = ""

    if beb_noalc_sel:
        if beb_noalc_sel == "Hielo":
            label_noalc = "Cantidad (bolsas de hielo):"
        elif beb_noalc_sel == "Gaseosa":
            label_noalc = "Cantidad (botellas):"
        elif beb_noalc_sel == "Everest":
            label_noalc = "Cantidad (botellas / latas):"
        elif beb_noalc_sel == "Agua":
            label_noalc = "Cantidad (litros o botellas):"
        elif beb_noalc_sel == "Limón":
            label_noalc = "Cantidad (unidades):"
        else:
            label_noalc = "Cantidad:"
        cant_beb_noalc = st.number_input(label_noalc, min_value=0, step=1)
    else:
        cant_beb_noalc = 0

    enviado = st.button("✅ Registrar aporte", use_container_width=True)

    # ---------- PROCESAR ----------
    if enviado:
        if not nombre.strip():
            st.error("Selecciona tu nombre.")
            st.stop()

        if not df.empty and nombre in df["nombre"].values:
            st.error("Ya registraste tu aporte antes.")
            st.stop()

        if not piqueo_sel:
            st.error("Debes elegir un piqueo.")
            st.stop()

        # Procesar piqueo
        if piqueo_sel == "Otro (indicar)":
            if not piqueo_otro.strip():
                st.error("Indica qué piqueo llevarás.")
                st.stop()
            if not tipo_piqueo:
                st.error("Elige si es snack en bolsa, preparado o dulce.")
                st.stop()
            piqueo_final = piqueo_otro.strip()
            tipo_piqueo_final = tipo_piqueo
        else:
            piqueo_final = piqueo_sel
            tipo_piqueo_final = PIQUEO_TIPO_DEFAULT.get(piqueo_sel, "")

            # Validar cupos
            if piqueo_final in PIQUEO_CUPOS_MAX:
                if conteo[piqueo_final] >= PIQUEO_CUPOS_MAX[piqueo_final]:
                    st.error("Ese piqueo ya alcanzó el máximo de personas permitidas.")
                    st.stop()

        if cant_piqueo <= 0:
            st.error("Indica una cantidad válida para el piqueo.")
            st.stop()

        # Límite global de snacks en bolsa
        if tipo_piqueo_final == "Snack en bolsa":
            bolsas_actuales = contar_bolsas(df)
            if bolsas_actuales + cant_piqueo > MAX_BOLSAS_GRUPO:
                st.error(
                    f"Supera el límite total permitido de {MAX_BOLSAS_GRUPO} bolsas grandes de snacks."
                )
                st.stop()

        # Procesar bebida alcohólica
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
                st.error("Indica una cantidad válida para la bebida alcohólica.")
                st.stop()
            cant_beb_alc_final = int(cant_beb_alc)

        # Procesar bebida no alcohólica
        if not beb_noalc_sel:
            beb_noalc_final = ""
            cant_beb_noalc_final = 0
        else:
            if beb_noalc_sel == "Otro (indicar)":
                if not beb_noalc_otro.strip():
                    st.error("Especifica la bebida/ingrediente.")
                    st.stop()
                beb_noalc_final = beb_noalc_otro.strip()
            else:
                beb_noalc_final = beb_noalc_sel

            if cant_beb_noalc <= 0:
                st.error("Indica una cantidad válida para la bebida no alcohólica.")
                st.stop()
            cant_beb_noalc_final = int(cant_beb_noalc)

        # Validar que haya por lo menos una bebida
        if (not beb_alc_final or cant_beb_alc_final <= 0) and \
           (not beb_noalc_final or cant_beb_noalc_final <= 0):
            st.error("Debes registrar al menos una bebida (alcohólica o no alcohólica).")
            st.stop()

        # Crear registro final
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

        df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
        guardar_aportes(df)

        # Mensaje final
        msg = f"¡Listo, {nombre}! Llevarás **{int(cant_piqueo)}** de **{piqueo_final}**"
        if beb_alc_final:
            if beb_alc_final.lower() == "cerveza":
                msg += f", **{cant_beb_alc_final}** six-pack de **{beb_alc_final}**"
            else:
                msg += f", **{cant_beb_alc_final}** botellas de **{beb_alc_final}**"
        if beb_noalc_final:
            msg += f", y **{cant_beb_noalc_final}** de **{beb_noalc_final}**"

        st.success(msg + " 🎉")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- CUPOS DE PIQUEOS ----------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🍽️ Cupos y límites por piqueo")

    filas = []
    for p, maximo in PIQUEO_CUPOS_MAX.items():
        usados = conteo[p]
        filas.append({
            "Piqueo": p,
            "Tipo": PIQUEO_TIPO_DEFAULT.get(p, ""),
            "Unidad": PIQUEO_UNIDAD.get(p, ""),
            "Máx. sugerido": PIQUEO_MAX_TEXTO.get(p, ""),
            "Personas registradas": usados,
            "Estado": "Disponible ✔️" if usados < maximo else "Lleno ❌",
        })

    st.dataframe(pd.DataFrame(filas), hide_index=True, use_container_width=True)

    bolsas_actuales = contar_bolsas(df)
    st.markdown(
        f"""
        <div style="font-size:0.9rem;color:#555;">
        🧃 <strong>Snacks en bolsa:</strong> máximo {MAX_BOLSAS_GRUPO} bolsas grandes.<br>
        Actualmente hay <strong>{bolsas_actuales}</strong>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------- RESUMEN DE BEBIDAS ----------
    st.markdown("---")
    st.subheader("🥤 Resumen de bebidas registradas")

    total_alc, total_noalc = resumen_bebidas(df)

    RANGO_ALC = (6, 15)
    RANGO_NOALC = (10, 22)

    df_beb = pd.DataFrame([
        {
            "Tipo": "Bebidas alcohólicas",
            "Cantidad registrada": total_alc,
            "Rango sugerido": f"{RANGO_ALC[0]}–{RANGO_ALC[1]}",
            "Estado": estado_rango(total_alc, *RANGO_ALC),
        },
        {
            "Tipo": "Bebidas no alcohólicas / ingredientes",
            "Cantidad registrada": total_noalc,
            "Rango sugerido": f"{RANGO_NOALC[0]}–{RANGO_NOALC[1]}",
            "Estado": estado_rango(total_noalc, *RANGO_NOALC),
        },
    ])

    st.dataframe(df_beb, hide_index=True, use_container_width=True)

    # ---------- TRAGOS POSIBLES ----------
    st.markdown("---")
    st.subheader("🍹 Tragos posibles con lo que ya hay")

    tokens = ingredientes_disponibles(df)

    if not tokens:
        st.markdown("<p style='color:#777;'>Aún no hay suficientes ingredientes.</p>", unsafe_allow_html=True)
    else:
        for base, recetas in RECIPES.items():
            if normalizar(base) not in tokens:
                continue
            st.markdown(f"**Con {base.lower()} se puede preparar:**")
            for trago, reqs in recetas.items():
                faltan = [x for x in reqs if x not in tokens]
                if not faltan:
                    st.markdown(f"- ✔️ {trago}")
                else:
                    st.markdown(f"- ℹ️ {trago}: faltan {', '.join(faltan)}")

    # ---------- LISTA COMPLETA DE APORTES ----------
    if not df.empty:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📋 Aportes registrados")

        df_mostrar = df.copy()
        for c in ["cant_piqueo", "cant_bebida_alcoholica", "cant_bebida_no_alcoholica"]:
            df_mostrar[c] = df_mostrar[c].apply(safe_int)

        df_mostrar.columns = [
            "Nombre", "Piqueo", "Tipo de piqueo", "Cant. piqueo",
            "Bebida alcohólica", "Cant. beb. alc.",
            "Bebida no alcohólica / ingrediente", "Cant. beb. no alc."
        ]

        st.dataframe(df_mostrar, hide_index=True, use_container_width=True)

        # Quiénes faltan
        registrados = set(df["nombre"])
        faltan = [p for p in sorted(PARTICIPANTES) if p not in registrados]

        if faltan:
            st.markdown(
                f"""
                <div style="
                    background-color:#ffecec;
                    padding:10px 14px;
                    border-radius:8px;
                    border:1px solid #ff4d4f;
                    color:#a8071a;">
                    🔴 <strong>Faltan registrar:</strong><br>{", ".join(faltan)}
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()