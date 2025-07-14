#!/bin/bash
export PATH="$PATH:/c/Development/AudioBook/tools"
####################################################################################
# AUDIBLE AAX TO M4B CONVERTER
#
# This script is designed to decrypt Audible AAX audiobook files and convert them
# into the M4B format. It also extracts and embeds the audiobook cover art into the
# converted M4B files.
#
# REQUIREMENTS:
# - ffmpeg: Used for decryption of AAX files and conversion to M4B format.
# - AtomicParsley: Used for embedding artwork into M4B files.
#
# INSTALLATION INSTRUCTIONS:
# macOS:
#   - ffmpeg: Install via Homebrew with 'brew install ffmpeg'
#   - AtomicParsley: Install via Homebrew with 'brew install AtomicParsley'
# Windows:
#   - ffmpeg: Download from https://ffmpeg.org/download.html or install via Chocolatey with 'choco install ffmpeg'
#   - AtomicParsley: Download from https://github.com/wez/atomicparsley or install via Chocolatey with 'choco install atomicparsley'
# Linux:
#   - ffmpeg: Install via package manager, e.g., 'sudo apt-get install ffmpeg' (Debian/Ubuntu)
#   - AtomicParsley: Install via package manager, e.g., 'sudo apt-get install atomicparsley' (Debian/Ubuntu)
#
# CONFIGURATION:
# The script uses the following configurable variables:
# - AUDIBLE_ACTIVATION_BYTES: Your unique Audible activation bytes. If not set in
#   the script, it will default to the value of the environment variable with the
#   same name.
# - AUDIBLE_ARCHIVED_DIR: Directory to move original AAX files after processing.
# - AUDIBLE_OUTPUT_DIR: Directory to copy converted M4B files.
#
# USAGE:
# Run the script with one or more AAX files as arguments. Example:
# ./audibleConvert.sh book1.aax book2.aax
#
# NOTES:
# - The script checks for the required tools (ffmpeg and AtomicParsley) at the
#   beginning and exits if they are not installed.
# - It uses the AUDIBLE_ACTIVATION_BYTES for decrypting the AAX files.
# - Temporary files are created during processing and are cleaned up on exit.
#
########                   PS C:\Development\AudioBook> ./aaxToM4b/audibleDecrypt.sh
####################################################################################


# Configuration
# Set your activation bytes here or export as environment variable AUDIBLE_ACTIVATION_BYTES
#ACTIVATION_BYTES="${AUDIBLE_ACTIVATION_BYTES_GB:-}"
#if [[ -z "$ACTIVATION_BYTES" ]]; then
#  echo "Error: AUDIBLE_ACTIVATION_BYTES is not set."
#  echo "Please export your activation bytes as an environment variable or set in the script."
#  exit 1
#else
#  echo "Using activation bytes: $ACTIVATION_BYTES"
#fi

#AUDIBLE_ACTIVATION_BYTES="c86fe509" # Use environment variable if not set here Audible Gianpaolo
#AUDIBLE_ACTIVATION_BYTES="692ac312" # Use environment variable if not set here Audible Adriana

# I save the aax files to a network drive for archiving.
AUDIBLE_ARCHIVED_DIR="$(pwd)/aax" # Directory to move original AAX files after processing
# I save the converted m4b files to a network drive for archiving.
AUDIBLE_OUTPUT_DIR="$(pwd)/m4b" # Directory to copy converted M4B files
mkdir -p "$AUDIBLE_ARCHIVED_DIR" "$AUDIBLE_OUTPUT_DIR"
# End of Configuration

# Function to create a unique temporary file
create_temp_file() {
    mktemp /tmp/audible_script.XXXXXX
}

# Setup a trap to clean up temporary files on EXIT and INTERRUPT
cleanup() {
    echo "Cleaning up temporary files..."
    rm -f /tmp/audible_script.*
}
trap cleanup EXIT INT

# Check for required programs
if ! command -v ffmpeg &> /dev/null || ! command -v AtomicParsley &> /dev/null; then
    echo "ffmpeg and AtomicParsley are required but not installed. Exiting."
    read -p "Debug1: Press any key to continue..."
    exit 1
fi

# Check if AUDIBLE_ACTIVATION_BYTES is set
if [ -z "$AUDIBLE_ACTIVATION_BYTES" ]; then
    echo "Error: AUDIBLE_ACTIVATION_BYTES is not set."
    read -p "Debug2: Press any key to continue..."
    exit 1
fi
# Function to extract artwork
extract_artwork() {
    local artworkFile
    artworkFile=$(create_temp_file)
    local baseName="${1%.*}"
    ffmpeg -activation_bytes "$AUDIBLE_ACTIVATION_BYTES" -i "$1" -vcodec copy "${baseName}.jpg" > "$artworkFile" 2>&1
    local status=$?
    cat "$artworkFile"
    rm "$artworkFile"
    return $status
}
# Function to decrypt aax file
decrypt_aax() {
    local decryptionFile
    decryptionFile=$(create_temp_file)
    local baseName="${1%.*}"
    ffmpeg -activation_bytes "$AUDIBLE_ACTIVATION_BYTES" -i "$1" -vn -c:a copy "${baseName}.m4b" > "$decryptionFile" 2>&1
    local status=$?
    cat "$decryptionFile"
    rm "$decryptionFile"
    return $status
}

# Function to bundle m4b file with artwork
bundle_m4b() {
    local bundleFile
    bundleFile=$(create_temp_file)
    local baseName="${1%.*}"
    if [ -f "${baseName}.jpg" ]; then
        AtomicParsley "${baseName}.m4b" --artwork "${baseName}.jpg" --overWrite > "$bundleFile" 2>&1
        local status=$?
        cat "$bundleFile"
        rm "$bundleFile"
        return $status
    fi
}


# Elenco dei file da processare (tutti i .aax nella cartella corrente)
audiobook_list_Gianpaolo=( *.aax )

echo "Elenco dei file da processare: ${audiobook_list_Gianpaolo[*]}"
read -p "Debug3: Press any key to continue..."
# Check if the list is empty
if [ ${#audiobook_list_Gianpaolo[@]} -eq 0 ]; then
    echo "Nessun file AAX trovato nella cartella corrente."
    exit 0
fi
# Check if the directories exist, if not create them
mkdir -p "$AUDIBLE_ARCHIVED_DIR" "$AUDIBLE_OUTPUT_DIR" || { echo "Errore nella creazione delle directory di output." >&2; exit 1; }
# Check if the directories are writable
if [ ! -w "$AUDIBLE_ARCHIVED_DIR" ] || [ ! -w "$AUDIBLE_OUTPUT_DIR" ]; then
    echo "Le directory di output non sono scrivibili. Verifica i permessi." >&2
    exit 1
fi
# Check if the activation bytes are set
if [ -z "$AUDIBLE_ACTIVATION_BYTES" ]; then
    echo "Errore: AUDIBLE_ACTIVATION_BYTES non è impostato." >&2
    exit 1
fi
echo "Utilizzo dei byte di attivazione: $AUDIBLE_ACTIVATION_BYTES"
# Check if the activation bytes are valid (length should be 8 characters)
if [[ ! "$AUDIBLE_ACTIVATION_BYTES" =~ ^[0-9a-fA-F]{8}$ ]]; then
    echo "Errore: AUDIBLE_ACTIVATION_BYTES deve essere una stringa esadecimale di 8 caratteri." >&2
    exit    1
fi  

# Main loop
originalDirectory="$PWD"

for audibleBook in "${audiobook_list_Gianpaolo[@]}"; do
    extension="${audibleBook##*.}"
    baseName="${audibleBook%.*}"
    m4bFile="$AUDIBLE_OUTPUT_DIR/${baseName}.m4b"
    
    # Salta se il file M4B esiste già
    if [ -f "$m4bFile" ]; then
        echo "Il file $m4bFile esiste già, salto la generazione."
        continue
    fi
    # Salta se il file di input non esiste (probabilmente già processato e spostato)
    if [ ! -f "$audibleBook" ]; then
        echo "Controllo esistenza file: $PWD/$audibleBook"
        echo "Il file di input $audibleBook non esiste, probabilmente già processato e spostato. Salto."
        continue
    fi

    # Check if the file contains a path
    if [[ "$audibleBook" == */* ]]; then
        directory="${audibleBook%/*}"
    else
        directory="$PWD"
    fi

    if [ "$extension" != "aax" ]; then
        echo "Skipping $audibleBook -- must be AAX"
        continue
    fi

    if [ -f "$audibleBook" ]; then
        if [ "$PWD" != "$directory" ]; then
            cd "$directory" || exit 1
        fi


        echo "Processing ${audibleBook}:"

        if ! extract_artwork "$audibleBook"; then
            echo "Artwork extraction failed."
            continue
        fi

        if ! decrypt_aax "$audibleBook"; then
            echo "Decryption failed."
            exit 1
        fi

        if ! bundle_m4b "$audibleBook"; then
            echo "Bundling failed."
            exit 1
        fi

        rm -f "${baseName}.jpg"

        # Move and copy files if directories exist
        [ -d "$AUDIBLE_ARCHIVED_DIR" ] && mv -v "$audibleBook" "$AUDIBLE_ARCHIVED_DIR"
        [ -d "$AUDIBLE_OUTPUT_DIR" ] && cp -v "${baseName}.m4b" "$AUDIBLE_OUTPUT_DIR"
    fi
done

cd "$originalDirectory" || exit 1

read -p "Script terminato. Premi INVIO per chiudere la finestra..."