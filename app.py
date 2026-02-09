import streamlit as st
from google import genai
import random
import json
import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
from character_creator import crea_personaggio

load_dotenv()

st.set_page_config(page_title="D&D Party", page_icon="🎲", layout="wide")

# ============ CSS TAVERNA INLINE ============
def load_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap');
    
    /* Sfondo taverna */
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
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a0f08 0%, #2d1b12 50%, #1a0f08 100%);
        border-right: 4px solid #5c4033;
    }
    
    /* Font titoli medievale */
    h1, h2, h3 {
        font-family: 'MedievalSharp', cursive !important;
        color: #f4e4c1 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }
    
    /* Testo normale */
    p, div, span, label {
        color: #e8d4b0 !important;
        font-family: 'Georgia', serif !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #f4e4c1 !important;
    }
    
    /* Pulsanti legno */
    button {
        background: linear-gradient(145deg, #5c4033 0%, #6d4c3d 50%, #5c4033 100%) !important;
        color: #f4e4c1 !important;
        border: 3px solid #3d2817 !important;
        border-radius: 8px !important;
        font-family: 'MedievalSharp', cursive !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8) !important;
    }
    
    button:hover {
        background: linear-gradient(145deg, #6d4c3d 0%, #7d5c4d 50%, #6d4c3d 100%) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Input */
    input, textarea, select {
        background: rgba(30,20,15,0.8) !important;
        color: #f4e4c1 !important;
        border: 2px solid #5c4033 !important;
        font-family: 'Georgia', serif !important;
    }
    
    /* Chat messaggi */
    [data-testid="stChatMessageContent"] {
        background: rgba(45,30,20,0.9) !important;
        border: 2px solid #5c4033 !important;
        border-radius: 10px !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #ffd700 !important;
        font-weight: bold !important;
    }
    
    /* Progress bar HP */
    [data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, #8b0000 0%, #ff4444 50%, #8b0000 100%) !important;
        border-radius: 10px !important;
    }
    
  /* ============ NASCONDI ELEMENTI TECNICI ============ */
    
    /* Nascondi SVG e icone */
    [data-testid="stExpander"] svg,
    button[title*="sidebar"] svg,
    svg[data-testid="stIconChevronDown"],
    svg[data-testid="stIconChevronUp"],
    svg[data-testid="stIconMaterial"] {
        display: none !important;
    }
    
    /* Nascondi testo "keyboard_double_arrow" */
    button span[data-baseweb] {
        font-size: 0 !important;
    }
    
    /* Nascondi testo tecnico negli expander */
    [data-testid="stExpander"] details summary span {
        font-size: inherit !important;
    }
    
    [data-testid="stExpander"] details summary::marker {
        content: "🗡️ " !important;
    }
    
    /* Nascondi "double_arrow_right" e simili */
    button[kind="header"]::after {
        content: "" !important;
    }
    
    button[kind="header"] span {
        visibility: hidden !important;
    }
    
    /* Nascondi label del radio button */
    [data-testid="stRadio"] > label {
        display: none !important;
    }
    
    /* Nascondi testo "smart_" nelle chat */
    [data-testid="stChatMessage"] span[data-testid*="smart"] {
        display: none !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        background: #2c1810;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #5c4033 0%, #3d2817 100%);
        border-radius: 6px;
    }
    /* ============ FIX TESTI TECNICI SPECIFICI ============ */
    
    /* Nascondi "keyboard_double_arrow" nel pulsante sidebar */
    button[kind="header"] {
        font-size: 0 !important;
        width: 40px !important;
    }
    
    button[kind="header"] svg {
        font-size: 24px !important;
    }
    
    /* Nascondi "double_arrow_right" sopra la chat */
    [data-testid="stHeader"] button span {
        display: none !important;
    }
    
    /* Nascondi "smart_toy" nelle icone chat */
    [data-testid="stChatMessage"] svg + span {
        display: none !important;
    }
    
    /* Nascondi TUTTI i testi Material Icons */
    span[class*="material"] {
        font-size: 0 !important;
    }
    
    span[class*="material"]::before,
    span[class*="material"]::after {
        font-size: 0 !important;
    }
    
    /* Forza nascondere testo nei bottoni header */
    [data-testid="collapsedControl"] span {
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
    }
    
    /* Mantieni solo l'icona SVG visibile */
    [data-testid="collapsedControl"] svg {
        visibility: visible !important;
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
                "livello": 3,
                "forza": 16,
                "destrezza": 12,
                "costituzione": 14,
                "intelligenza": 10,
                "saggezza": 11,
                "carisma": 9,
                "hp_max": 30,
                "hp": 30,
                "inventario": ["Spada lunga", "Scudo", "Pozione cura"]
            },
            "Giocatore 2": {
                "nome": "Elara",
                "classe": "Mago",
                "livello": 3,
                "forza": 8,
                "destrezza": 14,
                "costituzione": 10,
                "intelligenza": 16,
                "saggezza": 12,
                "carisma": 13,
                "hp_max": 20,
                "hp": 20,
                "inventario": ["Bacchetta", "Libro", "Pozione mana"]
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

# ============ FUNZIONE CALCOLA MODIFICATORE ============
def calcola_modificatore(stat):
    """Calcola il modificatore di una statistica D&D"""
    return (stat - 10) // 2

# ============ SYSTEM PROMPT (deve essere PRIMA della creazione PG) ============
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
- Quando infligi danno dì ESATTAMENTE quanti PF perdono (es: "Subisci 8 danni!")
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
# Usa session_state per tracciare se la creazione è completa
if "personaggi_creati" not in st.session_state:
    st.session_state.personaggi_creati = False

# Controlla se i personaggi sono stati effettivamente creati
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

# Se entrambi sono creati, segna come completo
if pg1_creato and pg2_creato:
    st.session_state.personaggi_creati = True

# Mostra creazione SOLO se non è stata completata
if not st.session_state.personaggi_creati:
    # CASO 1: Nessun personaggio creato → Crea il primo
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

    # CASO 2: Solo il primo creato → Crea il secondo
    if pg1_creato and not pg2_creato:
        st.title("🎭 Aggiungi un compagno d'avventura!")
        st.markdown(f"### {p1['nome']} cerca un alleato fidato...")
        
        nuovo_pg = crea_personaggio()
        
        if nuovo_pg:
            dati["giocatori"]["Giocatore 2"] = nuovo_pg
            salva_partita(dati)
            st.success(f"✅ {nuovo_pg['nome']} si unisce alla party!")
            st.balloons()
            
            # Messaggio iniziale del DM dopo creazione party completa
            if not dati["chat"]:
                messaggio_iniziale = f"""La sera cala sulla città portuale di Saltmist. L'aria sa di salmastro e pesce, mentre le lanterne cominciano ad accendersi una ad una lungo le strade acciottolate.

{p1['nome']}, {p1['razza']} {p1['classe']}, e {nuovo_pg['nome']}, {nuovo_pg['razza']} {nuovo_pg['classe']}, si incontrano per la prima volta nell'affollata sala de "L'Ancora Spezzata", una taverna nota tanto per la sua birra scura quanto per i loschi figuri che la frequentano.

Entrambi siete qui per lo stesso motivo: una misteriosa lettera ricevuta tre giorni fa, firmata solo con un simbolo - un'ancora spezzata circondata da rune. La lettera prometteva oro e gloria a chi avesse il coraggio di presentarsi qui, questa sera, al tramonto.

Mentre vi sedete allo stesso tavolo d'angolo, notate che sulla superficie di legno usurato è inciso proprio quel simbolo. Un vecchio marinaio con una benda sull'occhio vi osserva dalla barra, poi si avvicina lentamente...

**Cosa fate?**"""
                
                dati["chat"].append(messaggio_iniziale)
                salva_partita(dati)
            
            # Segna come completato
            st.session_state.personaggi_creati = True
            st.rerun()
        
        st.stop()

# CASO 3: Entrambi creati → Continua con il gioco normale
# ============ SIDEBAR ============
with st.sidebar:
    st.header("🎮 Personaggio")
    giocatore_attivo = st.radio("Chi sei?", list(dati["giocatori"].keys()), label_visibility="collapsed", key="selettore_giocatore")
    pg = dati["giocatori"][giocatore_attivo]
    
    st.divider()
    st.subheader(f"📜 {pg['nome']}")
    st.caption(f"{pg['classe']} - Lv.{pg['livello']}")
    
    hp_pct = (pg['hp'] / pg['hp_max']) * 100
    colore = "🟢" if hp_pct > 50 else "🟡" if hp_pct > 25 else "🔴"
    st.metric(f"{colore} HP", f"{pg['hp']}/{pg['hp_max']}")
    st.progress(pg['hp'] / pg['hp_max'])
    
    st.divider()
    
    st.write("**📊 Stats**")
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
    
    col_hp1, col_hp2 = st.columns(2)
    with col_hp1:
        danno = st.number_input("Danno", 0, 100, 5)
        if st.button("💔 Subisci", use_container_width=True):
            pg['hp'] = max(0, pg['hp'] - danno)
            salva_partita(dati)
            st.rerun()
    with col_hp2:
        cura = st.number_input("Cura", 0, 100, 5)
        if st.button("💚 Cura", use_container_width=True):
            pg['hp'] = min(pg['hp_max'], pg['hp'] + cura)
            salva_partita(dati)
            st.rerun()
    
    st.divider()
    
    with st.expander("🎒 Inventario"):
        for i, item in enumerate(pg['inventario']):
            col_i, col_d = st.columns([4, 1])
            with col_i:
                st.write(f"• {item}")
            with col_d:
                if st.button("🗑️", key=f"del_{i}"):
                    pg['inventario'].pop(i)
                    salva_partita(dati)
                    st.rerun()
        
        nuovo = st.text_input("Aggiungi")
        if st.button("➕", use_container_width=True) and nuovo:
            pg['inventario'].append(nuovo)
            salva_partita(dati)
            st.rerun()
    
    st.divider()
    
    st.write("**🎲 Dadi**")
    tipo_dado = st.selectbox("Tipo", ["d20", "d12", "d10", "d8", "d6", "d4"])
    
    if st.button("🎲 TIRA!", use_container_width=True, type="primary"):
        risultato = random.randint(1, int(tipo_dado[1:]))
        mod = calcola_modificatore(pg['forza'])
        msg = f"🎲 **{pg['nome']}** tira {tipo_dado}: **{risultato}** (FOR: {risultato + mod})"
        dati["chat"].append(msg)
        salva_partita(dati)
        st.rerun()
    
    st.divider()
    
    if st.button("🔄 Ricarica", use_container_width=True):
        st.session_state.dati = carica_partita()
        st.rerun()

# ============ CHAT ============
st.title("⚔️ D&D Campaign")

col1, col2 = st.columns(2)
p1 = dati["giocatori"]["Giocatore 1"]
p2 = dati["giocatori"]["Giocatore 2"]

with col1:
    st.info(f"**{p1['nome']}** - HP: {p1['hp']}/{p1['hp_max']}")
with col2:
    st.info(f"**{p2['nome']}** - HP: {p2['hp']}/{p2['hp_max']}")

st.divider()

# System prompt migliorato
p1 = dati["giocatori"]["Giocatore 1"]
p2 = dati["giocatori"]["Giocatore 2"]

# Mostra chat
for msg in dati["chat"]:
    # Converte tutto in stringa per sicurezza
    msg_str = str(msg) if not isinstance(msg, str) else msg
    
    if "🎲" in msg_str or msg_str.startswith("**"):
        st.chat_message("user").write(msg_str)
    else:
        st.chat_message("assistant").write(msg_str)

# Input
if prompt := st.chat_input(f"Cosa fa {pg['nome']}?"):
    msg_user = f"**{pg['nome']}**: {prompt}"
    
    st.chat_message("user").write(msg_user)
    
    # Prepara conversazione
    conversazione = SYSTEM_PROMPT + "\n\n"
    for msg in dati["chat"]:
        conversazione += str(msg) + "\n\n"
    conversazione += msg_user
    
    with st.chat_message("assistant"):
        with st.spinner("Il DM pensa..."):
            try:
                response = client.models.generate_content(
                    model='gemini-flash-latest',  # Modello con quota diversa
                    contents=conversazione
                )
                
                risposta = response.text
                st.write(risposta)
                
                dati["chat"].append(msg_user)
                dati["chat"].append(risposta)
                
                salva_partita(dati)
                st.rerun()
                
            except Exception as e:
                st.error(f"Errore: {e}")
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    st.warning("⏰ Quota API esaurita. Riprova tra qualche minuto o domani!")

# Backup e Reset
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
            use_container_width=True
        )
    
    # Reset
with col_opt2:
    st.write("**🔄 Reset Partita**")
    st.warning("⚠️ Cancella tutto!")
    
    if st.button("🗑️ RESET COMPLETO", use_container_width=True, type="secondary"):
        # Cancella dal database
        try:
            supabase.table("partite").delete().eq("partita_id", PARTITA_ID).execute()
        except:
            pass
        
        # Reset locale - torna ai placeholder
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
        
        # Resetta anche il flag di creazione personaggi
        st.session_state.personaggi_creati = False
        
        st.success("✅ Partita resettata!")
        st.rerun()