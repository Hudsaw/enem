import os
import PyPDF2

def extract_text_from_pdf(pdf_path):
    """
    Extrai o texto de um arquivo PDF e salva em um arquivo TXT para reutilização.

    :param pdf_path: Caminho do arquivo PDF.
    :return: Texto extraído do PDF.
    """
    # Cria a pasta data/txt/ se não existir
    txt_folder = os.path.join(os.path.dirname(pdf_path), 'txt')
    os.makedirs(txt_folder, exist_ok=True)

    # Define o caminho do arquivo TXT correspondente
    txt_filename = os.path.splitext(os.path.basename(pdf_path))[0] + '.txt'
    txt_path = os.path.join(txt_folder, txt_filename)

    # Verifica se o arquivo TXT já existe
    if os.path.exists(txt_path):
        print(f"Lendo texto pré-convertido: {txt_path}")
        with open(txt_path, 'r', encoding='utf-8') as file:
            return file.read()

    # Se o arquivo TXT não existir, converte o PDF
    print(f"Convertendo PDF para TXT: {pdf_path}")
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()

        # Salva o texto em um arquivo TXT
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

        return text

import os

def save_results_to_txt(results, words, base_folder='results/'):
    """
    Salva todos os trechos encontrados em um único arquivo TXT,
    com o nome baseado nas palavras buscadas, incluindo a letra do gabarito.

    :param results: Lista de dicionários com os trechos encontrados e metadados.
    :param words: Lista de palavras buscadas.
    :param base_folder: Pasta base onde os resultados serão salvos.
    """
    # Cria a pasta results/ se não existir
    os.makedirs(base_folder, exist_ok=True)

    # Define o nome do arquivo com base nas palavras buscadas
    filename = '_'.join(words) + '.txt'
    filepath = os.path.join(base_folder, filename)

    # Agrupa todos os trechos em uma única string
    conteudo = ""
    for result in results:
        # Define o caminho do arquivo de gabarito
        gabarito_path = os.path.join('app/data/txt', f"{result['arquivo']}_GB.txt")

        # Obtém a letra do gabarito
        letra_gabarito = get_gabarito_letter(gabarito_path, result['numero_questao'])

        # Adiciona o trecho e a letra do gabarito ao conteúdo
        conteudo += f"{result['arquivo']}/{result['trecho']}\nResposta: {letra_gabarito}\n\n{'='*50}\n\n"

    # Salva o conteúdo no arquivo TXT
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(conteudo)

    print(f"Todos os trechos salvos em {filepath}")


def get_gabarito_letter(gabarito_path, numero_questao):
    """
    Obtém a letra correta do gabarito para o número da questão.

    :param gabarito_path: Caminho do arquivo de gabarito.
    :param numero_questao: Número da questão.
    :return: Letra correta ou "?" se não encontrada.
    """
    if not os.path.exists(gabarito_path):
        return "?"

    with open(gabarito_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 2 and parts[0] == numero_questao:
                return parts[1]  # Retorna a letra correta
    return "?"