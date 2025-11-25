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
        "pack_rol",
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

def resumen_bebidas(df_aportes: pd.DataFrame):
    if df_aportes.empty:
        return 0, 0
    df_tmp = df_aportes.copy()
    df_tmp["cant_bebida_alcoholica"] = df_tmp["cant_bebida_alcoholica"].apply(safe_int)
    df_tmp["cant_bebida_no_alcoholica"] = df_tmp["cant_bebida_no_alcoholica"].apply(safe_int)
    total_alc = int(df_tmp["cant_bebida_alcoholica"].sum())
    total_noalc = int(df_tmp["cant_bebida_no_alcoholica"].sum())
    return total_alc, total_noalc

def resumen_packs(df_aportes: pd.DataFrame):
    """Resumen por pack: personas, vacantes, etc."""
    if df_aportes.empty:
        return pd.DataFrame(), 0, False

    df = df_aportes.copy()
    df["pack_codigo"] = df["pack_codigo"].astype(str).str.strip()
    df = df[df["pack_codigo"] != ""]
    if df.empty:
        return pd.DataFrame(), 0, False

    resumen = []
    for pack, sub in df.groupby("pack_codigo"):
        personas = sub["nombre"].nunique()
        vacantes = max(0, 3 - personas)
        estado = "Completo ✅" if personas == 3 else f"En formación (faltan {vacantes})"
        resumen.append(
            {
                "Pack": pack,
                "Personas en el pack": personas,
                "Vacantes (de 3)": vacantes,
                "Estado": estado,
            }
        )

    df_res = pd.DataFrame(resumen).sort_values("Pack")
    num_packs = df_res.shape[0]
    packs_lista = df_res["Pack"].tolist()

    hay_cerveza_y_sangria = any("Cerveza" in p for p in packs_lista) and any(
        "Sangría" in p or "Sangria" in p for p in packs_lista
    )
    return df_res, num_packs, hay_cerveza_y_sangria


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

<ul> <li><strong>Piqueos:</strong> 
Se lleva en <strong>presentación grande</strong> 
(bandejas, fracciones de ciento o bolsas grandes). 
Hay cupos para cada tipo de piqueo y, en total, 
trataremos de no pasar de <strong>6 bolsas grandes</strong> de snacks.</li> 
<li><strong>Bebidas:</strong> Funcionan por <strong>packs</strong>. 
Cada pack se comparte entre <strong>3 personas</strong> (roles A, B y C). 
<br>Ejemplo: una persona lleva el pisco, otra el ginger ale y otra el limón + hielo. 
</li> <li>Si varias personas eligen el <strong>mismo pack</strong>, 
forman un mini-equipo y deben <strong>coordinar entre ellas</strong> para dividir gastos 
y asegurarse de completar todo (botellas, mezclas, hielo, etc.).</li>
 <li>No necesitamos demasiados packs distintos. <br>Si 
 los packs son sencillos, bastan <strong>3 packs</strong>
 diferentes para cubrir a los 18. <br>Si agregamos también
 un pack de <strong>Cerveza</strong> y uno de <strong>Sangría</strong>, 
 como máximo tendríamos <strong>4 packs</strong> en total.</li> <li>Las 
 cervezas se pueden enfriar en la <strong>refri del local</strong>.</li> </ul> </div>
            
         
            
            
           
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

    # ---------- PACKS DE BEBIDAS (SIN MODO MANUAL) ----------
    PACKS = {
        "A1 - Chilcano clásico": {
            "roles": {
                "A": {
                    "beb_alc": "Pisco",
                    "cant_beb_alc": 1,
                    "beb_noalc": "",
                    "cant_beb_noalc": 0,
                    "detalle": "1 botella de pisco (base alcohólica para chilcanos).",
                },
                "B": {
                    "beb_alc": "",
                    "cant_beb_alc": 0,
                    "beb_noalc": "Ginger ale",
                    "cant_beb_noalc": 1,
                    "detalle": "1 botella de ginger ale.",
                },
                "C": {
                    "beb_alc": "",
                    "cant_beb_alc": 0,
                    "beb_noalc": "Limón y hielo",
                    "cant_beb_noalc": 1,
                    "detalle": "Limón + 1 bolsa de hielo.",
                },
            },
            "equipo": "",
        },
        "A3 - Pisco sour clásico": {
            "roles": {
                "A": {
                    "beb_alc": "Pisco",
                    "cant_beb_alc": 1,
                    "beb_noalc": "",
                    "cant_beb_noalc": 0,
                    "detalle": "1 botella de pisco (base para pisco sour).",
                },
                "B": {
                    "beb_alc": "",
                    "cant_beb_alc": 0,
                    "beb_noalc": "Huevos (docena) y azúcar",
                    "cant_beb_noalc": 1,
                    "detalle": "1 docena de huevos + azúcar.",
                },
                "C": {
                    "beb_alc": "",
                    "cant_beb_alc": 0,
                    "beb_noalc": "Limón y hielo",
                    "cant_beb_noalc": 1,
                    "detalle": "Limón + hielo.",
                },
            },
            "equipo": "⚠️ Este pack requiere licuadora o coctelera.",
        },
        "B1 - Mojito": {
            "roles": {
                "A": {
                    "beb_alc": "Ron",
                    "cant_beb_alc": 1,
                    "beb_noalc": "",
                    "cant_beb_noalc": 0,
                    "detalle": "1 botella de ron.",
                },
                "B": {
                    "beb_alc": "",
                    "cant_beb_alc": 0,
                    "beb_noalc": "Agua con gas",
                    "cant_beb_noalc": 2,
                    "detalle": "2 botellas de agua con gas.",
                },
                "C": {
                    "beb_alc": "",
                    "cant_beb_alc": 0,
                    "beb_noalc": "Hierbabuena, limón, azúcar",
                    "cant_beb_noalc": 1,
                    "detalle": "Hierbabuena + limón + azúcar (para mojito).",
                },
            },
            "equipo": "",
        },
        "B2 - Cuba libre": {
            "roles": {
                "A": {
                    "beb_alc": "Ron",
                    "cant_beb_alc": 1,
                    "beb_noalc": "",
                    "cant_beb_noalc": 0,
                    "detalle": "1 botella de ron.",
                },
                "B": {
                    "beb_alc": "",
                    "cant_beb_alc": 0,
                    "beb_noalc": "Gaseosa cola",
                    "cant_beb_noalc": 1,
                    "detalle": "1 botella de gaseosa cola.",
                },
                "C": {
                    "beb_alc": "",
                    "cant_beb_alc": 0,
                    "beb_noalc": "Limón",
                    "cant_beb_noalc": 1,
                    "detalle": "Limón para acompañar.",
                },
            },
            "equipo": "",
        },
        "C1 - Sangría clásica": {
            "roles": {
                "A": {
                    "beb_alc": "Vino tinto",
                    "cant_beb_alc": 1,
                    "beb_noalc": "",
                    "cant_beb_noalc": 0,
                    "detalle": "1 botella de vino tinto.",
                },
                "B": {
                    "beb_alc": "",
                    "cant_beb_alc": 0,
                    "beb_noalc": "Gaseosa",
                    "cant_beb_noalc": 1,
                    "detalle": "1 botella de gaseosa.",
                },
                "C": {
                    "beb_alc": "",
                    "cant_beb_alc": 0,
                    "beb_noalc": "Fruta y azúcar",
                    "cant_beb_noalc": 1,
                    "detalle": "Frutas picadas + azúcar.",
                },
            },
            "equipo": "",
        },
        "D1 - Pack cerveza": {
            "roles": {
                "A": {
                    "beb_alc": "Cerveza (six-pack)",
                    "cant_beb_alc": 1,
                    "beb_noalc": "",
                    "cant_beb_noalc": 0,
                    "detalle": "1 six-pack de cerveza.",
                },
                "B": {
                    "beb_alc": "Cerveza (six-pack)",
                    "cant_beb_alc": 1,
                    "beb_noalc": "",
                    "cant_beb_noalc": 0,
                    "detalle": "1 six-pack de cerveza adicional.",
                },
                "C": {
                    "beb_alc": "",
                    "cant_beb_alc": 0,
                    "beb_noalc": "Hielo",
                    "cant_beb_noalc": 1,
                    "detalle": "Bolsas de hielo para las cervezas.",
                },
            },
            "equipo": "Las cervezas se pueden enfriar en la refri del local.",
        },
        "E1 - Refrescos sin alcohol": {
            "roles": {
                "A": {
                    "beb_alc": "",
                    "cant_beb_alc": 0,
                    "beb_noalc": "Gaseosa",
                    "cant_beb_noalc": 1,
                    "detalle": "1 botella grande de gaseosa.",
                },
                "B": {
                    "beb_alc": "",
                    "cant_beb_alc": 0,
                    "beb_noalc": "Agua",
                    "cant_beb_noalc": 1,
                    "detalle": "Agua (botella grande o varios litros).",
                },
                "C": {
                    "beb_alc": "",
                    "cant_beb_alc": 0,
                    "beb_noalc": "Jugo y hielo",
                    "cant_beb_noalc": 1,
                    "detalle": "Jugo o té frío + 1 bolsa de hielo.",
                },
            },
            "equipo": "",
        },
    }

    st.markdown("### 🍹 Packs de bebidas")

    pack_opciones = ["(Elige un pack)"] + list(PACKS.keys())
    pack_sel = st.selectbox(
        "Elige un pack de bebidas (cada pack es para 3 personas: roles A, B y C):",
        pack_opciones,
        key="pack_sel",
    )

    beb_alc_final = ""
    cant_beb_alc_final = 0
    beb_noalc_final = ""
    cant_beb_noalc_final = 0
    pack_codigo = ""
    pack_rol = ""
    rol_sel = None

    if pack_sel and pack_sel != "(Elige un pack)":
        pack_codigo = pack_sel
        info_pack = PACKS[pack_sel]

        # Cuántas personas ya están en este pack
        personas_actuales = 0
        if not df_aportes.empty:
            personas_actuales = df_aportes.loc[
                df_aportes["pack_codigo"] == pack_sel, "nombre"
            ].nunique()
        vacantes_actuales = max(0, 3 - personas_actuales)

        st.markdown(
            f"Actualmente este pack tiene <strong>{personas_actuales}</strong> persona(s) registrada(s). "
            f"El pack es para <strong>3 personas</strong>, así que hay espacio para "
            f"<strong>{vacantes_actuales}</strong> más (contándote a ti).",
            unsafe_allow_html=True,
        )

        if personas_actuales >= 3:
            st.error("Este pack ya está completo, elige otro pack.")
        else:
            rol_sel = st.radio(
                "¿Qué parte del pack vas a llevar?",
                ["A", "B", "C"],
                key="rol_pack",
            )
            pack_rol = rol_sel

            if info_pack.get("equipo"):
                st.warning(info_pack["equipo"])

            info_rol = info_pack["roles"].get(rol_sel)
            if info_rol:
                beb_alc_final = info_rol["beb_alc"]
                cant_beb_alc_final = info_rol["cant_beb_alc"]
                beb_noalc_final = info_rol["beb_noalc"]
                cant_beb_noalc_final = info_rol["cant_beb_noalc"]

                detalle = info_rol.get("detalle", "")
                if detalle:
                    st.markdown(f"**Tu aporte en este pack:** {detalle}")

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
        if not pack_codigo or not pack_rol:
            st.error("Elige un pack de bebidas y tu rol dentro del pack.")
            st.stop()

        # Recalcular personas en ese pack para no pasarnos de 3
        personas_actuales = 0
        if not df_aportes.empty:
            personas_actuales = df_aportes.loc[
                df_aportes["pack_codigo"] == pack_codigo, "nombre"
            ].nunique()
        if personas_actuales >= 3:
            st.error("Este pack ya llegó a 3 personas. Elige otro pack.")
            st.stop()

        if (not beb_alc_final or cant_beb_alc_final <= 0) and (
            not beb_noalc_final or cant_beb_noalc_final <= 0
        ):
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
            "pack_rol": pack_rol,
        }

        df_aportes = pd.concat([df_aportes, pd.DataFrame([nuevo])], ignore_index=True)
        guardar_aportes(df_aportes)

        msg = f"¡Listo, {nombre}! Llevarás *{int(cant_piqueo)}* de *{piqueo_final}*"
        if beb_alc_final:
            if "cerveza" in normalizar(beb_alc_final):
                msg += f", *{cant_beb_alc_final}* six-pack de *{beb_alc_final}*"
            else:
                msg += f", *{cant_beb_alc_final}* de *{beb_alc_final}*"
        if beb_noalc_final:
            msg += f", y *{cant_beb_noalc_final}* de *{beb_noalc_final}*"

        msg += f" (Pack: {pack_codigo}, rol {pack_rol})."
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

    df_packs, num_packs, hay_cerveza_y_sangria = resumen_packs(df_aportes)

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
            texto_extra += " Es bastante variedad, revisen si realmente necesitan tantos packs diferentes. 😉"
        elif num_packs > 3 and not hay_cerveza_y_sangria:
            texto_extra += " Recuerden que la idea general es no pasar de 3 packs si son sencillos."
        elif num_packs == 4 and hay_cerveza_y_sangria:
            texto_extra += " Con cerveza y sangría se acepta hasta 4 packs, pero ya es tope."

        st.markdown(
            f"""
            <div style="margin-top:6px;font-size:0.9rem;color:#555;text-align:justify;">
            💡 Cada pack está pensado para 3 personas (A, B y C).<br>
            Si ves que tu pack está en <strong>“En formación”</strong>, 
            coordina con tus compas para que se sumen dos personas más y el pack quede completo.
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
                "bebida_alcoholica": "Bebida alcohólica",
                "cant_bebida_alcoholica": "Cant. beb. alcohólica",
                "bebida_no_alcoholica": "Bebida no alcohólica / ingrediente",
                "cant_bebida_no_alcoholica": "Cant. beb. no alcohólica / ingr.",
                "pack_codigo": "Pack elegido",
                "pack_rol": "Rol en el pack",
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