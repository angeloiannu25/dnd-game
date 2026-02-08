import streamlit as st
from google import genai
import random
import json
import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="D&D Party", page_icon="🎲", layout="wide")

# ============ CONFIGURAZIONE ============
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

PARTITA_ID = "partita_principale"

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
                "classe": "Maga",
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

def calcola_modificatore(stat):
    return (stat - 10) // 2

# ============ SIDEBAR ============
with st.sidebar:
    st.header("🎮 Personaggio")
    giocatore_attivo = st.radio("Chi sei?", list(dati["giocatori"].keys()), label_visibility="collapsed")
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

# System prompt
SYSTEM_PROMPT = f"""Sei un Dungeon Master di D&D 5e.

PARTY: {p1['nome']} (Guerriero, HP {p1['hp']}/{p1['hp_max']}) e {p2['nome']} (Maga, HP {p2['hp']}/{p2['hp_max']})

Sii descrittivo, coinvolgente. Chiedi tiri quando serve. Crea una bella avventura!"""

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

# Backup
with st.expander("💾 Backup"):
    st.download_button(
        "Scarica",
        json.dumps(dati, indent=2),
        "partita.json",
        "application/json"
    )