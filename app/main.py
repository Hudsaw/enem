import os
from app.utils.file_handling import extract_text_from_pdf, save_results_to_txt
from app.utils.search import search_words_in_text

def main():
    # Caminho da pasta onde estão os PDFs
    pdf_folder = 'data/'

    # Verifica se a pasta existe
    if not os.path.exists(pdf_folder):
        print(f"Erro: A pasta '{pdf_folder}' não foi encontrada.")
        return

    # Lista todos os arquivos PDF na pasta
    pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

    if not pdf_files:
        print(f"Nenhum arquivo PDF encontrado na pasta '{pdf_folder}'.")
        return

    # Palavras a serem buscadas
    words = input("Digite as palavras que deseja buscar (separadas por vírgula): ").split(',')

    # Remove espaços em branco e normaliza as palavras
    words = [word.strip() for word in words]

    # Processa cada PDF
    all_results = []
    for pdf_path in pdf_files:
        print(f"\nProcessando: {pdf_path}")
        text = extract_text_from_pdf(pdf_path)

        # Obtém o nome do arquivo (sem extensão)
        pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]

        # Busca as palavras no texto
        results = search_words_in_text(text, words, pdf_filename)

        if results:
            print(f"\nResultados para as palavras '{', '.join(words)}':")
            for result in results:
                print(f"- Trecho: {result['trecho'][:100]}...")  # Exibe os primeiros 100 caracteres
                all_results.append(result)
        else:
            print(f"Nenhum resultado encontrado para as palavras '{', '.join(words)}'.")

    # Salva todos os resultados em um único arquivo TXT
    if all_results:
        save_results_to_txt(all_results, words)

if __name__ == "__main__":
    main()