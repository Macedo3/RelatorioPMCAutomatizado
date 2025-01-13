# Documentação do Projeto: Relatório Automatizado da Pesquisa Mensal do Comércio do Brasil

## Objetivo do Projeto

Este projeto foi desenvolvido para gerar um **relatório automatizado** contendo gráficos e tabelas com os principais dados da Pesquisa Mensal do Comércio (PMC) do Brasil, realizada pelo IBGE. O objetivo é permitir que o relatório seja gerado de forma automatizada a partir de dados coletados do site do IBGE, com mínima intervenção manual.

O resultado final é um **PDF com os gráficos e tabelas** formatados para visualização das principais métricas do setor de comércio brasileiro, replicável em qualquer ambiente que rode o script principal.

## Estrutura do Projeto

O projeto está dividido em três módulos principais, além de um script principal de execução. Cada módulo desempenha uma função específica no processo de coleta, processamento, visualização e geração do relatório final. 

### Módulos e Funções

1. **IBGEScraper** (`ibge_scraper.py`): Responsável por coletar os dados do IBGE.
2. **DataProcessor** (`data_processor.py`): Responsável por processar e limpar os dados coletados.
3. **ReportGenerator** (`report_generator.py`): Gera o relatório em PDF com os gráficos e métricas calculadas.
4. **Script Principal** (`main.py`): Orquestra a execução do pipeline completo.

### Estrutura de Pastas e Arquivos

O projeto possui a seguinte estrutura de diretórios:
```plaintext
.
└── src
    ├── main.py                    # Script principal de execução do pipeline
    ├── ibge_scraper.py            # Módulo para coleta de dados do IBGE
    ├── data_processor.py          # Módulo para processamento e limpeza dos dados
    ├── report_generator.py        # Módulo para geração do relatório em PDF
    ├── data                       # Pasta onde os dados baixados serão salvos
    ├── images                     # Pasta onde os gráficos gerados serão salvos
    └── reports                    # Pasta onde o relatório final em PDF será salvo
```

## Descrição dos Módulos

### 1. `IBGEScraper` - Coleta de Dados

Este módulo usa a biblioteca **Playwright** para acessar o site do IBGE, navegar até as páginas dos dados de interesse e baixar arquivos em Excel que contêm informações das seguintes categorias:

- Indicadores de Varejo
- PMC Ampliado
- Automóveis
- Materiais de Construção

Cada função dentro do módulo `IBGEScraper` é dedicada a baixar um conjunto específico de dados. A estrutura principal do módulo é:
- `download_indicadores_varejo()`: Baixa os indicadores específicos do varejo.
- `pmc_ampliado()`: Baixa os dados do PMC ampliado.
- `automoveis()`: Baixa os dados referentes a automóveis.
- `materiais_construcao()`: Baixa os dados sobre materiais de construção.

#### Detalhes Técnicos

Cada função de download:
- Acessa a página de dados correspondente no site do IBGE.
- Seleciona as categorias e meses desejados, automatizando essa navegação.
- Inicia o download e salva o arquivo Excel na pasta `data` para processamento posterior.

### 2. `DataProcessor` - Processamento de Dados

Este módulo é responsável pela limpeza, transformação e cálculo de métricas relevantes dos dados baixados. Ele usa **Pandas** para manipulação e processamento dos dados.

#### Principais Funções

- `clean_data()`: Limpa e organiza os dados de cada conjunto para análise.
- `calculate_metrics(df)`: Calcula variações percentuais mensais para as diferentes categorias de comércio.
- `generate_plots(df)`: Gera gráficos para visualização das métricas e salva na pasta `images`.

#### Fluxo de Processamento

1. **Limpeza dos dados**: Os dados de cada categoria são carregados, tratados para eliminar valores nulos e organizados no formato apropriado para análise.
2. **Cálculo de Métricas**: As métricas mensais são calculadas, incluindo variações percentuais para as últimas observações de cada categoria.
3. **Geração de Gráficos**: Gera gráficos das métricas calculadas, exportando-os como imagens.

### 3. `ReportGenerator` - Geração de Relatório

Este módulo usa **ReportLab** para criar um relatório em PDF. Ele organiza as imagens dos gráficos e tabelas em um documento final com layout estruturado.

#### Estrutura do PDF

- As imagens dos gráficos e métricas geradas são inseridas página por página no relatório.
- Cada imagem é centralizada e dimensionada para caber nas páginas do relatório.
- O relatório final é salvo na pasta `reports` com o nome `relatorio_final.pdf`.

### 4. `main.py` - Script Principal

O script `main.py` orquestra o processo de coleta, processamento e geração do relatório final. Ele executa as seguintes etapas sequenciais:

1. Instancia as classes `IBGEScraper`, `DataProcessor` e `ReportGenerator`.
2. Realiza o download dos dados necessários do site do IBGE.
3. Processa os dados baixados, limpando-os e calculando as métricas desejadas.
4. Gera gráficos com base nos dados processados.
5. Compõe o relatório final em PDF, incluindo gráficos e tabelas.

### Exemplo de Uso

Para executar o pipeline completo e gerar o relatório, basta rodar o script `main.py` na linha de comando:
```bash
cd src
python3 main.py
```

O relatório gerado estará disponível em `reports/relatorio_final.pdf`.

## Dependências

O projeto utiliza as seguintes bibliotecas:

- **Playwright**: Para automação da navegação e download de arquivos no site do IBGE.
- **Pandas**: Para manipulação e limpeza de dados.
- **ReportLab**: Para geração de relatórios em PDF.
- **PIL (Pillow)**: Para manipulação e dimensionamento de imagens antes da inserção no relatório PDF.
- **Seaborn** e **Matplotlib**: Para geração de gráficos a partir dos dados processados.

Para instalar as dependências, execute:
```bash
pip install playwright pandas reportlab pillow matplotlib seaborn
playwright install
```

## Considerações Finais

Este projeto visa a **automação total** da geração de relatórios com dados da PMC, garantindo replicabilidade e facilidade de uso. Basta executar o script principal (`main.py`) para que todos os passos do pipeline sejam completados, desde a coleta dos dados até a geração do relatório em PDF.