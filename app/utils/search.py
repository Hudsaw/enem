import re
import unicodedata

def normalize_text(text):
    """
    Normaliza o texto para ignorar maiúsculas/minúsculas e acentos.

    :param text: Texto a ser normalizado.
    :return: Texto normalizado.
    """
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    return text.lower()

def search_words_in_text(text, words, pdf_filename):
    """
    Busca múltiplas palavras no texto e retorna os trechos que as contêm,
    delimitados por "QUEST", juntamente com o número da questão.

    :param text: Texto onde a busca será realizada.
    :param words: Lista de palavras a serem buscadas.
    :param pdf_filename: Nome do arquivo PDF (sem extensão).
    :return: Lista de dicionários com os trechos encontrados e metadados.
    """
    # Normaliza o texto e as palavras
    normalized_text = normalize_text(text)
    normalized_words = [normalize_text(word) for word in words]

    # Divide o texto em trechos (usando "QUEST" como delimitador)
    trechos = text.split('QUEST')

    # Filtra os trechos que contêm todas as palavras
    results = []
    for i in range(1, len(trechos)):  # Ignora o primeiro trecho (antes da primeira "QUEST")
        trecho = 'QUEST' + trechos[i]  # Adiciona "QUEST" de volta ao trecho
        normalized_trecho = normalize_text(trecho)
        if all(word in normalized_trecho for word in normalized_words):
            # Extrai o número da questão usando regex
            match = re.search(r'QUEST(ÃO|AO)?\s*(\d+)', trecho, re.IGNORECASE)
            numero_questao = match.group(2) if match else "Desconhecido"

            # Adiciona o resultado com metadados
            results.append({
                'arquivo': pdf_filename,
                'numero_questao': numero_questao,
                'trecho': trecho.strip()
            })

    return results