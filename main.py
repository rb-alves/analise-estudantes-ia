import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Impacto da IA na educação", layout="wide")

# Carrega dados
@st.cache_data
def carregar_dados(caminho_csv):
    df = pd.read_csv(caminho_csv)

    print(df.info())

    df = df.drop_duplicates()

    df = df.fillna(df.median(numeric_only=True))

    df["Variacao_Nota"] = df["Post_Semester_GPA"] - df["Pre_Semester_GPA"]

    media_horas = df["Weekly_GenAI_Hours"].mean()

    df['Perfil_Utilizador'] = np.where(df['Weekly_GenAI_Hours'] > media_horas, 'Utilizador Intensivo', 'Utilizador Regular')

    return df

df = carregar_dados("ai_student_impact_dataset.csv")

# Cabecalho
st.title("O Impacto da IA Generativa na Vida Académica")
st.markdown("""
### **Definição do Problema**
Este projeto analisa como o uso de ferramentas de Inteligência Artificial Generativa afeta o desempenho académico (notas), 
o nível de ansiedade e o risco de esgotamento mental (Burnout) dos estudantes universitários de diferentes áreas de conhecimento.
""")

# Sidebar e Filtros
st.sidebar.header("Filtros")

cursos_selecionados = st.sidebar.multiselect(
    "Selecione as Áreas de Estudo:",
    options=df['Major_Category'].unique().tolist(),
    default=df['Major_Category'].unique().tolist()
)

df_filtrado = df[df["Major_Category"].isin(cursos_selecionados)]


# dados gerais
st.subheader("Panorama Geral dos Estudantes Selecionados")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Alunos Analisados", f"{len(df_filtrado):,}")
col2.metric("Média de Horas IA/Semana", f"{df_filtrado['Weekly_GenAI_Hours'].mean():.2f}h")
col3.metric("Horas de Estudo Tradicional", f"{df_filtrado['Traditional_Study_Hours'].mean():.2f}h")
col4.metric("Variação Média da Nota", f"{df_filtrado['Variacao_Nota'].mean():+.3f}")

st.markdown("---")

st.subheader("Análise e Visualizações")
aba1, aba2 = st.tabs(["Impacto Académico", "Saúde Mental e Comportamento"])

with aba1:
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.write("#### Uso de IA vs. Desempenho (Variação da Nota)")
        fig, ax = plt.subplots(figsize=(6, 4))
        scatter = ax.scatter(
            df_filtrado['Weekly_GenAI_Hours'], 
            df_filtrado['Variacao_Nota'], 
            alpha=0.5, 
            c=df_filtrado['Perceived_AI_Dependency'], 
            cmap='viridis'
        )
        ax.set_xlabel("Horas Semanais de IA Generativa")
        ax.set_ylabel("Variação da Nota (Pós - Pré Semestre)")
        ax.axhline(0, color='red', linestyle='--', alpha=0.5)
        fig.colorbar(scatter, ax=ax, label="Dependência Percecionada de IA")
        st.pyplot(fig)
        st.caption("Cada ponto representa um aluno. Avalie se o uso excessivo de IA (pontos mais à direita) se traduz em notas maiores (acima da linha vermelha) ou apenas em maior dependência (cores mais claras).")

    with col_g2:
        st.write("#### Variação de Nota por Caso de Uso Principal")
        fig, ax = plt.subplots(figsize=(6, 4))
        df_agrupado_uso = df_filtrado.groupby('Primary_Use_Case')['Variacao_Nota'].mean().sort_values()
        df_agrupado_uso.plot(kind='barh', ax=ax, color='skyblue')
        ax.set_xlabel("Variação Média da Nota")
        ax.set_ylabel("Caso de Uso Principal")
        ax.axvline(0, color='gray', linestyle='--')
        st.pyplot(fig)
        st.caption("Compara o ganho médio de nota entre diferentes usos da IA. Barras mais longas à direita indicam as estratégias de estudo com IA que trazem melhores resultados.")

with aba2:
    col_g3, col_g4 = st.columns(2)
    
    with col_g3:
        st.write("#### Nível de Ansiedade vs. Política Institucional")
        fig, ax = plt.subplots(figsize=(6, 4))
        df_politica = df_filtrado.groupby('Institutional_Policy')['Anxiety_Level_During_Exams'].mean().sort_values()
        df_politica.plot(kind='bar', ax=ax, color='salmon')
        ax.set_ylabel("Média do Nível de Ansiedade nos Exames")
        ax.set_xlabel("Política da Instituição face à IA")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
        st.caption("Mostra a média de ansiedade dos alunos agrupada pelas regras da universidade. Barras mais altas indicam ambientes de avaliação mais estressantes.")

    with col_g4:
        st.write("#### Distribuição do Risco de Burnout por Perfil de Utilizador")
        fig, ax = plt.subplots(figsize=(6, 4))
        df_burnout = pd.crosstab(df_filtrado['Perfil_Utilizador'], df_filtrado['Burnout_Risk_Level'], normalize='index') * 100
        df_burnout = df_burnout[['Low', 'Medium', 'High']]
        df_burnout.plot(kind='bar', stacked=True, ax=ax, color=['#A2E8DD', '#FBC15E', '#FA6E59'])
        ax.set_ylabel("Percentagem (%)")
        ax.set_xlabel("Perfil de Utilizador de IA")
        plt.xticks(rotation=0)
        ax.legend(title="Risco de Burnout")
        st.pyplot(fig)
        st.caption("Compara a proporção do risco de Burnout (Baixo, Médio, Alto) entre os alunos. Observe se a faixa vermelha (Risco Alto) é maior em algum perfil de uso.")

st.markdown("---")

# --- CONCLUSÃO ---
st.subheader("Conclusão e Resumo Executivo")
st.markdown("""
Com base nos dados analisados, podemos inferir que:
1. **Desempenho Académico**: Os alunos que utilizam a IA de forma direcionada tendem a apresentar evolução positiva nas notas. No entanto, os **Utilizadores Intensivos** podem acabar por associar o excesso de horas a uma maior dependência, estagnando o crescimento da nota.
2. **Saúde Mental**: Políticas universitárias severas de proibição mostram uma forte correlação com níveis elevados de ansiedade nos exames, possivelmente devido ao medo de punições.
3. **Recomendação Final**: Sugere-se que as instituições adotem posturas de orientação e permissão ética (com citação), ajudando os estudantes a utilizarem estas ferramentas como complemento ao estudo tradicional, mitigando assim o risco de esgotamento mental (*Burnout*).
""")