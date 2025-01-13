import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def save_indicadores_varejo_cleaned_as_excel(excel_data, output_path):
    """
    Process and clean retail indicator data, and save the cleaned dataset as an Excel file.

    Parameters:
    - excel_data (str): Path to the Excel file containing raw retail indicators.
    - output_path (str): Path where the cleaned Excel file will be saved.

    Returns:
    - None: Saves the cleaned data directly to the specified output path.
    """
    df = pd.read_excel(excel_data, sheet_name='Tabela', header=4)
    df = df.dropna(axis=1, how='all')
    df = df.rename(columns={"Unnamed: 1": "Atividades"})
    df = df.loc[:, ~df.columns.str.contains("NaN|Variável|Tabela|Brasil", case=False, na=False)]
    df = df.dropna(subset=["Atividades"]).reset_index(drop=True)
    
    dates = pd.date_range(start="2000-01", periods=len(df.columns) - 1, freq='M')
    df_long = df.melt(id_vars=["Atividades"], var_name="Data", value_name="Receita")
    df_long["Data"] = pd.Series([dates[i] for i in range(len(dates))]).repeat(len(df.index)).reset_index(drop=True)
    df_long["Data"] = df_long["Data"].dt.strftime('%Y-%m')
    
    df_long["Receita"] = pd.to_numeric(df_long["Receita"], errors='coerce')
    df_cleaned_final = df_long.dropna(subset=["Receita"]).reset_index(drop=True)
    
    df_cleaned_final.to_excel(output_path, index=False)

def indicadores_varejo_cleaned(excel_data):
    """
    Load and process retail indicators data, returning a DataFrame with cleaned columns.

    Parameters:
    - excel_data (str): Path to the Excel file containing cleaned retail indicators.

    Returns:
    - pd.DataFrame: A pivoted DataFrame with 'DateTime' and various activity columns.
    """
    df = pd.read_excel(excel_data)
    df = save_indicadores_varejo_cleaned_as_excel(excel_data, '../data/indicadores_varejo_cleaned.xlsx')
    df = pd.read_excel('../data/indicadores_varejo_cleaned.xlsx')
    df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m')
    df.rename(columns={'Data': 'DateTime'}, inplace=True)
    df_pivot = df.pivot(index='DateTime', columns='Atividades', values='Receita').reset_index()

    return df_pivot

def pmc_ampliado_cleaned(excel_data):
    """
    Clean and return the 'PMC Ampliado' data for further analysis.

    Parameters:
    - excel_data (str): Path to the raw Excel file for PMC data.

    Returns:
    - pd.DataFrame: A DataFrame with 'DateTime' and 'PMC Ampliado' columns.
    """
    df = pd.read_excel(excel_data, sheet_name='Tabela', header=None)
    brasil_row_idx = df[df.apply(lambda row: row.astype(str).str.contains("Brasil").any(), axis=1)].index[0]
    df_numeric = df.iloc[brasil_row_idx, 1:].to_frame().reset_index(drop=True).transpose()
    dates = pd.date_range(start="2003-01", periods=df_numeric.shape[1], freq='M').strftime('%Y-%m')
    pmc_df = pd.DataFrame({"DateTime": dates, "PMC Ampliado": df_numeric.iloc[0].values})
    pmc_df["PMC Ampliado"] = pd.to_numeric(pmc_df["PMC Ampliado"], errors='coerce')

    return pmc_df

def automoveis_cleaned(excel_data):
    """
    Process and clean automotive data for analysis.

    Parameters:
    - excel_data (str): Path to the Excel file with automotive data.

    Returns:
    - pd.DataFrame: A DataFrame with 'DateTime' and 'Automoveis' columns.
    """
    df = pd.read_excel(excel_data, sheet_name='Tabela', header=None)
    brasil_row_idx = df[df.apply(lambda row: row.astype(str).str.contains("Brasil").any(), axis=1)].index[0]
    df_numeric = df.iloc[brasil_row_idx, 1:].to_frame().reset_index(drop=True).transpose()
    dates = pd.date_range(start="2000-01", periods=df_numeric.shape[1], freq='M').strftime('%Y-%m')
    automoveis_df = pd.DataFrame({"DateTime": dates, "Automoveis": df_numeric.iloc[0].values})
    automoveis_df["Automoveis"] = pd.to_numeric(automoveis_df["Automoveis"], errors='coerce')

    return automoveis_df

def materiais_construcao_cleaned(excel_data):
    """
    Clean and return construction materials data.

    Parameters:
    - excel_data (str): Path to the Excel file with raw construction materials data.

    Returns:
    - pd.DataFrame: A DataFrame with 'DateTime' and 'Materiais Construção' columns.
    """
    df = pd.read_excel(excel_data, sheet_name='Tabela', header=None)
    brasil_row_idx = df[df.apply(lambda row: row.astype(str).str.contains("Brasil").any(), axis=1)].index[0]
    df_numeric = df.iloc[brasil_row_idx, 1:].to_frame().reset_index(drop=True).transpose()
    dates = pd.date_range(start="2003-01", periods=df_numeric.shape[1], freq='M').strftime('%Y-%m')
    materiais_df = pd.DataFrame({"DateTime": dates, "Materiais Construção": df_numeric.iloc[0].values})
    materiais_df["Materiais Construção"] = pd.to_numeric(materiais_df["Materiais Construção"], errors='coerce')

    return materiais_df

def plot_unique_data(df, variable_name, save_path='../images/'):
    """
    Plot time series data for a single variable and save the image.

    Parameters:
    - df (pd.DataFrame): Data containing the 'DateTime' and variable column.
    - variable_name (str): The column name of the variable to plot.
    - save_path (str): Path to save the plot image.

    Returns:
    - matplotlib.figure.Figure: The generated plot figure.
    """
    os.makedirs(save_path, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df, x='DateTime', y=variable_name, ax=ax, label=variable_name)
    ax.set_title(f'{variable_name} ao longo do tempo')
    ax.set_xlabel('Data')
    ax.set_ylabel('Valor')
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig.savefig(os.path.join(save_path, f'{variable_name}.png'))
    plt.show()

    return fig

def plot_multiple_data(df, variables, save_path='../images/'):
    """
    Plot multiple time series on the same plot and save the image.

    Parameters:
    - df (pd.DataFrame): DataFrame with 'DateTime' and multiple variable columns.
    - variables (list of str): List of column names to plot.
    - save_path (str): Path to save the plot image.

    Returns:
    - matplotlib.figure.Figure: The generated plot figure.
    """
    os.makedirs(save_path, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = sns.color_palette("tab10", n_colors=len(variables))
    for i, variable in enumerate(variables):
        sns.lineplot(data=df, x='DateTime', y=variable, ax=ax, label=variable, color=colors[i])
    ax.set_title('Atividades ao longo do tempo')
    ax.set_xlabel('Data')
    ax.set_ylabel('Valor')
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig.savefig(os.path.join(save_path, 'all_variables.png'))
    plt.show()

    return fig

class DataProcessor:
    """
    Data processing and plotting class for economic indicators.
    """
    def __init__(self):
        pass

    def clean_data(self):
        """
        Load and clean datasets for various economic indicators, merging them by date.

        Returns:
        - pd.DataFrame: DataFrame containing merged cleaned data for all indicators.
        """
        indicadores_varejo = '../data/indicadores_varejo.xlsx'
        pmc_ampliado = '../data/pmc_ampliado.xlsx'
        automoveis = '../data/automoveis.xlsx'
        materiais_construcao = '../data/materiais_construcao.xlsx'

        df_indicadores_varejo = indicadores_varejo_cleaned(indicadores_varejo)
        df_pmc_ampliado = pmc_ampliado_cleaned(pmc_ampliado)
        df_automoveis = automoveis_cleaned(automoveis)
        df_materiais_construcao = materiais_construcao_cleaned(materiais_construcao)

        # Ensure consistent DateTime format across DataFrames
        df_pmc_ampliado['DateTime'] = pd.to_datetime(df_pmc_ampliado['DateTime'])
        df_indicadores_varejo['DateTime'] = pd.to_datetime(df_indicadores_varejo['DateTime'])
        df_automoveis['DateTime'] = pd.to_datetime(df_automoveis['DateTime'])
        df_materiais_construcao['DateTime'] = pd.to_datetime(df_materiais_construcao['DateTime'])

        # Merge DataFrames
        df_automoveis_materiais = pd.merge(df_automoveis, df_materiais_construcao, on='DateTime', how='inner')
        df_pmc_ampliado_varejo = pd.merge(df_pmc_ampliado, df_indicadores_varejo, on='DateTime', how='inner')
        df = pd.merge(df_automoveis_materiais, df_pmc_ampliado_varejo, on='DateTime', how='inner')

        return df
        
    def calculate_metrics(self, df, save_path='../images/'):
        """
        Calculate month-to-month percentage variations for each activity in the DataFrame.

        Parameters:
        - df (pd.DataFrame): Data containing 'DateTime' and other activity columns.
        - save_path (str): Path to save the results image.

        Returns:
        - pd.DataFrame: DataFrame with month-to-month percentage variations for each activity.
        """
        if 'DateTime' not in df.columns:
            print("A coluna 'DateTime' não está presente no DataFrame.")
            return None

        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df = df.sort_values(by='DateTime', ascending=False).reset_index(drop=True)
        
        last_four_months_df = df.head(4)
        last_three_months_dates = last_four_months_df['DateTime'].dt.strftime('%Y-%m-%d').tolist()[:3]
        results = pd.DataFrame(columns=['Atividade', 'Peso'] + last_three_months_dates)

        for col in df.columns:
            if col in ['DateTime', 'Peso']:
                continue
            
            values = last_four_months_df[col].values
            weight = df.loc[df[col].notna(), 'Peso'].iloc[0] if 'Peso' in df.columns else None
            monthly_variations = []
            for i in range(1, len(values)):
                initial_value = values[i]
                final_value = values[i - 1]
                if pd.notna(initial_value) and initial_value != 0:
                    variation_percent = ((final_value - initial_value) / abs(initial_value)) * 100
                else:
                    variation_percent = None
                monthly_variations.append(variation_percent)

            row_data = [col, weight] + monthly_variations[-3:]
            results = pd.concat([results, pd.DataFrame([row_data], columns=results.columns)], ignore_index=True)

        os.makedirs(save_path, exist_ok=True)
        fig, ax = plt.subplots(figsize=(10, len(results) * 0.5))
        ax.axis('off')
        table = ax.table(cellText=results.values, colLabels=results.columns, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)
        plt.tight_layout()
        fig.savefig(os.path.join(save_path, '2.png'))

        return results

    def generate_plots(self, df):
        """
        Generate and save time series plots for various economic indicators.

        Parameters:
        - df (pd.DataFrame): DataFrame with cleaned data for each indicator.
        
        Returns:
        - None: Saves plots as images.
        """
        save_path = '../images/'
        plot_pmc = plot_unique_data(df, 'PMC Ampliado', save_path)
        plot_automoveis = plot_unique_data(df, 'Automoveis', save_path)
        plot_materiais = plot_unique_data(df, 'Materiais Construção', save_path)
        plot_medicos = plot_unique_data(df, 'Artigos farmacêuticos, médicos, ortopédicos, de perfumaria e cosméticos', save_path)
        plot_combustiveis = plot_unique_data(df, 'Combustíveis e lubrificantes', save_path)
        plot_hiper_supermercado = plot_unique_data(df, 'Hipermercados e supermercados', save_path)
        plot_livros_papelaria = plot_unique_data(df, 'Livros, jornais, revistas e papelaria', save_path)
        plot_moveis_decoracao = plot_unique_data(df, 'Móveis e eletrodomésticos', save_path)
        plot_vestuario_calcados = plot_unique_data(df, 'Tecidos, vestuário e calçados', save_path)

        plot_all_variables = plot_multiple_data(df, [
            'PMC Ampliado', 'Automoveis', 'Materiais Construção', 
            'Artigos farmacêuticos, médicos, ortopédicos, de perfumaria e cosméticos', 
            'Combustíveis e lubrificantes', 'Hipermercados e supermercados', 
            'Livros, jornais, revistas e papelaria', 'Móveis e eletrodomésticos', 
            'Tecidos, vestuário e calçados'
        ], save_path)