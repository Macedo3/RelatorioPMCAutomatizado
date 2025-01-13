from ibge_scraper import IBGEScraper
from data_processor import DataProcessor
from report_generator import ReportGenerator

def main():
    """
    Função principal que executa o pipeline de dados, realizando as etapas de coleta, processamento e geração de relatórios.

    Etapas executadas:
    1. Cria instâncias das classes IBGEScraper, DataProcessor e ReportGenerator para cada etapa do pipeline.
    2. Realiza o download dos dados do IBGE usando a classe IBGEScraper.
    3. Processa os dados baixados para limpeza e cálculo de métricas relevantes usando a classe DataProcessor.
    4. Gera gráficos a partir dos dados processados.
    5. Cria um relatório em PDF contendo as métricas e os gráficos gerados usando a classe ReportGenerator.
    """

    # Criação das instâncias das classes
    scraper = IBGEScraper()
    processor = DataProcessor()
    generator = ReportGenerator()

    # Download dos dados em Excel
    scraper.download_indicadores_varejo()
    scraper.pmc_ampliado()
    scraper.automoveis()
    scraper.materiais_construcao()

    # Processamento dos dados
    cleaned_data = processor.clean_data()                 # Limpeza e estruturação dos dados
    metrics = processor.calculate_metrics(cleaned_data)   # Cálculo de métricas sobre os dados limpos
    plots = processor.generate_plots(cleaned_data)        # Geração de gráficos a partir dos dados processados

    # Geração do relatório final
    generator.create_report()

if __name__ == "__main__":
    main()