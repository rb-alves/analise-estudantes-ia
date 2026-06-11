import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

st.set_page_config(page_title="Impacto da IA na Educação", layout="wide")

# ── Estilos globais ──────────────────────────────────────────────────────────
st.markdown("""
<style>
.pergunta-box {
    background-color: #EFF6FF;
    border-left: 4px solid #3B82F6;
    padding: 10px 14px;
    border-radius: 0 6px 6px 0;
    margin-bottom: 12px;
    font-size: 0.9rem;
    color: #1E40AF;
}
.resposta-box {
    background-color: #F0FDF4;
    border-left: 4px solid #22C55E;
    padding: 10px 14px;
    border-radius: 0 6px 6px 0;
    margin-bottom: 16px;
    font-size: 0.85rem;
    color: #166534;
}
.titulo-grafico {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 4px;
}
.legenda-scatter {
    background-color: #FFFBEB;
    border: 1px solid #FCD34D;
    border-radius: 6px;
    padding: 10px 14px;
    font-size: 0.82rem;
    color: #92400E;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)


# ── Carregamento de dados ────────────────────────────────────────────────────
@st.cache_data
def carregar_dados(caminho_csv):
    df = pd.read_csv(caminho_csv)
    df = df.drop_duplicates()
    df = df.fillna(df.median(numeric_only=True))
    df["Variacao_Nota"] = df["Post_Semester_GPA"] - df["Pre_Semester_GPA"]
    media_horas = df["Weekly_GenAI_Hours"].mean()
    df["Perfil_Utilizador"] = np.where(
        df["Weekly_GenAI_Hours"] > media_horas,
        "Utilizador Intensivo",
        "Utilizador Regular",
    )
    return df


df = carregar_dados("ai_student_impact_dataset.csv")


# ── Cabeçalho ────────────────────────────────────────────────────────────────
st.title("🎓 O Impacto da IA Generativa na Vida Académica")
st.markdown("""
### Definição do Problema
Este projeto analisa como o uso de ferramentas de **Inteligência Artificial Generativa** afeta
o desempenho académico (notas), o nível de ansiedade e o risco de esgotamento mental (*Burnout*)
dos estudantes universitários de diferentes áreas de conhecimento.

---
""")

st.markdown("""
<div style="background:#F8FAFC;border:1px solid #CBD5E1;border-radius:8px;padding:14px 18px;margin-bottom:1rem;">
<b>🎯 Pergunta Principal</b><br>
<span style="font-size:1rem;">
<em>"Qual é o verdadeiro impacto do uso de Inteligência Artificial Generativa
no desempenho académico e na saúde mental dos estudantes universitários?"</em>
</span>
</div>
""", unsafe_allow_html=True)


# ── Sidebar / Filtros ────────────────────────────────────────────────────────
st.sidebar.header("🔍 Filtros")
cursos_selecionados = st.sidebar.multiselect(
    "Selecione as Áreas de Estudo:",
    options=df["Major_Category"].unique().tolist(),
    default=df["Major_Category"].unique().tolist(),
)
df_filtrado = df[df["Major_Category"].isin(cursos_selecionados)]


# ── Métricas gerais ──────────────────────────────────────────────────────────
st.subheader("📊 Panorama Geral dos Estudantes Selecionados")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Alunos Analisados", f"{len(df_filtrado):,}")
col2.metric("Média de Horas IA/Semana", f"{df_filtrado['Weekly_GenAI_Hours'].mean():.2f}h")
col3.metric("Horas de Estudo Tradicional", f"{df_filtrado['Traditional_Study_Hours'].mean():.2f}h")
col4.metric("Variação Média da Nota", f"{df_filtrado['Variacao_Nota'].mean():+.3f}")

st.markdown("---")

# ════════════════════════════════════════════════════════════════════════════
# ABAS
# ════════════════════════════════════════════════════════════════════════════
st.subheader("📈 Análise e Visualizações")
aba1, aba2 = st.tabs(["📚 Impacto Académico", "🧠 Saúde Mental e Comportamento"])


# ────────────────────────────────────────────────────────────────────────────
# ABA 1 — IMPACTO ACADÉMICO
# ────────────────────────────────────────────────────────────────────────────
with aba1:

    # ── GRÁFICO 1 — Scatter ──────────────────────────────────────────────────
    st.markdown("### Gráfico 1 · Uso de IA vs. Desempenho Académico")

    st.markdown("""
    <div class="pergunta-box">
    ❓ <b>Pergunta:</b> Alunos que usam muita IA realmente melhoram suas notas ao longo
    do semestre, ou o uso excessivo apenas aumenta a <em>sensação de dependência</em> da ferramenta?
    </div>
    """, unsafe_allow_html=True)

    # ── Guia de leitura (expansível) ────────────────────────────────────────
    with st.expander("📖 Como ler este gráfico de dispersão? (clique para expandir)"):
        st.markdown("""
        Um **gráfico de dispersão** (scatter plot) coloca cada aluno como **um ponto** num plano com dois eixos:

        | Eixo | O que representa | Como interpretar |
        |------|-----------------|-----------------|
        | **Eixo X (horizontal)** | Horas semanais de uso de IA | Quanto mais à **direita**, mais horas de IA por semana |
        | **Eixo Y (vertical)** | Variação da nota (Pós − Pré semestre) | **Acima** da linha vermelha = nota **subiu**; **abaixo** = nota **desceu** |
        | **Cor do ponto** | Dependência percebida de IA (escala 1–10) | Cores **escuras** (roxo/azul) = baixa dependência; cores **claras** (amarelo) = alta dependência |

        **O que procurar:**
        - Se os pontos do lado direito (muitas horas de IA) estiverem maioritariamente **acima** da linha vermelha → uso intensivo melhora notas ✅
        - Se esses mesmos pontos tiverem cores **mais claras** → uso intensivo aumenta dependência, mesmo sem melhorar nota ⚠️
        - Se os pontos estiverem espalhados aleatoriamente → uso de IA tem pouco efeito direto na nota 🔍
        """)

    col_g1, col_g2_info = st.columns([2, 1])

    with col_g1:
        fig, ax = plt.subplots(figsize=(7, 4.5))
        scatter = ax.scatter(
            df_filtrado["Weekly_GenAI_Hours"],
            df_filtrado["Variacao_Nota"],
            alpha=0.45,
            c=df_filtrado["Perceived_AI_Dependency"],
            cmap="viridis",
            s=30,
            edgecolors="none",
        )
        ax.set_xlabel("Horas Semanais de IA Generativa", fontsize=10)
        ax.set_ylabel("Variação da Nota (Pós − Pré Semestre)", fontsize=10)
        ax.set_title("Uso de IA vs. Variação de Nota", fontsize=11, fontweight="bold")
        ax.axhline(0, color="red", linestyle="--", alpha=0.6, linewidth=1.2,
                   label="Sem variação de nota")
        ax.legend(fontsize=8, loc="upper right")
        cbar = fig.colorbar(scatter, ax=ax)
        cbar.set_label("Dependência de IA (1=baixa · 10=alta)", fontsize=8)
        ax.grid(True, alpha=0.2, linestyle=":")
        fig.tight_layout()
        st.pyplot(fig)

    with col_g2_info:
        st.markdown("**🔑 Legenda rápida**")
        st.markdown("""
        🟡 **Ponto amarelo/claro**  
        Alta dependência de IA

        🟣 **Ponto roxo/escuro**  
        Baixa dependência de IA

        📍 **Posição vertical**  
        Acima da linha → nota subiu  
        Abaixo → nota desceu

        📍 **Posição horizontal**  
        Mais à direita → mais horas de IA
        """)

        # Estatística de correlação
        corr_val = df_filtrado["Weekly_GenAI_Hours"].corr(df_filtrado["Variacao_Nota"])
        st.metric(
            "Correlação: horas IA × variação nota",
            f"{corr_val:.3f}",
            help="Próximo de 0 = relação fraca. Positivo = mais horas, nota maior.",
        )
        dep_corr = df_filtrado["Perceived_AI_Dependency"].corr(df_filtrado["Variacao_Nota"])
        st.metric(
            "Correlação: dependência × variação nota",
            f"{dep_corr:.3f}",
        )

    st.markdown("""
    <div class="resposta-box">
    💡 <b>Conclusão:</b> A correlação próxima de zero indica que mais horas de IA
    <b>não garante</b> melhoria de nota. Repara que pontos com muitas horas (direita) tendem a ter
    cores mais claras — confirmando que o uso intensivo eleva a <em>dependência percebida</em>
    sem elevar proporcionalmente o desempenho.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── GRÁFICO 2 — Caso de uso ──────────────────────────────────────────────
    st.markdown("### Gráfico 2 · Variação de Nota por Forma de Usar a IA")

    st.markdown("""
    <div class="pergunta-box">
    ❓ <b>Pergunta:</b> Quais formas de usar a IA (ex: fazer resumos, gerar ideias,
    corrigir códigos) trazem os <b>melhores resultados</b> para a nota do aluno?
    </div>
    """, unsafe_allow_html=True)

    col_g3, col_g4 = st.columns([2, 1])

    with col_g3:
        fig2, ax2 = plt.subplots(figsize=(7, 3.8))
        df_agrupado_uso = (
            df_filtrado.groupby("Primary_Use_Case")["Variacao_Nota"]
            .mean()
            .sort_values()
        )
        cores_barras = ["#EF4444" if v < 0 else "#3B82F6" for v in df_agrupado_uso.values]
        df_agrupado_uso.plot(kind="barh", ax=ax2, color=cores_barras, edgecolor="none")
        ax2.set_xlabel("Variação Média da Nota", fontsize=10)
        ax2.set_ylabel("Caso de Uso Principal", fontsize=10)
        ax2.set_title("Qual forma de usar a IA melhora mais as notas?", fontsize=11, fontweight="bold")
        ax2.axvline(0, color="gray", linestyle="--", alpha=0.6)
        ax2.grid(True, axis="x", alpha=0.2, linestyle=":")

        patch_pos = mpatches.Patch(color="#3B82F6", label="Ganho positivo de nota")
        patch_neg = mpatches.Patch(color="#EF4444", label="Perda de nota")
        ax2.legend(handles=[patch_pos, patch_neg], fontsize=8, loc="lower right")

        fig2.tight_layout()
        st.pyplot(fig2)

    with col_g4:
        st.markdown("**📊 Ranking dos usos**")
        ranking = df_filtrado.groupby("Primary_Use_Case")["Variacao_Nota"].mean().sort_values(ascending=False)
        for i, (uso, val) in enumerate(ranking.items()):
            emoji = "🥇" if i == 0 else ("🥈" if i == 1 else ("🥉" if i == 2 else "📌"))
            uso_limpo = uso.replace("_", " ")
            st.markdown(f"{emoji} **{uso_limpo}**  \n`{val:+.4f}`")

    st.markdown("""
    <div class="resposta-box">
    💡 <b>Conclusão:</b> <em>Debugging/Troubleshooting</em> e <em>Copywriting/Drafting</em>
    surgem com os melhores ganhos de nota — usos mais <b>ativos e orientados a tarefas</b>.
    Já a <em>Geração Direta de Respostas</em> apresenta o menor ganho, sugerindo que deixar
    a IA "pensar por si" não desenvolve competências avaliadas nos exames.
    </div>
    """, unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────────────────
# ABA 2 — SAÚDE MENTAL
# ────────────────────────────────────────────────────────────────────────────
with aba2:

    # ── GRÁFICO 3 — Ansiedade vs. Política ──────────────────────────────────
    st.markdown("### Gráfico 3 · Ansiedade nos Exames vs. Política Institucional")

    st.markdown("""
    <div class="pergunta-box">
    ❓ <b>Pergunta:</b> As políticas da universidade em relação à IA
    (como proibir totalmente ou permitir com citação) influenciam
    o nível de <b>ansiedade dos alunos</b> durante as semanas de provas?
    </div>
    """, unsafe_allow_html=True)

    col_g5, col_g6 = st.columns([2, 1])

    with col_g5:
        fig3, ax3 = plt.subplots(figsize=(7, 3.8))
        df_politica = (
            df_filtrado.groupby("Institutional_Policy")["Anxiety_Level_During_Exams"]
            .mean()
            .sort_values()
        )
        labels_pt = {
            "Actively_Encouraged": "Encorajada ativamente",
            "Allowed_With_Citation": "Permitida com citação",
            "Strict_Ban": "Proibição total",
        }
        df_politica.index = [labels_pt.get(x, x) for x in df_politica.index]
        palette = ["#22C55E", "#3B82F6", "#EF4444"][: len(df_politica)]
        bars = df_politica.plot(
            kind="bar", ax=ax3, color=palette[::-1], edgecolor="none", width=0.5
        )
        ax3.set_ylabel("Média do Nível de Ansiedade", fontsize=10)
        ax3.set_xlabel("Política da Instituição face à IA", fontsize=10)
        ax3.set_title("A política universitária afeta a ansiedade nos exames?", fontsize=11, fontweight="bold")
        ax3.set_ylim(0, df_politica.max() * 1.25)
        plt.xticks(rotation=20, ha="right")

        for rect, val in zip(ax3.patches, df_politica.values):
            ax3.text(
                rect.get_x() + rect.get_width() / 2,
                rect.get_height() + 0.05,
                f"{val:.2f}",
                ha="center", va="bottom", fontsize=9, fontweight="bold",
            )

        ax3.grid(True, axis="y", alpha=0.2, linestyle=":")
        fig3.tight_layout()
        st.pyplot(fig3)

    with col_g6:
        st.markdown("**📋 O que significa cada política?**")
        st.markdown("""
        🟢 **Encorajada ativamente**  
        A universidade promove o uso de IA nas tarefas.

        🔵 **Permitida com citação**  
        Pode usar, mas deve referenciar a ferramenta.

        🔴 **Proibição total**  
        Uso de IA é proibido e pode gerar punições.
        """)

        max_pol = df_filtrado.groupby("Institutional_Policy")["Anxiety_Level_During_Exams"].mean().idxmax()
        st.warning(f"⚠️ Maior ansiedade sob política: **{labels_pt.get(max_pol, max_pol)}**")

    st.markdown("""
    <div class="resposta-box">
    💡 <b>Conclusão:</b> Instituições com <em>Proibição Total</em> registam os maiores
    níveis de ansiedade — provavelmente pelo medo de punições. Políticas de
    permissão ética (com citação) ou encorajamento apresentam ambientes de
    avaliação significativamente menos stressantes.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── GRÁFICO 4 — Burnout por Perfil ──────────────────────────────────────
    st.markdown("### Gráfico 4 · Risco de Burnout por Perfil de Uso de IA")

    st.markdown("""
    <div class="pergunta-box">
    ❓ <b>Pergunta:</b> Os <em>Utilizadores Intensivos</em> (muitas horas de IA)
    correm um risco <b>maior de esgotamento mental (Burnout)</b> comparado
    com os que fazem uso moderado/regular?
    </div>
    """, unsafe_allow_html=True)

    col_g7, col_g8 = st.columns([2, 1])

    with col_g7:
        fig4, ax4 = plt.subplots(figsize=(7, 4))
        df_burnout = (
            pd.crosstab(
                df_filtrado["Perfil_Utilizador"],
                df_filtrado["Burnout_Risk_Level"],
                normalize="index",
            )
            * 100
        )
        df_burnout = df_burnout[["Low", "Medium", "High"]]
        cores_burnout = ["#22C55E", "#F59E0B", "#EF4444"]
        df_burnout.plot(
            kind="bar", stacked=True, ax=ax4,
            color=cores_burnout, edgecolor="white", linewidth=0.5,
        )
        ax4.set_ylabel("Percentagem (%)", fontsize=10)
        ax4.set_xlabel("Perfil de Utilizador de IA", fontsize=10)
        ax4.set_title("Utilizadores Intensivos têm mais Burnout?", fontsize=11, fontweight="bold")
        plt.xticks(rotation=0)
        ax4.set_ylim(0, 115)

        # Anotações de percentagem nas barras
        for bar_group in ax4.containers:
            for rect in bar_group:
                h = rect.get_height()
                if h > 4:
                    ax4.text(
                        rect.get_x() + rect.get_width() / 2,
                        rect.get_y() + h / 2,
                        f"{h:.0f}%",
                        ha="center", va="center",
                        fontsize=8, fontweight="bold", color="white",
                    )

        ax4.legend(
            title="Risco de Burnout",
            labels=["Baixo ✅", "Médio ⚠️", "Alto 🔴"],
            loc="upper right",
            fontsize=8,
        )
        ax4.grid(True, axis="y", alpha=0.15, linestyle=":")
        fig4.tight_layout()
        st.pyplot(fig4)

    with col_g8:
        st.markdown("**📊 Comparação directa**")

        if "Intensivo" in df_filtrado["Perfil_Utilizador"].values:
            pct_high_int = (
                df_burnout.loc["Utilizador Intensivo", "High"]
                if "Utilizador Intensivo" in df_burnout.index else 0
            )
            pct_high_reg = (
                df_burnout.loc["Utilizador Regular", "High"]
                if "Utilizador Regular" in df_burnout.index else 0
            )
            st.metric("Burnout Alto — Intensivo", f"{pct_high_int:.1f}%")
            st.metric("Burnout Alto — Regular", f"{pct_high_reg:.1f}%",
                      delta=f"{pct_high_reg - pct_high_int:.1f}pp vs. intensivo")

        st.markdown("""
        **O que é Burnout?**  
        É um estado de esgotamento físico e mental causado por stress crónico. No contexto académico manifesta-se como exaustão, falta de motivação e queda no desempenho.
        """)

    st.markdown("""
    <div class="resposta-box">
    💡 <b>Conclusão:</b> Os <em>Utilizadores Intensivos</em> têm uma proporção de Burnout Alto
    substancialmente maior. Usar IA em excesso parece <b>não substituir o esforço cognitivo</b>,
    mas adiciona sobrecarga — mais horas de ecrã, mais decisões, mais pressão para gerir
    os outputs da ferramenta.
    </div>
    """, unsafe_allow_html=True)


# ── Conclusão ────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("📝 Conclusão e Resumo Executivo")
st.markdown("""
Com base nos dados analisados, podemos inferir que:

1. **Desempenho Académico**: A quantidade de horas de IA por si só tem correlação quase nula com a melhoria de notas. O que importa é *como* a IA é usada — usos activos como *debugging* e *escrita assistida* geram melhores resultados do que a geração directa de respostas.

2. **Dependência**: Utilizadores Intensivos acumulam maior dependência percebida sem ganho proporcional de nota — um sinal de alerta para estudantes e educadores.

3. **Saúde Mental**: Políticas de proibição total correlacionam-se com níveis de ansiedade mais elevados. A permissão ética (com citação) é a abordagem que equilibra melhor autonomia e bem-estar.

4. **Recomendação Final**: Instituições devem adotar posturas de orientação e permissão ética, ajudando os estudantes a usarem estas ferramentas como *complemento* ao estudo tradicional — mitigando assim o risco de esgotamento mental (*Burnout*).
""")