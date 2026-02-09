import streamlit as st

# ============ RAZZE CON DESCRIZIONI ============
RAZZE = {
    "Umano": {
        "bonus": {"for": 1, "des": 1, "cos": 1, "int": 1, "sag": 1, "car": 1},
        "desc": "🌍 **Versatili e adattabili**. Gli umani sono la razza più comune e possono eccellere in qualsiasi ruolo.",
        "tratti": ["Bonus +1 a TUTTE le statistiche", "Linguaggio comune + 1 a scelta"]
    },
    "Elfo": {
        "bonus": {"for": 0, "des": 2, "cos": 0, "int": 0, "sag": 0, "car": 0},
        "desc": "🌿 **Agili e mistici**. Creature magiche dalla lunga vita, legati alla natura e all'arcano.",
        "tratti": ["+2 Destrezza", "Visione al buio (18m)", "Vantaggio vs Charme", "Immunità al Sonno magico", "Percezione (competenza)"]
    },
    "Nano": {
        "bonus": {"for": 0, "des": 0, "cos": 2, "int": 0, "sag": 0, "car": 0},
        "desc": "⛏️ **Robusti e tenaci**. Maestri artigiani e guerrieri inarrestabili, vivono nelle montagne.",
        "tratti": ["+2 Costituzione", "Visione al buio (18m)", "Resistenza al veleno", "Competenza con asce e martelli", "Conoscenza della pietra"]
    },
    "Halfling": {
        "bonus": {"for": 0, "des": 2, "cos": 0, "int": 0, "sag": 0, "car": 0},
        "desc": "🍀 **Piccoli ma fortunati**. Creature allegre e coraggiose, alte circa 90cm.",
        "tratti": ["+2 Destrezza", "Fortunato: ritira i dadi quando fai 1", "Coraggioso: vantaggio vs paura", "Agilità halfling: attraversi spazi di creature più grandi"]
    },
    "Mezz'orco": {
        "bonus": {"for": 2, "des": 0, "cos": 1, "int": 0, "sag": 0, "car": 0},
        "desc": "💪 **Potenti e resistenti**. Nati dall'unione di orchi e umani, temuti ma formidabili.",
        "tratti": ["+2 Forza, +1 Costituzione", "Visione al buio (18m)", "Tenacia Implacabile: scendi a 1 PF invece di 0 (1/riposo)", "Intimidazione (competenza)"]
    },
    "Tiefling": {
        "bonus": {"for": 0, "des": 0, "cos": 0, "int": 1, "sag": 0, "car": 2},
        "desc": "🔥 **Toccati dall'inferno**. Discendenti di patti diabolici, con corna e coda.",
        "tratti": ["+2 Carisma, +1 Intelligenza", "Visione al buio (18m)", "Resistenza al fuoco", "Magia innata: Taumaturgia, Rimprovero Infernale (lv3), Oscurità (lv5)"]
    }
}

# ============ CLASSI CON DESCRIZIONI ============
CLASSI = {
    "Guerriero": {
        "hp_base": 10,
        "abilita": [
            "⚔️ **Azione Impetuosa**: Una volta per riposo, puoi fare un'azione aggiuntiva nel tuo turno",
            "💚 **Secondo Vento**: Una volta per riposo, recuperi 1d10 + livello PF come azione bonus"
        ],
        "desc": "⚔️ **Il maestro del combattimento**. Eccelle con ogni arma e armatura, resistente e letale.",
        "armi": "Tutte le armi e armature",
        "ruolo": "Tank/Danno - Prima linea",
        "difficolta": "⭐ Facile (ideale per principianti)"
    },
    "Mago": {
        "hp_base": 6,
        "abilita": [
            "📘 **Recupero Arcano**: Una volta al giorno, recuperi slot incantesimo durante un riposo breve",
            "✨ **Tradizione Arcana**: Scegli una scuola di magia (Evocazione, Illusione, ecc.)"
        ],
        "desc": "📜 **Maestro dell'arcano**. Lancia potenti incantesimi ma è fragile. Richiede strategia.",
        "armi": "Balestre leggere, pugnali, dardi, bastoni, fionde",
        "ruolo": "Danno/Controllo - Retrovie",
        "difficolta": "⭐⭐⭐ Difficile (molti incantesimi da gestire)"
    },
    "Chierico": {
        "hp_base": 8,
        "abilita": [
            "✨ **Incanalare Divinità**: Usi il potere del tuo dio (Scaccia Non-Morti, effetti del Dominio)",
            "⛪ **Dominio Divino**: Scegli l'aspetto del tuo dio (Vita, Guerra, Luce, ecc.)"
        ],
        "desc": "⛪ **Guaritore divino**. Supporta la party con cure e protezioni. Anche combattente decente.",
        "armi": "Armi semplici, armature medie e scudi",
        "ruolo": "Supporto/Guarigione - Versatile",
        "difficolta": "⭐⭐ Medio (equilibrio tra magia e combattimento)"
    },
    "Ladro": {
        "hp_base": 8,
        "abilita": [
            "🗡️ **Attacco Furtivo**: +1d6 danni extra (aumenta con il livello) se colpisci con vantaggio",
            "🏃 **Azione Astuta**: Puoi Nasconderti, Disimpegnarti o Scattare come azione bonus"
        ],
        "desc": "🗡️ **Maestro dell'ombra**. Attacchi furtivi devastanti, esperto di trappole e serrature.",
        "armi": "Armi semplici, balestre a mano, spade corte, spade lunghe, stocchi",
        "ruolo": "Danno/Utilità - Furtivo",
        "difficolta": "⭐⭐ Medio (richiede posizionamento tattico)"
    },
    "Ranger": {
        "hp_base": 10,
        "abilita": [
            "🎯 **Nemico Prescelto**: Scegli un tipo di nemico (draghi, non-morti, ecc.) e ottieni bonus contro di loro",
            "🌲 **Esploratore Nato**: Scegli un terreno (foresta, montagna, ecc.) dove eccelli"
        ],
        "desc": "🏹 **Cacciatore della natura**. Esploratore e combattente a distanza, con magia naturale.",
        "armi": "Armi semplici e marziali, armature leggere e medie",
        "ruolo": "Danno a distanza/Esplorazione",
        "difficolta": "⭐⭐ Medio (mix di combattimento e magia)"
    }
}

# ============ BACKGROUND ============
BACKGROUND = {
    "Accolito": {
        "desc": "⛪ Cresciuto in un tempio, dedicato a una divinità.",
        "competenze": ["Intuizione", "Religione"],
        "tratto": "Rifugio dei Fedeli: trovi ospitalità nei templi della tua fede"
    },
    "Criminale": {
        "desc": "🗡️ Vita nelle strade come ladro, truffatore o contrabbandiere.",
        "competenze": ["Inganno", "Furtività"],
        "tratto": "Contatto Criminale: hai contatti nel sottobosco criminale"
    },
    "Eroe Popolare": {
        "desc": "🌟 Il popolo ti ammira per un'impresa passata.",
        "competenze": ["Addestrare Animali", "Sopravvivenza"],
        "tratto": "Ospitalità Rustica: la gente comune ti aiuta e nasconde"
    },
    "Nobile": {
        "desc": "👑 Nato in una famiglia ricca e influente.",
        "competenze": ["Storia", "Persuasione"],
        "tratto": "Posizione Privilegiata: sei benvenuto nell'alta società"
    },
    "Saggio": {
        "desc": "📚 Studioso di libri antichi e conoscenze arcane.",
        "competenze": ["Arcano", "Storia"],
        "tratto": "Ricercatore: sai dove trovare informazioni rare"
    },
    "Soldato": {
        "desc": "⚔️ Addestrato nell'esercito, disciplinato e combattivo.",
        "competenze": ["Atletica", "Intimidazione"],
        "tratto": "Rango Militare: soldati di rango inferiore ti rispettano"
    },
    "Orfano": {
        "desc": "🏚️ Cresciuto per strada, sopravvissuto grazie all'astuzia.",
        "competenze": ["Rapidità di Mano", "Furtività"],
        "tratto": "Segreti della Città: conosci i percorsi nascosti delle città"
    },
    "Mercante": {
        "desc": "💰 Esperto di commercio e negoziazione.",
        "competenze": ["Intuizione", "Persuasione"],
        "tratto": "Fattore: hai contatti commerciali e conosci rotte mercantili"
    }
}

# ============ INCANTESIMI LIVELLO 1 ============
INCANTESIMI_LV1 = {
    "Dardo Incantato": {
        "desc": "✨ Crei 3 dardi di energia magica che colpiscono automaticamente (non serve tiro per colpire).",
        "effetto": "3 dardi × (1d4+1) danni forza ciascuno",
        "quando": "Danno garantito, ottimo contro nemici con alta CA"
    },
    "Scudo": {
        "desc": "🛡️ Uno scudo invisibile ti protegge quando stai per essere colpito.",
        "effetto": "Reazione. +5 alla CA contro un attacco. Dura fino al tuo prossimo turno",
        "quando": "Quando un nemico sta per colpirti e vuoi evitarlo"
    },
    "Mani Brucianti": {
        "desc": "🔥 Le tue mani eruttano un cono di fuoco che brucia tutto davanti a te.",
        "effetto": "Cono 4,5m. Tutti i nemici: TS Destrezza o 3d6 danni fuoco (metà se superano)",
        "quando": "Contro gruppi di nemici vicini"
    },
    "Sonno": {
        "desc": "💤 Fai addormentare le creature più deboli in un'area.",
        "effetto": "Tira 5d8. Addormenti creature per quel totale di PF (inizia dalle più deboli)",
        "quando": "Contro gruppi di nemici deboli (goblin, cultisti, ecc.)"
    },
    "Armatura Magica": {
        "desc": "✨ Proteggi un alleato con energia magica.",
        "effetto": "Un alleato ottiene CA 13 + mod DES per 8 ore (se non indossa armatura)",
        "quando": "All'inizio della giornata sul mago o alleato senza armatura"
    },
    "Individuazione del Magico": {
        "desc": "👁️ Percepisci l'aura della magia intorno a te.",
        "effetto": "Per 10 minuti, vedi aure magiche entro 9m e ne intuisci la scuola",
        "quando": "Cerchi oggetti magici, trappole magiche, porte sigillate"
    },
    "Charme su Persone": {
        "desc": "💕 Convinci un umanoide che sei suo amico.",
        "effetto": "TS Saggezza o ti considera amico fidato per 1 ora. Sa che era magia dopo",
        "quando": "Convincere guardie, negoziare, evitare combattimenti"
    },
    "Immagine Silenziosa": {
        "desc": "👻 Crei un'illusione visiva (senza suoni) che puoi muovere.",
        "effetto": "Illusione 4,5m × 4,5m che dura 10 minuti (concentrazione). Puoi muoverla",
        "quando": "Distrazioni, inganni, creare copertura illusoria"
    },
    "Caduta Morbida": {
        "desc": "🪶 Un alleato che cade scende dolcemente come una piuma.",
        "effetto": "Reazione. Velocità caduta 18m/round, 0 danni, atterra in piedi",
        "quando": "Qualcuno viene buttato giù, cade in un burrone, ecc."
    },
    "Passo Veloce": {
        "desc": "⚡ Acceleri magicamente un alleato.",
        "effetto": "Azione bonus. Un alleato raddoppia velocità fino a fine suo turno + Disimpegno gratis",
        "quando": "Alleato deve raggiungere un nemico lontano o fuggire"
    }
}

# ============ FUNZIONE CREAZIONE ============
def crea_personaggio():
    """Form completo per creare un personaggio D&D"""
    
    st.title("🎭 Creazione del Personaggio")
    st.markdown("*Crea il tuo eroe per l'avventura che sta per iniziare...*")
    st.markdown("---")
    
    # ========== NOME ==========
    st.subheader("📜 Identità")
    nome = st.text_input(
        "**Nome del Personaggio**",
        placeholder="Es: Thorin Scudodiquercia, Elara Lunargento...",
        help="Scegli un nome evocativo per il tuo eroe!"
    )
    
    # ========== RAZZA ==========
    st.markdown("---")
    st.subheader("🧬 Razza")
    
    razza = st.selectbox(
        "Scegli la tua razza",
        list(RAZZE.keys()),
        help="La razza determina aspetto, abilità innate e bonus statistiche"
    )
    
    # Mostra dettagli razza
    razza_data = RAZZE[razza]
    st.info(razza_data["desc"])
    
    with st.expander("📊 Tratti Razziali"):
        for tratto in razza_data["tratti"]:
            st.write(f"• {tratto}")
    
    # ========== CLASSE ==========
    st.markdown("---")
    st.subheader("⚔️ Classe")
    
    classe = st.selectbox(
        "Scegli la tua classe",
        list(CLASSI.keys()),
        help="La classe determina le tue abilità in combattimento e fuori"
    )
    
    # Mostra dettagli classe
    classe_data = CLASSI[classe]
    st.info(classe_data["desc"])
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.caption(f"❤️ **Dado Vita**: d{classe_data['hp_base']}")
        st.caption(f"🎯 **Ruolo**: {classe_data['ruolo']}")
    with col_c2:
        st.caption(f"⚔️ **Armi**: {classe_data['armi']}")
        st.caption(f"📈 **Difficoltà**: {classe_data['difficolta']}")
    
    with st.expander("🎯 Abilità di Classe"):
        for abil in classe_data["abilita"]:
            st.write(f"• {abil}")
    
    # ========== BACKGROUND ==========
    st.markdown("---")
    st.subheader("📖 Background")
    
    background = st.selectbox(
        "Qual è la tua storia?",
        list(BACKGROUND.keys()),
        help="Il background rappresenta la tua vita prima dell'avventura"
    )
    
    bg_data = BACKGROUND[background]
    st.info(bg_data["desc"])
    st.caption(f"**Competenze**: {', '.join(bg_data['competenze'])}")
    st.caption(f"**Tratto**: {bg_data['tratto']}")
    
    # ========== LIVELLO ==========
    st.markdown("---")
    livello = st.slider("**Livello**", 1, 5, 3, help="Livello iniziale del personaggio")
    
    # ========== STATISTICHE ==========
    st.markdown("---")
    st.subheader("📊 Punteggi Caratteristica")
    st.caption("⚠️ I valori standard vanno da 8 a 15. Il bonus razziale viene applicato dopo.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        forza = st.number_input("💪 Forza", 3, 18, 10, help="Forza fisica, attacchi in mischia")
        destrezza = st.number_input("🏃 Destrezza", 3, 18, 10, help="Agilità, attacchi a distanza, CA")
    
    with col2:
        costituzione = st.number_input("🛡️ Costituzione", 3, 18, 10, help="Resistenza, punti ferita")
        intelligenza = st.number_input("🧠 Intelligenza", 3, 18, 10, help="Conoscenze, alcuni incantesimi")
    
    with col3:
        saggezza = st.number_input("🦉 Saggezza", 3, 18, 10, help="Percezione, intuito, alcuni incantesimi")
        carisma = st.number_input("💬 Carisma", 3, 18, 10, help="Persuasione, presenza, alcuni incantesimi")
    
    # Applica bonus razza
    bonus_razza = razza_data["bonus"]
    forza_tot = forza + bonus_razza["for"]
    destrezza_tot = destrezza + bonus_razza["des"]
    costituzione_tot = costituzione + bonus_razza["cos"]
    intelligenza_tot = intelligenza + bonus_razza["int"]
    saggezza_tot = saggezza + bonus_razza["sag"]
    carisma_tot = carisma + bonus_razza["car"]
    
    # Mostra totali con bonus
    st.success(f"**📊 Con Bonus Razziali**: FOR {forza_tot} | DES {destrezza_tot} | COS {costituzione_tot} | INT {intelligenza_tot} | SAG {saggezza_tot} | CAR {carisma_tot}")
    
    # ========== INCANTESIMI (solo caster) ==========
    incantesimi_scelti = []
    if classe in ["Mago", "Chierico"]:
        st.markdown("---")
        st.subheader("✨ Incantesimi Conosciuti")
        st.caption(f"Scegli 3-5 incantesimi di 1° livello per il tuo {classe}")
        
        for inc_nome, inc_data in INCANTESIMI_LV1.items():
            with st.expander(f"✨ {inc_nome}"):
                st.write(inc_data["desc"])
                st.caption(f"**Effetto**: {inc_data['effetto']}")
                st.caption(f"**Quando usarlo**: {inc_data['quando']}")
                
                if st.checkbox(f"Seleziona {inc_nome}", key=f"spell_{inc_nome}"):
                    if inc_nome not in incantesimi_scelti:
                        incantesimi_scelti.append(inc_nome)
        
        if len(incantesimi_scelti) > 0:
            st.info(f"**Incantesimi selezionati**: {', '.join(incantesimi_scelti)}")
    
    # ========== EQUIPAGGIAMENTO ==========
    st.markdown("---")
    st.subheader("⚔️ Equipaggiamento Iniziale")
    
    equipaggiamento_base = {
        "Guerriero": ["Spada lunga", "Scudo", "Armatura di maglia", "Lancia"],
        "Mago": ["Bacchetta magica", "Libro degli incantesimi", "Pugnale", "Veste da mago"],
        "Chierico": ["Mazza", "Scudo", "Simbolo sacro", "Armatura di scaglie", "Libro di preghiere"],
        "Ladro": ["Spada corta", "Arco corto (20 frecce)", "Arnesi da scasso", "Armatura di cuoio", "Rampino e corda"],
        "Ranger": ["Spada lunga", "Arco lungo (20 frecce)", "Armatura di cuoio borchiato", "Corno da caccia"]
    }
    
    inventario_base = equipaggiamento_base.get(classe, []) + [
        "Zaino",
        "Sacco a pelo",
        "Corda di canapa (15m)",
        "Razione da viaggio (5 giorni)",
        "Torcia (3)",
        "Borraccia",
        f"{10 + livello * 5} monete d'oro"
    ]
    
    col_eq1, col_eq2 = st.columns(2)
    
    with col_eq1:
        st.write("**⚔️ Equipaggiamento di classe:**")
        for item in equipaggiamento_base.get(classe, []):
            st.write(f"• {item}")
    
    with col_eq2:
        st.write("**🎒 Equipaggiamento base:**")
        for item in ["Zaino", "Sacco a pelo", "Corda (15m)", "Razioni (5)", "Torce (3)", "Borraccia"]:
            st.write(f"• {item}")
    
    # Calcola HP massimi
    hp_base = classe_data['hp_base']
    mod_cos = (costituzione_tot - 10) // 2
    hp_max = hp_base + (hp_base + mod_cos) * (livello - 1)
    
    st.markdown("---")
    col_hp1, col_hp2 = st.columns(2)
    with col_hp1:
        st.metric("❤️ Punti Ferita Massimi", hp_max)
    with col_hp2:
        st.metric("💰 Monete d'Oro Iniziali", 10 + livello * 5)
    
    # ========== CONFERMA ==========
    st.markdown("---")
    
    if st.button("✅ CREA PERSONAGGIO", type="primary", use_container_width=True):
        # Validazioni
        if not nome or len(nome.strip()) < 2:
            st.error("⚠️ Inserisci un nome valido (almeno 2 caratteri)!")
            return None
        
        if classe in ["Mago", "Chierico"] and len(incantesimi_scelti) < 3:
            st.error(f"⚠️ Seleziona almeno 3 incantesimi per il tuo {classe}!")
            return None
        
        # Crea dizionario personaggio
        return {
            "nome": nome.strip(),
            "razza": razza,
            "classe": classe,
            "background": background,
            "livello": livello,
            "forza": forza_tot,
            "destrezza": destrezza_tot,
            "costituzione": costituzione_tot,
            "intelligenza": intelligenza_tot,
            "saggezza": saggezza_tot,
            "carisma": carisma_tot,
            "hp_max": hp_max,
            "hp": hp_max,
            "incantesimi": incantesimi_scelti,
            "inventario": inventario_base,
            "abilita": classe_data['abilita'],
            "monete_oro": 10 + livello * 5
        }
    
    return None