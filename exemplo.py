import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Impacto da IA na Educação",
    layout="wide"
)


@st.cache_data
def carregar_dados(caminho_csv):

    df = pd.read_csv(caminho_csv)

    df = df.drop_duplicates()

    df = df.fillna(df.median(numeric_only=True))

    df["Variacao_Nota"] = (
        df["Post_Semester_GPA"] -
        df["Pre_Semester_GPA"]
    )

    media_horas = df["Weekly_GenAI_Hours"].mean()

    df["Perfil_Utilizador"] = np.where(
        df["Weekly_GenAI_Hours"] > media_horas,
        "Usuário Intensivo",
        "Usuário Moderado"
    )


    # Traduções
    traducao_cursos = {
        "Humanities": "Humanas",
        "Medical": "Medicina",
        "Engineering": "Engenharia",
        "Business": "Administração",
        "Computer Science": "Ciência da Computação",
        "Natural Sciences": "Ciências Naturais"
    }

    traducao_uso = {
        "Summarizing_Reading": "Resumo de Leituras",
        "Ideation": "Geração de Ideias",
        "Copywriting/Drafting": "Produção de Textos",
        "Debugging/Troubleshooting": "Correção de Código",
        "Direct_Answer_Generation": "Geração de Respostas"
    }

    traducao_politica = {
        "Strict_Ban": "Proibição Total",
        "Allowed_With_Citation": "Permitido com Citação",
        "Actively_Encouraged": "Incentivado"
    }

    traducao_burnout = {
        "Low": "Baixo",
        "Medium": "Médio",
        "High": "Alto"
    }

    df["Major_Category"] = df["Major_Category"].replace(
        traducao_cursos
    )

    df["Primary_Use_Case"] = df["Primary_Use_Case"].replace(
        traducao_uso
    )

    df["Institutional_Policy"] = df["Institutional_Policy"].replace(
        traducao_politica
    )

    df["Burnout_Risk_Level"] = df["Burnout_Risk_Level"].replace(
        traducao_burnout
    )

    return df


df = carregar_dados("ai_student_impact_dataset.csv")


# CABEÇALHO
st.title("O Impacto da Inteligência Artificial Generativa na Vida Acadêmica")

st.markdown("""
### Problema de Pesquisa

**Qual é o verdadeiro impacto do uso de Inteligência Artificial Generativa
no desempenho acadêmico e na saúde mental dos estudantes universitários?**

Para responder essa questão, foram analisados dados sobre desempenho acadêmico,
hábitos de estudo, dependência da IA, ansiedade e risco de burnout.
""")


# FILTROS
st.sidebar.header("Filtros")

cursos_selecionados = st.sidebar.multiselect(
    "Selecione as Áreas de Estudo",
    options=sorted(df["Major_Category"].unique()),
    default=sorted(df["Major_Category"].unique())
)

df_filtrado = df[
    df["Major_Category"].isin(cursos_selecionados)
]


# INDICADORES
st.subheader("Panorama Geral")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total de Alunos",
    f"{len(df_filtrado):,}"
)

col2.metric(
    "Média Horas IA/Semana",
    f"{df_filtrado['Weekly_GenAI_Hours'].mean():.2f}h"
)

col3.metric(
    "Horas de Estudo Tradicional",
    f"{df_filtrado['Traditional_Study_Hours'].mean():.2f}h"
)

col4.metric(
    "Variação Média da Nota",
    f"{df_filtrado['Variacao_Nota'].mean():+.3f}"
)

st.markdown("---")


# ABAS
aba1, aba2 = st.tabs([
    "Impacto Acadêmico",
    "Saúde Mental"
])


# ABA 1
with aba1:

    col_g1, col_g2 = st.columns(2)

    
    with col_g1:

        st.subheader("Uso de IA x Desempenho Acadêmico")

        st.markdown("""
        **Alunos que utilizam mais IA realmente melhoram suas notas ou apenas desenvolvem maior dependência da ferramenta?**
        """)

        fig, ax = plt.subplots(figsize=(6, 4))

        scatter = ax.scatter(
            df_filtrado["Weekly_GenAI_Hours"],
            df_filtrado["Variacao_Nota"],
            c=df_filtrado["Perceived_AI_Dependency"],
            cmap="viridis",
            alpha=0.5
        )

        ax.axhline(
            0,
            color="red",
            linestyle="--"
        )

        ax.set_xlabel(
            "Horas Semanais de Uso de IA"
        )

        ax.set_ylabel(
            "Variação da Nota"
        )

        fig.colorbar(
            scatter,
            ax=ax,
            label="Dependência Percebida"
        )

        st.pyplot(fig)

        correlacao_nota = (
            df_filtrado["Weekly_GenAI_Hours"]
            .corr(df_filtrado["Variacao_Nota"])
        )

        correlacao_dependencia = (
            df_filtrado["Weekly_GenAI_Hours"]
            .corr(df_filtrado["Perceived_AI_Dependency"])
        )


        st.markdown(f"""
### Análise

A correlação entre horas de uso da IA e variação das notas foi de
**{correlacao_nota:.2f}**, indicando uma relação fraca entre essas variáveis.

Já a correlação entre horas de uso e dependência percebida foi de
**{correlacao_dependencia:.2f}**, indicando uma associação muito mais forte.
""")

        st.success("""
Conclusão: O uso intensivo de IA não apresentou relação significativa
com melhora das notas, mas demonstrou associação com maior dependência
da ferramenta.
""")

    

    with col_g2:

        st.subheader("Variação da Nota por Tipo de Uso")
        st.markdown("""
        **Quais formas de utilização da IA geram os melhores resultados acadêmicos?**
        """)

        fig, ax = plt.subplots(figsize=(6, 4))

        df_agrupado_uso = (
            df_filtrado
            .groupby("Primary_Use_Case")["Variacao_Nota"]
            .mean()
            .sort_values()
        )

        df_agrupado_uso.plot(
            kind="barh",
            ax=ax
        )

        ax.axvline(
            0,
            linestyle="--"
        )

        ax.set_xlabel(
            "Variação Média da Nota"
        )

        ax.set_ylabel(
            "Uso Principal da IA"
        )

        st.pyplot(fig)

        melhor_uso = df_agrupado_uso.idxmax()
        melhor_valor = df_agrupado_uso.max()


        st.markdown(f"""
### Análise

A estratégia que apresentou maior ganho médio de desempenho foi:

**{melhor_uso}**

com uma variação média de **{melhor_valor:.3f} pontos**.
""")

        st.success(f"""
Conclusão: O uso da IA para **{melhor_uso.lower()}**
foi o que apresentou melhor desempenho acadêmico médio.
""")


# ABA 2
with aba2:

    col_g3, col_g4 = st.columns(2)

    
    with col_g3:

        st.subheader("Ansiedade e Política Institucional")
        st.markdown("""
        **Como as políticas institucionais relacionadas ao uso da IA influenciam a ansiedade dos estudantes?**
        """)


        fig, ax = plt.subplots(figsize=(6, 4))

        df_politica = (
            df_filtrado
            .groupby("Institutional_Policy")[
                "Anxiety_Level_During_Exams"
            ]
            .mean()
            .sort_values()
        )

        df_politica.plot(
            kind="bar",
            ax=ax
        )

        ax.set_ylabel(
            "Ansiedade Média"
        )

        plt.xticks(rotation=20)

        st.pyplot(fig)

        maior_ansiedade = df_politica.idxmax()
        valor_ansiedade = df_politica.max()


        st.markdown(f"""
### Análise

A política que apresentou maior nível médio de ansiedade foi:

**{maior_ansiedade}**

com média de **{valor_ansiedade:.2f} pontos**.
""")

        st.success("""
Conclusão: Instituições com políticas mais restritivas
tendem a apresentar níveis mais elevados de ansiedade
entre os estudantes.
""")

    

    with col_g4:

        st.subheader("Risco de Burnout por Perfil")
        st.markdown("""
        **O uso intensivo de IA está associado a um maior risco de burnout?**
        """)

        fig, ax = plt.subplots(figsize=(6, 4))

        df_burnout = (
            pd.crosstab(
                df_filtrado["Perfil_Utilizador"],
                df_filtrado["Burnout_Risk_Level"],
                normalize="index"
            ) * 100
        )

        ordem = ["Baixo", "Médio", "Alto"]

        df_burnout = df_burnout[ordem]

        df_burnout.plot(
            kind="bar",
            stacked=True,
            ax=ax
        )

        ax.set_ylabel("Percentual (%)")

        plt.xticks(rotation=0)

        st.pyplot(fig)

        alto_intensivo = (
            df_burnout.loc["Usuário Intensivo", "Alto"]
            if "Usuário Intensivo" in df_burnout.index
            else 0
        )

        alto_moderado = (
            df_burnout.loc["Usuário Moderado", "Alto"]
            if "Usuário Moderado" in df_burnout.index
            else 0
        )

        st.markdown(f"""
### Análise

Alto risco de burnout:

- Usuários Intensivos: **{alto_intensivo:.1f}%**
- Usuários Moderados: **{alto_moderado:.1f}%**
""")

        st.success("""
Conclusão: Os usuários intensivos apresentam uma
proporção significativamente maior de estudantes
com alto risco de burnout.
""")


# CONCLUSÃO 
st.markdown("---")

st.header("Conclusão Geral")

st.markdown("""
### Resposta à Pergunta Principal

A Inteligência Artificial Generativa pode trazer benefícios acadêmicos quando utilizada como ferramenta de apoio ao aprendizado, especialmente em atividades de resolução de problemas e construção do conhecimento.

Entretanto, o aumento das horas de utilização não apresentou relação significativa com a melhoria das notas. Em contrapartida, observou-se associação entre uso intensivo e maior dependência da ferramenta.

Os resultados também indicam que políticas institucionais excessivamente restritivas podem estar associadas a maiores níveis de ansiedade, enquanto usuários intensivos apresentaram maior incidência de risco elevado de burnout.

Portanto, os dados sugerem que o uso equilibrado e orientado da IA tende a produzir melhores resultados acadêmicos e psicológicos do que seu uso excessivo ou sua proibição total.
""")