import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image

class ReportGenerator:
    """
    Classe para gerar um relatório em PDF a partir de uma lista ordenada de imagens.
    """

    def __init__(self, report_path='../reports/relatorio_final.pdf', images_path='../images/'):
        """
        Inicializa o gerador de relatórios.

        Parâmetros:
        - report_path (str): Caminho para salvar o arquivo PDF gerado.
        - images_path (str): Caminho onde as imagens estão localizadas.
        """
        self.report_path = report_path
        self.images_path = images_path
        self.image_order = [
            "Capa.png", ## Substitua essa pela capa da sua empresa, no meu caso, estou utilizando da Liga de Mercado Financeiro do Inteli (@Inteli_Finance [https://www.linkedin.com/company/inteli-finance][https://www.instagram.com/inteli_finance/])
            "calculate_metrics_results.png",
            "PMC Ampliado.png",
            "Automoveis.png",
            "Materiais Construção.png",
            "Hipermercados e supermercados.png",
            "Combustíveis e lubrificantes.png",
            "Artigos farmacêuticos, médicos, ortopédicos, de perfumaria e cosméticos.png",
            "Livros, jornais, revistas e papelaria.png",
            "Móveis e eletrodomésticos.png",
            "Tecidos, vestuário e calçados.png",
            "all_variables.png"
        ]
    
    def create_report(self):
        """
        Cria um relatório PDF com as imagens listadas na ordem especificada.

        - Verifica se cada imagem existe no diretório especificado.
        - Redimensiona cada imagem para caber na página.
        - Adiciona cada imagem ao PDF, uma por página.
        - Salva o PDF no caminho especificado ao final.
        """
        # Cria o diretório de saída, se ele não existir
        os.makedirs(os.path.dirname(self.report_path), exist_ok=True)
        
        # Inicializa o canvas para o PDF
        pdf = canvas.Canvas(self.report_path, pagesize=letter)
        largura_pagina, altura_pagina = letter
        
        # Itera sobre a lista de imagens na ordem especificada
        for imagem_nome in self.image_order:
            caminho_imagem = os.path.join(self.images_path, imagem_nome)
            
            # Verifica se o arquivo de imagem existe
            if os.path.exists(caminho_imagem):
                # Abre a imagem e ajusta o tamanho para caber na página
                with Image.open(caminho_imagem) as img:
                    largura_img, altura_img = img.size
                    proporcao = min(largura_pagina / largura_img, altura_pagina / altura_img)
                    largura_img_redimensionada = largura_img * proporcao
                    altura_img_redimensionada = altura_img * proporcao

                    # Centraliza a imagem na página
                    x = (largura_pagina - largura_img_redimensionada) / 2
                    y = (altura_pagina - altura_img_redimensionada) / 2

                    # Adiciona a imagem ao PDF
                    pdf.drawImage(caminho_imagem, x, y, largura_img_redimensionada, altura_img_redimensionada)
                    pdf.showPage()  # Finaliza a página e cria uma nova para a próxima imagem
            else:
                print(f"Imagem não encontrada: {imagem_nome}")

        # Salva o PDF
        pdf.save()
        print(f'Relatório PDF gerado com sucesso: {self.report_path}')