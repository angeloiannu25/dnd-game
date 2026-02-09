import streamlit as st
from google import genai
import random
import json
import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
from character_creator import crea_personaggio
import re

load_dotenv()

st.set_page_config(page_title="D&D Party", page_icon="🎲", layout="wide")

# ============ CSS TAVERNA INLINE ============
def load_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap');
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #2c1810 0%, #3d2817 25%, #4a3520 50%, #3d2817 75%, #2c1810 100%);
        background-size: 400% 400%;
        animation: gradient-shift 20s ease infinite;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a0f08 0%, #2d1b12 50%, #1a0f08 100%);
        border-right: 4px solid #5c4033;
        box-shadow: inset -10px 0 30px rgba(0,0,0,0.5);
    }
    
    h1, h2, h3 {
        font-family: 'MedievalSharp', cursive !important;
        color: #f4e4c1 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }
    
    p, div, span, label {
        color: #e8d4b0 !important;
        font-family: 'Georgia', serif !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #f4e4c1 !important;
    }
    
    button {
        background: linear-gradient(145deg, #5c4033 0%, #6d4c3d 50%, #5c4033 100%) !important;
        color: #f4e4c1 !important;
        border: 3px solid #3d2817 !important;
        border-radius: 8px !important;
        font-family: 'MedievalSharp', cursive !important;
        font-size: 14px !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8) !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5) !important;
    }
    
    button:hover {
        background: linear-gradient(145deg, #6d4c3d 0%, #7d5c4d 50%, #6d4c3d 100%) !important;
        transform: translateY(-2px) !important;
    }
    
    input, textarea, select {
        background: rgba(30,20,15,0.8) !important;
        color: #f4e4c1 !important;
        border: 2px solid #5c4033 !important;
        border-radius: 6px !important;
        font-family: 'Georgia', serif !important;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.5) !important;
    }
    
    [data-testid="stChatMessageContent"] {
        background: rgba(45,30,20,0.9) !important;
        border: 2px solid #5c4033 !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }
    
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        border-left: 4px solid #d4a574 !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #ffd700 !important;
        font-weight: bold !important;
        text-shadow: 0 0 10px rgba(255,215,0,0.5) !important;
    }
    
    [data-testid="metric-container"] {
        background: rgba(30,20,15,0.6) !important;
        border: 2px solid #5c4033 !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, #8b0000 0%, #ff4444 50%, #8b0000 100%) !important;
        border-radius: 10px !important;
        box-shadow: 0 0 15px rgba(255,0,0,0.5) !important;
    }
    
    [data-testid="stExpander"] {
        background: rgba(45,30,20,0.6) !important;
        border: 2px solid #5c4033 !important;
        border-radius: 8px !important;
    }
    
    ::-webkit-scrollbar {
        width: 12px;
        background: #2c1810;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #5c4033 0%, #3d2817 100%);
        border-radius: 6px;
        border: 2px solid #2c1810;
    }
    
    button[kind="header"],
    button[kind="headerNoPadding"],
    [data-testid="collapsedControl"] button {
        font-size: 0 !important;
        line-height: 0 !important;
        overflow: hidden !important;
    }
    
    button[kind="header"] *:not(svg),
    button[kind="headerNoPadding"] *:not(svg),
    [data-testid="collapsedControl"] button *:not(svg) {
        font-size: 0 !important;
        display: inline !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    
    button[kind="header"] svg,
    button[kind="headerNoPadding"] svg,
    [data-testid="collapsedControl"] svg {
        font-size: 24px !important;
        width: 24px !important;
        height: 24px !important;
    }
    
    span[class*="material"],
    span[data-testid*="stIcon"],
    .material-icons,
    .material-symbols-outlined {
        font-size: 0 !important;
        width: 0 !important;
        height: 0 !important;
        display: none !important;
    }
    
    [data-testid="stExpander"] summary {
        font-size: 16px !important;
    }
    
    [data-testid="stExpander"] summary svg {
        display: none !important;
    }
    
    [data-testid="stExpander"] summary::before {
        content: "📜 ";
    }
    
    [data-testid="stRadio"] > label {
        display: none !important;
    }
    
    [data-testid="stChatMessage"] svg {
        display: none !important;
    }
    
    [data-testid="stHeader"] button span {
        font-size: 0 !important;
    }
    
    [data-testid="stHeader"] svg {
        font-size: 24px !important;
    }
    
    .stAlert {
        background: rgba(60,40,25,0.95) !important;
        border-left: 4px solid #d4a574 !important;
        border-radius: 8px !important;
        color: #f4e4c1 !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# ============ CONFIGURAZIONE ============
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

PARTITA_ID = "partita_principale"

# ============ FUNZIONI UTILITÀ ============
def calcola_modificatore(stat):
    """Calcola il modificatore di una statistica D&D"""
    return (stat - 10) // 2

def estrai_danni_da_messaggio(messaggio, nomi_personaggi):
    """
    Estrae automaticamente i danni dal messaggio del DM.
    Cerca pattern come: "8 danni", "subisci 10", "perde 5 HP", ecc.
    Restituisce: [(nome_personaggio, danni), ...]
    """
    risultati = []
    messaggio_lower = messaggio.lower()
    
    # Pattern per trovare danni
    # Esempi: "subisci 8 danni", "Thorin perde 10 HP", "5 danni", "colpisce per 12"
    patterns = [
        r'(?:subisci|prendi|perde|perdi|ricevi|ti colpisce per)\s+(\d+)\s*(?:danni|danno|hp|pf|punti ferita)',
        r'(\d+)\s+(?:danni|danno|hp|pf|punti ferita)',
        r'(?:per|di)\s+(\d+)\s+(?:danni|danno)',
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, messaggio_lower)
        for match in matches:
            danno = int(match.group(1))
            
            # Cerca quale personaggio è menzionato prima del danno
            pos_danno = match.start()
            testo_prima = messaggio[:pos_danno].lower()
            
            personaggio_colpito = None
            for nome in nomi_personaggi:
                if nome.lower() in testo_prima:
                    # Trova l'ultima occorrenza del nome prima del danno
                    personaggio_colpito = nome
            
            # Se non trova il nome, prende l'ultimo personaggio menzionato nell'intero messaggio
            if not personaggio_colpito:
                for nome in nomi_personaggi:
                    if nome.lower() in messaggio_lower:
                        personaggio_colpito = nome
                        break
            
            if personaggio_colpito and danno > 0:
                risultati.append((personaggio_colpito, danno))
                break  # Prendi solo il primo match per evitare duplicati
    
    return risultati

def applica_danni_automatici(messaggio_dm, dati):
    """
    Applica automaticamente i danni ai personaggi menzionati nel messaggio del DM.
    """
    nomi = [pg['nome'] for pg in dati['giocatori'].values() if pg.get('nome')]
    danni_trovati = estrai_danni_da_messaggio(messaggio_dm, nomi)
    
    if danni_trovati:
        for nome_pg, danno in danni_trovati:
            # Trova il giocatore corretto
            for key, pg in dati['giocatori'].items():
                if pg.get('nome') == nome_pg:
                    hp_prima = pg['hp']
                    pg['hp'] = max(0, pg['hp'] - danno)
                    hp_dopo = pg['hp']
                    
                    # Crea notifica
                    if 'notifiche' not in st.session_state:
                        st.session_state.notifiche = []
                    
                    st.session_state.notifiche.append({
                        'tipo': 'danno',
                        'personaggio': nome_pg,
                        'valore': danno,
                        'hp_prima': hp_prima,
                        'hp_dopo': hp_dopo
                    })
                    break

# ============ FUNZIONI DATABASE ============
def carica_partita():
    try:
        response = supabase.table("partite").select("*").eq("partita_id", PARTITA_ID).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]["dati"]
    except:
        pass
    
    return {
        "chat": [],
        "giocatori": {
            "Giocatore 1": {
                "nome": "Thorin",
                "classe": "Guerriero",
                "livello": 1,
                "forza": 10,
                "destrezza": 10,
                "costituzione": 10,
                "intelligenza": 10,
                "saggezza": 10,
                "carisma": 10,
                "hp_max": 10,
                "hp": 10,
                "inventario": []
            },
            "Giocatore 2": {
                "nome": "Elara",
                "classe": "Maga",
                "livello": 1,
                "forza": 10,
                "destrezza": 10,
                "costituzione": 10,
                "intelligenza": 10,
                "saggezza": 10,
                "carisma": 10,
                "hp_max": 10,
                "hp": 10,
                "inventario": []
            }
        }
    }

def salva_partita(dati):
    try:
        existing = supabase.table("partite").select("*").eq("partita_id", PARTITA_ID).execute()
        
        if existing.data and len(existing.data) > 0:
            supabase.table("partite").update({
                "dati": dati,
                "ultimo_aggiornamento": datetime.now().isoformat()
            }).eq("partita_id", PARTITA_ID).execute()
        else:
            supabase.table("partite").insert({
                "partita_id": PARTITA_ID,
                "dati": dati,
                "ultimo_aggiornamento": datetime.now().isoformat()
            }).execute()
        return True
    except:
        return False

# ============ INIZIALIZZA ============
if "dati" not in st.session_state:
    st.session_state.dati = carica_partita()

dati = st.session_state.dati

# ============ SYSTEM PROMPT ============
p1 = dati["giocatori"]["Giocatore 1"]
p2 = dati["giocatori"]["Giocatore 2"]

SYSTEM_PROMPT = f"""Sei un Dungeon Master esperto di D&D 5a Edizione.

🎭 PARTY ATTUALE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 {p1.get('nome', 'Giocatore 1')} - {p1.get('razza', 'Umano')} {p1.get('classe', 'Guerriero')} (Livello {p1.get('livello', 1)})
   Background: {p1.get('background', 'Avventuriero')}
   HP: {p1.get('hp', 10)}/{p1.get('hp_max', 10)}
   FOR {p1.get('forza', 10)} | DES {p1.get('destrezza', 10)} | COS {p1.get('costituzione', 10)}
   INT {p1.get('intelligenza', 10)} | SAG {p1.get('saggezza', 10)} | CAR {p1.get('carisma', 10)}

👤 {p2.get('nome', 'Giocatore 2')} - {p2.get('razza', 'Elfo')} {p2.get('classe', 'Mago')} (Livello {p2.get('livello', 1)})
   Background: {p2.get('background', 'Avventuriero')}
   HP: {p2.get('hp', 10)}/{p2.get('hp_max', 10)}
   FOR {p2.get('forza', 10)} | DES {p2.get('destrezza', 10)} | COS {p2.get('costituzione', 10)}
   INT {p2.get('intelligenza', 10)} | SAG {p2.get('saggezza', 10)} | CAR {p2.get('carisma', 10)}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📜 TUO RUOLO:
Sei un Dungeon Master cinematografico che crea avventure epiche e memorabili.

🎯 STILE NARRATIVO:
- Descrizioni vivide usando tutti e 5 i sensi
- Crea atmosfera immersiva con tensione e suspense
- NPCs realistici con personalità uniche
- Conseguenze reali delle azioni

⚔️ GESTIONE COMBATTIMENTO:
- All'inizio del combattimento chiedi iniziativa (d20 + DES)
- Descrivi ogni attacco in modo cinematografico
- Quando un PG attacca chiedi il tiro appropriato
- **IMPORTANTE**: Quando infligi danno, scrivi ESATTAMENTE: "[Nome] subisce [numero] danni" (esempio: "Thorin subisce 8 danni")
- Questo permette al sistema di togliere automaticamente gli HP
- Descrivi ferite e sforzo fisico

🎲 REGOLE D&D 5E:
- Usa le regole ufficiali correttamente
- CD appropriate: Facile 10, Medio 15, Difficile 20
- 1 sul d20 = fallimento critico, 20 = successo critico
- Considera vantaggi/svantaggi tattici

🎭 INTERAZIONE:
- Fai domande quando le azioni sono ambigue
- Offri scelte significative
- Premia creatività e gioco di ruolo
- Usa i background dei PG nella storia

🎬 RITMO:
- Alterna combattimento, esplorazione, enigmi, social
- Crea cliffhanger
- Bilancia momenti epici con pause

INIZIA SEMPRE TU quando la chat è vuota con una scena d'apertura atmosferica che introduce il setting!
"""

# ============ CREAZIONE PERSONAGGI ============
pg1_creato = (
    p1.get("nome") and 
    p1.get("nome") not in ["Thorin", ""] and
    p1.get("razza") is not None
)

pg2_creato = (
    p2.get("nome") and 
    p2.get("nome") not in ["Elara", ""] and
    p2.get("razza") is not None
)

if "personaggi_creati" not in st.session_state:
    st.session_state.personaggi_creati = (pg1_creato and pg2_creato)

if pg1_creato and pg2_creato:
    st.session_state.personaggi_creati = True

if not st.session_state.personaggi_creati:
    if not pg1_creato and not pg2_creato:
        st.title("🎭 Benvenuto nel mondo di D&D!")
        st.markdown("### Prima di iniziare, crea il tuo personaggio")
        st.info("💡 **Consiglio**: Prenditi il tempo per leggere le descrizioni e scegliere con cura!")
        
        nuovo_pg = crea_personaggio()
        
        if nuovo_pg:
            dati["giocatori"]["Giocatore 1"] = nuovo_pg
            salva_partita(dati)
            st.success(f"✅ {nuovo_pg['nome']} è pronto per l'avventura!")
            st.balloons()
            st.rerun()
        
        st.stop()

    if pg1_creato and not pg2_creato:
        st.title("🎭 Aggiungi un compagno d'avventura!")
        st.markdown(f"### {p1['nome']} cerca un alleato fidato...")
        
        nuovo_pg = crea_personaggio()
        
        if nuovo_pg:
            dati["giocatori"]["Giocatore 2"] = nuovo_pg
            salva_partita(dati)
            st.success(f"✅ {nuovo_pg['nome']} si unisce alla party!")
            st.balloons()
            
            if not dati["chat"]:
                messaggio_iniziale = f"""La sera cala sulla città portuale di Saltmist. L'aria sa di salmastro e pesce, mentre le lanterne cominciano ad accendersi una ad una lungo le strade acciottolate.

{p1['nome']}, {p1['razza']} {p1['classe']}, e {nuovo_pg['nome']}, {nuovo_pg['razza']} {nuovo_pg['classe']}, si incontrano per la prima volta nell'affollata sala de "L'Ancora Spezzata", una taverna nota tanto per la sua birra scura quanto per i loschi figuri che la frequentano.

Entrambi siete qui per lo stesso motivo: una misteriosa lettera ricevuta tre giorni fa, firmata solo con un simbolo - un'ancora spezzata circondata da rune. La lettera prometteva oro e gloria a chi avesse il coraggio di presentarsi qui, questa sera, al tramonto.

Mentre vi sedete allo stesso tavolo d'angolo, notate che sulla superficie di legno usurato è inciso proprio quel simbolo. Un vecchio marinaio con una benda sull'occhio vi osserva dalla barra, poi si avvicina lentamente...

**Cosa fate?**"""
                
                dati["chat"].append(messaggio_iniziale)
                salva_partita(dati)
            
            st.session_state.personaggi_creati = True
            st.rerun()
        
        st.stop()

# ============ SIDEBAR ============
with st.sidebar:
    st.header("🎮 Personaggio")
    giocatore_attivo = st.radio("Chi sei?", list(dati["giocatori"].keys()), label_visibility="collapsed", key="selettore_giocatore")
    pg = dati["giocatori"][giocatore_attivo]
    
    st.divider()
    
    # SCHEDA PERSONAGGIO COMPLETA
    st.subheader(f"📜 {pg['nome']}")
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.caption(f"**{pg.get('razza', 'Umano')}** {pg['classe']}")
    with col_info2:
        st.caption(f"Livello {pg['livello']}")
    
    if pg.get('background'):
        st.caption(f"🎭 {pg['background']}")
    
    st.divider()
    
    # HP
    hp_pct = (pg['hp'] / pg['hp_max']) * 100
    colore = "🟢" if hp_pct > 50 else "🟡" if hp_pct > 25 else "🔴"
    st.metric(f"{colore} Punti Ferita", f"{pg['hp']}/{pg['hp_max']}")
    st.progress(pg['hp'] / pg['hp_max'])
    
    # Gestione HP
    col_hp1, col_hp2 = st.columns(2)
    with col_hp1:
        danno = st.number_input("Danno", 0, 100, 5, key="danno_input")
        if st.button("💔 Subisci", use_container_width=True, key="btn_danno"):
            pg['hp'] = max(0, pg['hp'] - danno)
            salva_partita(dati)
            st.rerun()
    with col_hp2:
        cura = st.number_input("Cura", 0, 100, 5, key="cura_input")
        if st.button("💚 Cura", use_container_width=True, key="btn_cura"):
            pg['hp'] = min(pg['hp_max'], pg['hp'] + cura)
            salva_partita(dati)
            st.rerun()
    
    st.divider()
    
    # STATISTICHE
    st.write("**📊 Caratteristiche**")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💪 FOR", pg['forza'], f"{calcola_modificatore(pg['forza']):+d}")
        st.metric("🏃 DES", pg['destrezza'], f"{calcola_modificatore(pg['destrezza']):+d}")
        st.metric("🛡️ COS", pg['costituzione'], f"{calcola_modificatore(pg['costituzione']):+d}")
    with col2:
        st.metric("🧠 INT", pg['intelligenza'], f"{calcola_modificatore(pg['intelligenza']):+d}")
        st.metric("🦉 SAG", pg['saggezza'], f"{calcola_modificatore(pg['saggezza']):+d}")
        st.metric("💬 CAR", pg['carisma'], f"{calcola_modificatore(pg['carisma']):+d}")
    
    st.divider()
    
    # ABILITÀ DI CLASSE
    if pg.get('abilita'):
        with st.expander("⚔️ Abilità"):
            for abilita in pg['abilita']:
                st.write(f"• {abilita}")
    
    # INCANTESIMI
    if pg.get('incantesimi') and len(pg['incantesimi']) > 0:
        with st.expander("✨ Incantesimi"):
            for incantesimo in pg['incantesimi']:
                st.write(f"• {incantesimo}")
    
    # INVENTARIO
    with st.expander("🎒 Inventario"):
        if pg.get('monete_oro'):
            st.write(f"**💰 {pg['monete_oro']} monete d'oro**")
            st.divider()
        
        for i, item in enumerate(pg['inventario']):
            col_i, col_d = st.columns([4, 1])
            with col_i:
                st.write(f"• {item}")
            with col_d:
                if st.button("🗑️", key=f"del_{i}"):
                    pg['inventario'].pop(i)
                    salva_partita(dati)
                    st.rerun()
        
        nuovo = st.text_input("Aggiungi oggetto", key="nuovo_oggetto")
        if st.button("➕ Aggiungi", use_container_width=True, key="btn_add_item") and nuovo:
            pg['inventario'].append(nuovo)
            salva_partita(dati)
            st.rerun()
    
    st.divider()
    
    # DADI
    with st.expander("🎲 Tira i Dadi"):
        tipo_dado = st.selectbox("Tipo dado", ["d20", "d12", "d10", "d8", "d6", "d4"], key="tipo_dado")
        modificatore_stat = st.selectbox("Aggiungi modificatore", 
            ["Nessuno", "Forza", "Destrezza", "Costituzione", "Intelligenza", "Saggezza", "Carisma"],
            key="mod_stat"
        )
        
        if st.button("🎲 TIRA!", use_container_width=True, type="primary", key="btn_tira_dado"):
            risultato = random.randint(1, int(tipo_dado[1:]))
            
            if modificatore_stat != "Nessuno":
                stat_map = {
                    "Forza": pg['forza'],
                    "Destrezza": pg['destrezza'],
                    "Costituzione": pg['costituzione'],
                    "Intelligenza": pg['intelligenza'],
                    "Saggezza": pg['saggezza'],
                    "Carisma": pg['carisma']
                }
                mod = calcola_modificatore(stat_map[modificatore_stat])
                totale = risultato + mod
                msg = f"🎲 **{pg['nome']}** tira {tipo_dado} ({modificatore_stat[:3].upper()}): **{risultato}** + {mod} = **{totale}**"
            else:
                msg = f"🎲 **{pg['nome']}** tira {tipo_dado}: **{risultato}**"
            
            dati["chat"].append(msg)
            salva_partita(dati)
            st.rerun()
    
    st.divider()
    
    # MANUALE REGOLE
    with st.expander("📖 Manuale & Regole"):
        st.markdown("""
### 🎲 I Dadi

**d20** - Dado principale per:
- Prove di abilità (Atletica, Furtività, ecc.)
- Tiri per colpire in combattimento
- Tiri salvezza

**Altri dadi** - Per danni e cure:
- **d4**: Pugnale, cure minori
- **d6**: Spada corta, dardo incantato
- **d8**: Spada lunga, arco corto
- **d10**: Spada a due mani
- **d12**: Ascia bipenne, arma grande

---

### 📊 Come funzionano le Prove

**Tiro d20 + Modificatore vs CD**

**Modificatori**:
- **FOR**: Atletica, attacchi in mischia
- **DES**: Acrobazia, Furtività, attacchi a distanza
- **COS**: Resistere veleni, fatica
- **INT**: Conoscenze, Indagare
- **SAG**: Percezione, Intuizione, Sopravvivenza
- **CAR**: Persuasione, Inganno, Intimidire

**Classe Difficoltà (CD)**:
- Facile: CD 10
- Media: CD 15
- Difficile: CD 20
- Molto Difficile: CD 25

---

### ⚔️ Combattimento

**1. INIZIATIVA**
- Tutti tirano d20 + DES
- Ordine dal più alto al più basso

**2. TURNO**
Nel tuo turno puoi fare:
- **1 Azione** (attacco, incantesimo, ecc.)
- **1 Movimento** (fino a 9 metri)
- **1 Azione Bonus** (se hai abilità che la usano)
- **1 Reazione** (es: attacco di opportunità)

**3. ATTACCARE**
- Tira d20 + modificatore appropriato
- Se uguale/superiore alla CA del nemico → colpisci!
- Tira il dado danno dell'arma

**4. MORTE**
- A 0 HP cadi incosciente
- Fai tiri salvezza morte (d20, CD 10)
- 3 successi = stabilizzato
- 3 fallimenti = morto

---

### ✨ Incantesimi Base

**Dardo Incantato** (1° livello)
- 3 dardi, 1d4+1 danni ciascuno
- Colpiscono automaticamente

**Cura Ferite** (1° livello)
- Tocco, cura 1d8 + modificatore SAG

**Scudo** (1° livello)
- Reazione, +5 CA fino al tuo turno

**Mani Brucianti** (1° livello)
- Cono 4,5m, 3d6 danni fuoco
- TS Destrezza dimezza

---

### 🎭 Azioni Comuni

**In Esplorazione**:
- Percepire pericoli: SAG (Percezione)
- Trovare trappole: INT (Indagare)
- Seguire tracce: SAG (Sopravvivenza)
- Scalare: FOR (Atletica)
- Muoversi silenziosamente: DES (Furtività)

**In Sociale**:
- Convincere: CAR (Persuasione)
- Mentire: CAR (Inganno)
- Intimidire: CAR (Intimidazione)
- Capire intenzioni: SAG (Intuizione)

**In Combattimento**:
- Schivare: Azione (vantaggio sui TS DES)
- Aiutare: Azione (alleato ha vantaggio)
- Nascondersi: Azione bonus (DES Furtività)
- Preparare azione: Aspetti un trigger

---

### 🎯 Vantaggio/Svantaggio

**Vantaggio**: Tira 2d20, prendi il più alto
- Quando hai una posizione favorevole
- Se il nemico non ti vede
- Con aiuto di un alleato

**Svantaggio**: Tira 2d20, prendi il più basso
- Quando sei in difficoltà
- Attacchi mentre sei prono
- Condizioni negative

---

### 💡 Consigli Rapidi

- **Descrivi cosa fai**, non solo "attacco"
- **Usa l'ambiente**: rovescia tavoli, spegni torce
- **Lavora in team**: aiutati con gli alleati
- **Sii creativo**: il DM premia l'ingegno
- **Chiedi al DM** se non sei sicuro delle regole
        """)
    
    st.divider()
    
    # RICARICA
    if st.button("🔄 Ricarica Dati", use_container_width=True, key="btn_reload"):
        st.session_state.dati = carica_partita()
        st.rerun()

# ============ CHAT PRINCIPALE ============
st.title("⚔️ D&D Campaign")

# Mostra HP party in alto
col1, col2 = st.columns(2)
with col1:
    hp1_pct = (p1.get('hp', 10) / p1.get('hp_max', 10)) * 100
    col_hp = "🟢" if hp1_pct > 50 else "🟡" if hp1_pct > 25 else "🔴"
    st.info(f"{col_hp} **{p1.get('nome', 'Giocatore 1')}** - HP: {p1.get('hp', 10)}/{p1.get('hp_max', 10)}")
with col2:
    hp2_pct = (p2.get('hp', 10) / p2.get('hp_max', 10)) * 100
    col_hp = "🟢" if hp2_pct > 50 else "🟡" if hp2_pct > 25 else "🔴"
    st.info(f"{col_hp} **{p2.get('nome', 'Giocatore 2')}** - HP: {p2.get('hp', 10)}/{p2.get('hp_max', 10)}")

st.divider()

# Mostra notifiche danni/cure automatici
if 'notifiche' in st.session_state and st.session_state.notifiche:
    for notifica in st.session_state.notifiche:
        if notifica['tipo'] == 'danno':
            st.error(f"💔 **{notifica['personaggio']}** ha subito **{notifica['valore']} danni**! (HP: {notifica['hp_prima']} → {notifica['hp_dopo']})")
    st.session_state.notifiche = []

# Mostra chat
for msg in dati["chat"]:
    if isinstance(msg, str):
        if "🎲" in msg or msg.startswith("**"):
            st.chat_message("user").write(msg)
        else:
            st.chat_message("assistant").write(msg)

# Input chat
if prompt := st.chat_input(f"Cosa fa {pg['nome']}?"):
    msg_user = f"**{pg['nome']}**: {prompt}"
    
    st.chat_message("user").write(msg_user)
    
    conversazione = SYSTEM_PROMPT + "\n\n"
    for msg in dati["chat"]:
        if isinstance(msg, str):
            conversazione += msg + "\n\n"
    conversazione += msg_user
    
    with st.chat_message("assistant"):
        with st.spinner("Il DM pensa..."):
            try:
response = client.models.generate_content(
    model='gemini-flash-latest',
                    contents=conversazione
                )
                
                risposta = response.text
                st.write(risposta)
                
                dati["chat"].append(msg_user)
                dati["chat"].append(risposta)
                
                # APPLICA DANNI AUTOMATICI
                applica_danni_automatici(risposta, dati)
                
                salva_partita(dati)
                st.rerun()
                
            except Exception as e:
                st.error(f"Errore: {e}")
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    st.warning("⏰ Quota API esaurita. Riprova tra qualche minuto!")

# ============ OPZIONI E RESET ============
with st.expander("⚙️ Opzioni"):
    col_opt1, col_opt2 = st.columns(2)
    
    # Backup
    with col_opt1:
        st.write("**💾 Backup Partita**")
        backup_data = json.dumps(dati, indent=2, ensure_ascii=False)
        st.download_button(
            "📥 Scarica Backup",
            data=backup_data,
            file_name=f"dnd_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True,
            key="btn_backup"
        )
    
    # Reset
    with col_opt2:
        st.write("**🔄 Reset Partita**")
        st.warning("⚠️ Cancella tutto!")
        
        if st.button("🗑️ RESET COMPLETO", use_container_width=True, type="secondary", key="btn_reset"):
            try:
                supabase.table("partite").delete().eq("partita_id", PARTITA_ID).execute()
            except:
                pass
            
            st.session_state.dati = {
                "chat": [],
                "giocatori": {
                    "Giocatore 1": {
                        "nome": "Thorin",
                        "classe": "Guerriero",
                        "livello": 1,
                        "forza": 10,
                        "destrezza": 10,
                        "costituzione": 10,
                        "intelligenza": 10,
                        "saggezza": 10,
                        "carisma": 10,
                        "hp_max": 10,
                        "hp": 10,
                        "inventario": []
                    },
                    "Giocatore 2": {
                        "nome": "Elara",
                        "classe": "Maga",
                        "livello": 1,
                        "forza": 10,
                        "destrezza": 10,
                        "costituzione": 10,
                        "intelligenza": 10,
                        "saggezza": 10,
                        "carisma": 10,
                        "hp_max": 10,
                        "hp": 10,
                        "inventario": []
                    }
                }
            }
            
            st.session_state.personaggi_creati = False
            
            st.success("✅ Partita resettata!")
            st.rerun()