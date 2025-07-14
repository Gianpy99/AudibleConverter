# AudibleConverter

Un toolkit completo per convertire i file audio Audible AAX nel formato M4B per uso personale.

## Panoramica

AudibleConverter è una suite di strumenti che permette di:
- Ottenere i bytes di attivazione dal tuo account Audible
- Convertire i file .aax di Audible in formato .m4b
- Estrarre e incorporare le copertine nei file convertiti
- Organizzare automaticamente i file originali e convertiti

Questo progetto è stato creato come risposta all'introduzione di contenuti pubblicitari nell'app Audible dopo l'acquisizione da parte di Amazon, offrendo un'alternativa per utilizzare i propri audiolibri in Apple Books o altri lettori compatibili.

## Componenti del Progetto

### 1. **audible-activator** 
Script Python per recuperare i bytes di attivazione dal tuo account Audible.

### 2. **aaxToM4b**
Script bash per convertire i file .aax in formato .m4b con supporto per metadati e copertine.

### 3. **tools**
Binari pre-compilati per Windows:
- `ffmpeg.exe` - Per la decrittazione e conversione audio
- `AtomicParsley.exe` - Per l'embedding dei metadati

### 4. **Cartelle di Output**
- `aax/` - Directory per archiviare i file AAX originali
- `m4b/` - Directory per i file M4B convertiti

## Prerequisiti

### Software Richiesto
- **Python 3.6+** (per audible-activator)
- **Bash** (WSL su Windows o terminale Unix/Linux)
- **ffmpeg** - Per la conversione audio
- **AtomicParsley** - Per l'embedding dei metadati

### Dipendenze Python
```bash
pip install requests selenium
```

### Browser e WebDriver
- **Google Chrome** o **Firefox**
- **ChromeDriver** o **GeckoDriver** corrispondente

## Installazione

### 1. Clona il Repository
```bash
git clone <repository-url>
cd AudibleConverter
```

### 2. Installa le Dipendenze Python
```bash
cd audible-activator
pip install -r requirements.txt
```

### 3. Configura WebDriver
Scarica ChromeDriver da [qui](https://sites.google.com/a/chromium.org/chromedriver/downloads) e posizionalo nella cartella `audible-activator/`.

### 4. Verifica i Tool
I binari per Windows sono inclusi nella cartella `tools/`. Per altri sistemi operativi:

**macOS:**
```bash
brew install ffmpeg atomicparsley
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg atomicparsley
```

**Windows (Chocolatey):**
```bash
choco install ffmpeg atomicparsley
```

## Utilizzo

### Passo 1: Ottenere i Bytes di Attivazione

```bash
cd audible-activator
python audible-activator.py
```

Opzioni disponibili:
- `-l de` - Per account tedeschi
- `-l uk` - Per account britannici
- `-l au` - Per account australiani
- `-f` - Usa Firefox invece di Chrome
- `-d` - Modalità debug (utile per 2FA)

### Passo 2: Configurare la Conversione

Modifica il file `aaxToM4b/audibleDecrypt.sh` e imposta:
```bash
AUDIBLE_ACTIVATION_BYTES="tuoi_bytes_qui"
```

Oppure esporta come variabile d'ambiente:
```bash
export AUDIBLE_ACTIVATION_BYTES="tuoi_bytes_qui"
```

### Passo 3: Convertire i File AAX

```bash
cd aaxToM4b
./audibleDecrypt.sh libro1.aax libro2.aax
```

## Funzionalità

### audible-activator
- ✅ Recupero automatico dei bytes di attivazione
- ✅ Supporto per account multi-regionali
- ✅ Compatibilità con 2FA
- ✅ Supporto per Firefox e Chrome
- ✅ Modalità debug avanzata

### aaxToM4b
- ✅ Conversione AAX → M4B
- ✅ Estrazione automatica delle copertine
- ✅ Embedding dei metadati
- ✅ Organizzazione automatica dei file
- ✅ Gestione degli errori
- ✅ Pulizia automatica dei file temporanei

## Struttura del Progetto

```
AudibleConverter/
├── audible-activator/          # Script per ottenere i bytes di attivazione
│   ├── audible-activator.py    # Script principale
│   ├── requirements.txt        # Dipendenze Python
│   └── README.md              # Documentazione dettagliata
├── aaxToM4b/                  # Script di conversione
│   ├── audibleDecrypt.sh      # Script bash principale
│   └── README.md              # Documentazione conversione
├── tools/                     # Binari per Windows
│   ├── ffmpeg.exe            # FFmpeg per Windows
│   └── AtomicParsley.exe     # AtomicParsley per Windows
├── aax/                       # Directory file AAX originali
├── m4b/                       # Directory file M4B convertiti
└── activation.blob            # File di attivazione generato
```

## Risoluzione Problemi

### Errori Comuni

**"Internal service error has occurred"**
- Contatta il supporto Audible per pulire i tuoi slot di attivazione (max 8)

**"Activation loop"**
- Tutti gli slot di attivazione sono in uso
- Attendi 30 minuti o contatta il supporto

**"ffmpeg not found"**
- Verifica che ffmpeg sia installato e nel PATH
- Su Windows, usa i binari nella cartella `tools/`

**"Too many authentication attempts"**
- Ban temporaneo di 30 minuti
- Usa la modalità debug (`-d`) per diagnosticare

### Debug Avanzato

Estrai il checksum SHA1 da un file AAX:
```bash
ffprobe test.aax
```

Verifica i bytes di attivazione:
```bash
ffplay -activation_bytes TUOI_BYTES file.aax
```

## Considerazioni Legali

⚠️ **IMPORTANTE**: Questo progetto è destinato **esclusivamente all'uso personale**.

- Non "cracka" il DRM, ma utilizza la tua chiave di decrittazione personale
- Utilizzalo solo per i tuoi audiolibri acquistati legalmente
- Non condividere i file decrittati pubblicamente
- Rispetta i termini di servizio di Audible
- Supporta autori ed editori acquistando contenuti originali

## Disclaimer

Gli utenti devono assicurarsi di rispettare i termini di servizio di Audible e le leggi applicabili riguardo l'uso di contenuti protetti da DRM. Questo strumento è fornito "as-is" senza garanzie.

## Contributi

I contributi sono benvenuti! Per favore:
1. Fai un fork del repository
2. Crea un branch per la tua feature
3. Committa le tue modifiche
4. Apri una Pull Request

## Licenza

Questo progetto include componenti con licenze diverse:
- `audible-activator/` - Vedi LICENSE nella rispettiva cartella
- `aaxToM4b/` - Vedi LICENSE nella rispettiva cartella

## Supporto

Per problemi o domande:
1. Controlla la documentazione esistente
2. Cerca nei README specifici di ogni componente
3. Utilizza la modalità debug per diagnosticare problemi
4. Apri una issue con dettagli completi del problema

---

*Ultimo aggiornamento: Luglio 2025*
