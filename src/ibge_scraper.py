from playwright.sync_api import sync_playwright
import os

class IBGEScraper:
    """
    Classe para realizar o scraping de dados do IBGE usando Playwright.
    """

    def __init__(self):
        """
        Inicializa o Playwright e o navegador Chromium para realizar as operações de scraping.
        """
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()

    def close(self):
        """
        Fecha o navegador e encerra o Playwright ao final das operações.
        """
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def download_indicadores_varejo(self):
        """
        Realiza o download dos indicadores de varejo do IBGE.

        Acessa a página de indicadores de varejo e seleciona categorias específicas.
        Em seguida, seleciona todos os meses disponíveis e inicia o download do arquivo Excel.
        """
        try:
            page = self.browser.new_page()
            page.goto("https://sidra.ibge.gov.br/tabela/8882")

            # Lista das categorias a serem selecionadas
            labels = [
                "Hipermercados e supermercados",
                "Tecidos, vestuário e calçados",
                "Móveis e eletrodomésticos",
                "Outros artigos de uso pessoal e doméstico",
                "Livros, jornais, revistas e papelaria",
                "Artigos farmacêuticos, médicos, ortopédicos, de perfumaria e cosméticos"
            ]
            # Caminho XPath para o elemento pai que contém as labels
            parent_element_xpath = "//div[@class='janela-borda-dados panel-body']//div[@class='lv-container']"
            for label in labels:
                label_xpath = f"{parent_element_xpath}//span[text()='{label}']/parent::div/button"
                page.locator(label_xpath).click()

            # Seleciona todos os meses
            select_all_months_button = 'xpath=/html/body/div[4]/div/div/div[1]/div[4]/div[6]/div/div[2]/div[3]/div/div[1]/div[1]/div/button[1]'
            page.locator(select_all_months_button).click()

            # Botão para iniciar o download
            download_button = 'xpath=/html/body/div[4]/div/div/div[1]/div[5]/div[2]/div/div[2]/button[2]'
            page.locator(download_button).click()

            # Define o caminho onde o arquivo será salvo
            save_dir = os.path.join(os.path.dirname(__file__), '../data')
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, 'indicadores_varejo.xlsx')

            # Espera o download ser concluído e salva o arquivo
            with page.expect_download() as download_info:
                page.fill('xpath=/html/body/div[6]/div/div/div[2]/div/div/div[1]/table/tbody/tr[1]/td[2]/input', save_path)
                page.locator('xpath=/html/body/div[6]/div/div/div[2]/div/div/div[2]/a').click()

            download = download_info.value
            download.save_as(save_path)

        except Exception as e:
            print(f"Erro ao fazer download dos indicadores de varejo: {e}")

    def pmc_ampliado(self):
        """
        Realiza o download do PMC ampliado do IBGE.

        Acessa a página do PMC ampliado e seleciona todos os meses disponíveis para download.
        Salva o arquivo em um diretório específico.
        """
        try:
            page = self.browser.new_page()
            page.goto("https://sidra.ibge.gov.br/tabela/8881")

            # Seleciona todos os meses
            select_all_months_button = 'xpath=/html/body/div[4]/div/div/div[1]/div[4]/div[5]/div/div[2]/div[3]/div/div[1]/div[1]/div/button[1]'
            page.locator(select_all_months_button).click()

            # Botão para iniciar o download
            download_button = 'xpath=/html/body/div[4]/div/div/div[1]/div[5]/div[2]/div/div[2]/button[2]'
            page.locator(download_button).click()

            # Define o caminho onde o arquivo será salvo
            save_dir = os.path.join(os.path.dirname(__file__), '../data')
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, 'pmc_ampliado.xlsx')

            # Espera o download ser concluído e salva o arquivo
            with page.expect_download() as download_info:
                page.fill('xpath=/html/body/div[6]/div/div/div[2]/div/div/div[1]/table/tbody/tr[1]/td[2]/input', save_path)
                page.locator('xpath=/html/body/div[6]/div/div/div[2]/div/div/div[2]/a').click()

            download = download_info.value
            download.save_as(save_path)

        except Exception as e:
            print(f"Erro ao fazer download do PMC ampliado: {e}")

    def automoveis(self):
        """
        Realiza o download dos dados de automóveis do IBGE.

        Acessa a página de indicadores de automóveis e seleciona todos os meses disponíveis.
        Salva o arquivo em um diretório específico.
        """
        try:
            page = self.browser.new_page()
            page.goto('https://sidra.ibge.gov.br/tabela/8884')

            # Seleciona todos os meses
            select_all_months_button = 'xpath=/html/body/div[4]/div/div/div[1]/div[4]/div[5]/div/div[2]/div[3]/div/div[1]/div[1]/div/button[1]'
            page.locator(select_all_months_button).click()

            # Botão para iniciar o download
            download_button = 'xpath=/html/body/div[4]/div/div/div[1]/div[5]/div[2]/div/div[2]/button[2]'
            page.locator(download_button).click()

            # Define o caminho onde o arquivo será salvo
            save_dir = os.path.join(os.path.dirname(__file__), '../data')
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, 'automoveis.xlsx')

            # Espera o download ser concluído e salva o arquivo
            with page.expect_download() as download_info:
                page.fill('xpath=/html/body/div[6]/div/div/div[2]/div/div/div[1]/table/tbody/tr[1]/td[2]/input', save_path)
                page.locator('xpath=/html/body/div[6]/div/div/div[2]/div/div/div[2]/a').click()

            download = download_info.value
            download.save_as(save_path)

        except Exception as e:
            print(f"Erro ao fazer download dos indicadores de automóveis: {e}")

    def materiais_construcao(self):
        """
        Realiza o download dos dados de materiais de construção do IBGE.

        Acessa a página de indicadores de materiais de construção e seleciona todos os meses disponíveis.
        Salva o arquivo em um diretório específico.
        """
        try:
            page = self.browser.new_page()
            page.goto('https://sidra.ibge.gov.br/tabela/8757')

            # Seleciona todos os meses
            select_all_months_button = 'xpath=/html/body/div[4]/div/div/div[1]/div[4]/div[5]/div/div[2]/div[3]/div/div[1]/div[1]/div/button[1]'
            page.locator(select_all_months_button).click()

            # Botão para iniciar o download
            download_button = 'xpath=/html/body/div[4]/div/div/div[1]/div[5]/div[2]/div/div[2]/button[2]'
            page.locator(download_button).click()

            # Define o caminho onde o arquivo será salvo
            save_dir = os.path.join(os.path.dirname(__file__), '../data')
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, 'materiais_construcao.xlsx')

            # Espera o download ser concluído e salva o arquivo
            with page.expect_download() as download_info:
                page.fill('xpath=/html/body/div[6]/div/div/div[2]/div/div/div[1]/table/tbody/tr[1]/td[2]/input', save_path)
                page.locator('xpath=/html/body/div[6]/div/div/div[2]/div/div/div[2]/a').click()

            download = download_info.value
            download.save_as(save_path)

        except Exception as e:
            print(f"Erro ao fazer download dos indicadores de materiais de construção: {e}")
