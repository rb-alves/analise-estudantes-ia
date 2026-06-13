# Impacto da IA Generativa na Vida Académica 🎓🤖

Este projeto consiste num dashboard interativo desenvolvido em **Streamlit** para analisar o impacto real do uso de Inteligência Artificial Generativa no desempenho académico e na saúde mental de estudantes universitários. 

O projeto foi construído utilizando o ecossistema fundamental de Ciência de Dados em Python (**Pandas, Numpy e Matplotlib**), cobrindo todo o ciclo de dados: desde o carregamento e tratamento até à geração de relatórios e insights visuais.

---

## 📌 Problema de Pesquisa

> **Pergunta Central:** Qual é o verdadeiro impacto do uso de Inteligência Artificial Generativa no desempenho académico e na saúde mental dos estudantes universitários?

A aplicação procura perceber se uma maior quantidade de horas dedicadas às ferramentas de IA se traduz em notas melhores ou se apenas gera dependência tecnológica, além de mapear os efeitos colaterais psicológicos (ansiedade e burnout) decorrentes das políticas institucionais e do perfil de uso dos alunos.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **Streamlit**: Para a criação da interface web interativa.
* **Pandas**: Para manipulação, limpeza e tradução dos dados.
* **Numpy**: Para engenharia de recursos (feature engineering) e lógica condicional vetorizada.
* **Matplotlib**: Para a construção de visualizações customizadas (gráficos de dispersão, barras e barras empilhadas).

---

## 📊 O Dataset

O projeto utiliza obrigatoriamente o ficheiro de dados nomeado exatamente como `ai_student_impact_dataset.csv`. O conjunto de dados original (disponibilizado via Kaggle) contém informações volumosas sobre:
* Histórico académico (GPAs pré e pós-semestre).
* Hábitos de estudo (horas semanais de IA e horas de estudo tradicional).
* Fatores comportamentais e institucionais (política da faculdade, caso de uso principal e dependência percebida).
* Métricas de saúde mental (nível de ansiedade em exames e risco de burnout).

---

## ⚙️ Pipeline de Dados & Funcionalidades do Código

O ficheiro principal `main.py` executa as seguintes etapas automatizadas:

### 1. Tratamento e Preparação dos Dados
* **Otimização de Performance**: Utilização do decorador `@st.cache_data` para evitar recarregamentos dispendiosos do dataset a cada interação de filtro.
* **Limpeza**: Remoção automática de linhas duplicadas (`drop_duplicates`) e tratamento de valores nulos utilizando a **mediana** dos dados numéricos (`fillna`), garantindo resiliência contra *outliers*.
* **Engenharia de Recursos (Feature Engineering)**:
    * `Variacao_Nota`: Calculada pela diferença simples entre o GPA pós-semestre e o GPA pré-semestre para medir a evolução real do aluno.
    * `Perfil_Utilizador`: Classificação dinâmica usando `np.where` que divide os alunos entre *Utilizadores Intensivos* e *Utilizadores Moderados* com base na média global de horas de uso de IA.
* **Localização/Tradução**: Mapeamento e tradução completa dos termos categóricos em inglês (cursos, políticas e níveis de risco) para português, tornando o painel amigável para o utilizador final.

### 2. Interface do Utilizador (Streamlit)
* **Filtros Dinâmicos**: Menu lateral (*sidebar*) com seleção múltipla (`st.multiselect`) por Área de Estudo que recalcula todos os indicadores e gráficos do dashboard em tempo real.
* **Cartões de KPI**: Exibição do panorama geral contendo o total de alunos filtrados, média de horas de IA, média de horas tradicionais e a variação média das notas.
* **Visualizações por Separadores (Abas)**: Separação organizada do conteúdo em duas frentes de análise.

---

## 📈 Estrutura de Análise Visual

### Aba 1: Impacto Académico
* **Uso de IA x Desempenho Académico (Gráfico de Dispersão)**: Cruza as horas semanais de IA com a variação de nota. Utiliza uma terceira dimensão de dados através de uma **escala de cores (Colorbar)** para mapear o nível de dependência. Inclui uma linha de corte horizontal no ponto zero.
* **Variação da Nota por Tipo de Uso (Barras Horizontais)**: Agrupa os dados com `.groupby().mean()` e ordena com `.sort_values()` para apontar de forma crescente quais as estratégias de uso da IA que trazem melhor retorno académico.

### Aba 2: Saúde Mental
* **Ansiedade e Política Institucional (Barras Verticais)**: Mapeia o nível médio de stress dos alunos de acordo com as regras de uso impostas pela universidade (Proibição, Citação ou Incentivo).
* **Risco de Burnout por Perfil (Barras Empilhadas 100%)**: Utiliza a função `pd.crosstab` do Pandas com normalização pelo índice para exibir a proporção exata de risco (Baixo, Médio, Alto) dentro do grupo de utilizadores moderados versus utilizadores intensivos.

---

## 🚀 Como Executar o Projeto

1. Certifique-se de ter o Python instalado na sua máquina.
2. Clone este repositório ou descarregue os ficheiros.
3. Garanta que o ficheiro `ai_student_impact_dataset.csv` está na **mesma pasta** do ficheiro `main.py`.
4. Instale as dependências necessárias executando o comando abaixo no seu terminal:

```bash
pip install streamlit pandas numpy matplotlib
