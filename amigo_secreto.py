import csv
from pathlib import Path

import pandas as pd
import streamlit as st

# ---------- CONFIGURACIÓN ----------
ARCHIVO_APORTES = Path("aportes.csv")

# Imagen de portada (debe estar en el mismo repo)
IMAGEN_PORTADA = "portada_posada.jpeg"  # cambia el nombre si quieres

# Lista fija de participantes (menú desplegable)
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

# Listas por categoría (como la imagen que mandaste)
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


# ---------- FUNCIONES AUXILIARES ----------

def cargar_aportes():
    """Lee el archivo de aportes (si existe) y retorna un DataFrame."""
    if ARCHIVO_APORTES.exists():
        return pd.read_csv(ARCHIVO_APORTES, dtype=str)
    else:
        return pd.DataFrame(
            columns=[
                "nombre",
                "piqueo",
                "cant_piqueo",
                "bebida_alcoholica",
                "cant_bebida_alcoholica",
                "bebida_no_alcoholica",
                "cant_bebida_no_alcoholica",
            ]
        )


def guardar_aportes(df_aportes: pd.DataFrame):
    """Guarda los aportes en CSV."""
    df_aportes.to_csv(ARCHIVO_APORTES, index=False, encoding="utf-8")


# ---------- APP STREAMLIT ----------

def main():
    st.set_page_config(
        page_title="Aportes Posada Territorial 2025",
        page_icon="🎄",
        layout="centered",
    )

    # ---- Estilos personalizados (colores, tipografía, etc.) ----
    st.markdown(
        """
        <style>
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

        /* Cuadros tipo tarjeta */
        .card {
            background-color: #ffffff;
            padding: 1.2rem 1rem;
            border-radius: 0.8rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border: 1px solid #f0e0d2;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---- Portada ----
    if Path(IMAGEN_PORTADA).exists():
        st.image(IMAGEN_PORTADA, use_column_width=True)
    st.markdown('<div class="titulo-principal">🎄 Aportes Posada Territorial 2025 🎁</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitulo">Registra tu piqueo y tus bebidas para organizar mejor la mesa ✨</div>',
        unsafe_allow_html=True,
    )

    # ---- AVISO IMPORTANTE AÑADIDO ----
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

    # Cargamos aportes actuales
    df_aportes = cargar_aportes()

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Layout: izquierda formulario, derecha tabla de referencia ----
    col_izq, col_der = st.columns([1.2, 0.8])

    # ---------- COLUMNA DERECHA: LISTA DE OPCIONES ----------
    with col_der:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📋 Lista de ideas")

        col_piq, col_alc, col_noalc = st.columns(3)
        with col_piq:
            st.markdown("**Lista de piqueos**")
            for item in LISTA_PIQUEOS:
                st.write(f"- {item}")
        with col_alc:
            st.markdown("**Bebidas alcohólicas**")
            for item in LISTA_BEBIDAS_ALC[1:]:  # saltamos "Ninguna"
                st.write(f"- {item}")
        with col_noalc:
            st.markdown("**Bebidas no alcohólicas**")
            for item in LISTA_BEBIDAS_NO_ALC[1:]:  # saltamos "Ninguna"
                st.write(f"- {item}")

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------- COLUMNA IZQUIERDA: FORMULARIO ----------
    with col_izq:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📝 Registrar tu aporte")

        with st.form("form_aporte"):
            # Nombre
            nombre = st.selectbox("Selecciona tu nombre:", PARTICIPANTES)

            # --- Piqueo ---
            st.markdown("#### 🧀 Piqueo")
            piqueo_sel = st.selectbox("¿Qué piqueo vas a llevar?", LISTA_PIQUEOS)
            piqueo_otro = ""
            if piqueo_sel == "Otro (indicar)":
                piqueo_otro = st.text_input("Indica el piqueo:")
            cant_piqueo = st.number_input(
                "Cantidad de piqueo (unidades / porciones):",
                min_value=0,
                step=1,
                value=0,
            )

            # --- Bebida alcohólica ---
            st.markdown("#### 🍷 Bebida alcohólica (opcional)")
            beb_alc_sel = st.selectbox(
                "Si llevarás bebida alcohólica, elige una:",
                LISTA_BEBIDAS_ALC,
            )
            beb_alc_otro = ""
            if beb_alc_sel == "Otro (indicar)":
                beb_alc_otro = st.text_input("Indica la bebida alcohólica:")
            cant_beb_alc = st.number_input(
                "Cantidad (botellas / six pack / unidades):",
                min_value=0,
                step=1,
                value=0,
                key="cant_beb_alc",
            )

            # --- Bebida no alcohólica ---
            st.markdown("#### 🥤 Bebida no alcohólica (opcional)")
            beb_noalc_sel = st.selectbox(
                "Si llevarás bebida no alcohólica, elige una:",
                LISTA_BEBIDAS_NO_ALC,
            )
            beb_noalc_otro = ""
            if beb_noalc_sel == "Otro (indicar)":
                beb_noalc_otro = st.text_input("Indica la bebida no alcohólica:")
            cant_beb_noalc = st.number_input(
                "Cantidad (botellas / litros / unidades):",
                min_value=0,
                step=1,
                value=0,
                key="cant_beb_noalc",
            )

            enviado = st.form_submit_button("✅ Registrar aporte")

        # ---------- PROCESAR ENVÍO ----------
        if enviado:
            # Validación nombre
            if not nombre.strip():
                st.error("Por favor selecciona tu nombre.")
                st.stop()

            # Evitar duplicados
            if not df_aportes.empty and nombre in df_aportes["nombre"].values:
                st.error("Ya registraste tu aporte. Si necesitas cambiarlo, avisa a la organización.")
                st.stop()

            # Resolver textos finales para cada categoría
            # Piqueo
            if piqueo_sel == "Otro (indicar)":
                if not piqueo_otro.strip():
                    st.error("Especifica qué piqueo llevarás en 'Otro (indicar)'.")
                    st.stop()
                piqueo_final = piqueo_otro.strip()
            else:
                piqueo_final = piqueo_sel

            # Bebida alcohólica
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

            # Bebida no alcohólica
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

            # Validar cantidades:
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

            msg = f"¡Listo, {nombre}! Llevarás **{cant_piqueo}** de **{piqueo_final}**"
            if beb_alc_final:
                msg += f", **{cant_beb_alc_final}** de **{beb_alc_final}**"
            if beb_noalc_final:
                msg += f", y **{cant_beb_noalc_final}** de **{beb_noalc_final}**"
            st.success(msg + " 🎉")

            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ---- Aportes registrados ----
    if not df_aportes.empty:
        st.subheader("📋 Aportes registrados hasta ahora")

        df_mostrar = df_aportes.copy()
        df_mostrar.rename(
            columns={
                "nombre": "Nombre",
                "piqueo": "Piqueo",
                "cant_piqueo": "Cantidad piqueo",
                "bebida_alcoholica": "Bebida alcohólica",
                "cant_bebida_alcoholica": "Cantidad beb. alcohólica",
                "bebida_no_alcoholica": "Bebida no alcohólica",
                "cant_bebida_no_alcoholica": "Cantidad beb. no alcohólica",
            },
            inplace=True,
        )

        df_mostrar = df_mostrar.sort_values("Nombre").reset_index(drop=True)
        st.dataframe(df_mostrar, use_container_width=True)

        # Quiénes faltan
        nombres_ya = set(df_aportes["nombre"].tolist())
        faltan = [n for n in PARTICIPANTES if n not in nombres_ya]
        if faltan:
            st.markdown("### 🙋‍♀️ Personas que aún no registran su aporte")
            st.write(", ".join(faltan))
        else:
            st.success("🎉 ¡Todos los participantes ya registraron su aporte!")


if __name__ == "__main__":
    main()