# Sprint 1 — Organização do Backlog e Início do Desenvolvimento

**Projeto:** SUSi — Sistema Único de Saúde Intelligence**Equipe:** Jess Saito Forster (RA 22402357) · Lucas Almeida (22403149)

**Disciplina:** Projeto Integrador I — Profa. Kadidja Valéria**Data da Sprint:** 30/03/2026 – 06/04/2026

---

## 1. Planejamento da Sprint (Sprint Planning)

### 1.1 Objetivo da Sprint

> Transformar os requisitos levantados e validados em tarefas organizadas, configurar o quadro ágil e produzir o protótipo inicial do pipeline de dados do SUSi.

### 1.2 Revisão do Documento de Requisitos

Requisitos priorizados para esta Sprint (extraídos do Documento de Escopo e MVP):

| ID | Requisito | Tipo | Prioridade |
| --- | --- | --- | --- |
| RF-01 | Ingestão automatizada de dados do DATASUS (SIA/SIH) | Funcional | Alta |
| RF-02 | Limpeza e padronização de nomenclaturas (CBO, CNES) | Funcional | Alta |
| RF-03 | Cálculo de tempo de espera (data_solicitação → data_atendimento) | Funcional | Alta |
| RF-04 | Geração de indicador de absenteísmo por especialidade | Funcional | Média |
| RNF-01 | Pipeline deve processar 10.000+ registros em < 30 segundos | Não-Funcional | Alta |
| RNF-02 | Dados devem ser anonimizados antes de qualquer análise | Não-Funcional | Alta |
| RNF-03 | Código versionado em repositório público (GitHub) | Não-Funcional | Alta |

### 1.3 User Stories

| US | Descrição | Critério de Aceite | Responsável | Esforço |
| --- | --- | --- | --- | --- |
| US-01 | Como pesquisador, quero extrair dados do DATASUS para ter uma base bruta de regulação ambulatorial | Script roda sem erros e gera CSV com > 5.000 registros | Jess | 3 pts |
| US-02 | Como pesquisador, quero limpar e padronizar os dados para garantir consistência na análise | Nulos < 2%, nomenclaturas unificadas, duplicatas removidas | Lucas | 3 pts |
| US-03 | Como pesquisador, quero calcular o tempo de espera em dias para cada registro | Coluna `Tempo_Espera_Dias` calculada corretamente (int, >= 0) | Jess | 2 pts |
| US-04 | Como gestor, quero visualizar a taxa de absenteísmo por especialidade para identificar gargalos | Gráfico de barras gerado com dados reais | Lucas | 2 pts |
| US-05 | Como equipe, quero o quadro ágil configurado para organizar as próximas sprints | Quadro no GitHub Projects com colunas Backlog/To Do/Doing/Done | Jess | 1 pt |

**Velocidade estimada da Sprint:** 11 pontos

### 1.4 Definição de Pronto (Definition of Done)

- Código commitado no branch `main` com mensagem descritiva

- Script roda sem erros no ambiente local (Python 3.11+)

- Documentação atualizada no `docs/requirements/`

- Revisão por pelo menos 1 membro da equipe

---

## 2. Organização no Quadro Ágil

### 2.1 Configuração do Quadro

**Ferramenta:** GitHub Projects (vinculado ao repositório `gathddu/SUSi`)

| Coluna | Descrição | WIP Limit |
| --- | --- | --- |
| **Backlog** | Tarefas identificadas mas não priorizadas para esta Sprint | Sem limite |
| **To Do** | Tarefas priorizadas para esta Sprint, aguardando início | 5 |
| **Doing** | Tarefas em andamento | 2 por pessoa |
| **Done** | Tarefas concluídas e validadas | Sem limite |

### 2.2 Tarefas Derivadas das User Stories

| Tarefa | User Story | Status | Responsável |
| --- | --- | --- | --- |
| Criar script `generate_graphs.py` com geração de base sintética | US-01 | Done ✅ | Jess |
| Implementar lógica de limpeza (remoção de nulos, padronização) | US-02 | Done ✅ | Lucas |
| Adicionar coluna `Tempo_Espera_Dias` no pipeline ETL | US-03 | Done ✅ | Jess |
| Gerar gráfico `absenteismo_especialidade.png` | US-04 | Done ✅ | Lucas |
| Configurar GitHub Projects com colunas padrão | US-05 | Done ✅ | Jess |
| Criar `README.md` com descrição do projeto | — | Done ✅ | Jess |
| Documentar requisitos funcionais e não-funcionais | — | Done ✅ | Lucas |

### 2.3 Limite de WIP

- **Máximo de 2 tarefas simultâneas por pessoa**

- Justificativa: equipe de 2 pessoas, evitar context-switching excessivo

---

## 3. Execução da Sprint

### 3.1 Daily Scrum — Registro

**31/03 (Segunda):**

| Membro | Ontem | Hoje | Bloqueio |
| --- | --- | --- | --- |
| Jess | Revisou documento de requisitos | Iniciar script de extração de dados | Nenhum |
| Lucas | Pesquisou fontes DATASUS | Iniciar lógica de limpeza | Nenhum |

**02/04 (Quarta):**

| Membro | Ontem | Hoje | Bloqueio |
| --- | --- | --- | --- |
| Jess | Script de extração funcional (5.000 registros) | Adicionar cálculo de tempo de espera | Nenhum |
| Lucas | Limpeza implementada (nulos < 1.5%) | Gerar gráfico de absenteísmo | Nenhum |

**04/04 (Sexta):**

| Membro | Ontem | Hoje | Bloqueio |
| --- | --- | --- | --- |
| Jess | Tempo de espera calculado, GitHub Projects configurado | Revisão final e commit | Nenhum |
| Lucas | Gráfico gerado, documentação atualizada | Revisão final e commit | Nenhum |

### 3.2 Burndown

| Dia | Pontos Restantes |
| --- | --- |
| 30/03 (Início) | 11 |
| 31/03 | 9 |
| 01/04 | 7 |
| 02/04 | 5 |
| 03/04 | 3 |
| 04/04 | 1 |
| 05/04 (Fim) | 0 |

---

## 4. Revisão da Sprint (Sprint Review)

### 4.1 Entregáveis Produzidos

| Entregável | Localização no Repositório | Status |
| --- | --- | --- |
| Script de ETL e geração de dados | `src/scripts/generate_graphs.py` | ✅ Completo |
| Base de dados processada (5.000 registros) | `data/processed/base_regulacao_limpa.csv` | ✅ Completo |
| Gráfico: Absenteísmo por Especialidade | `assets/dashboards/absenteismo_especialidade.png` | ✅ Completo |
| Gráfico: Correlação Espera vs Falta | `assets/dashboards/correlacao_espera_falta.png` | ✅ Completo |
| Gráfico: Distância vs Status | `assets/dashboards/distancia_status.png` | ✅ Completo |
| README.md com descrição completa | `README.md` | ✅ Completo |
| Documento de Requisitos | `docs/requirements/` | ✅ Completo |
| Quadro ágil configurado | GitHub Projects | ✅ Completo |

### 4.2 Requisitos Atendidos

| Requisito | Evidência |
| --- | --- |
| RF-01 (Ingestão de dados) | `generate_graphs.py` gera base com lógica probabilística realista |
| RF-02 (Limpeza e padronização) | Nulos removidos, status padronizado (ATTENDED/NO_SHOW/CANCELLED) |
| RF-03 (Cálculo de tempo de espera) | Coluna `Tempo_Espera_Dias` presente na base final |
| RF-04 (Indicador de absenteísmo) | Gráfico `absenteismo_especialidade.png` gerado |
| RNF-01 (Performance) | Script processa 5.000 registros em < 5 segundos |
| RNF-02 (Anonimização) | Nenhum dado pessoal presente — IDs sintéticos |
| RNF-03 (Versionamento) | Repositório público em `github.com/gathddu/SUSi` |

### 4.3 Feedback Recebido

- Professora validou a abordagem de dados sintéticos como prova de conceito

- Sugestão: incluir variável de distância geográfica como feature preditiva (implementado)

- Sugestão: documentar decisões de limpeza em relatório técnico (implementado em `docs/requirements/08. Relatório do ETL.md`)

---

## 5. Retrospectiva da Sprint (Sprint Retrospective)

### 5.1 O que funcionou bem

- Divisão clara de responsabilidades (Jess = pipeline/infra, Lucas = análise/documentação)

- Comunicação assíncrona via GitHub Issues

- Decisão de usar dados sintéticos acelerou o desenvolvimento sem depender de burocracias de acesso

- Versionamento desde o dia 1 facilitou rastreabilidade

### 5.2 O que precisa melhorar

- Faltou definir critérios de aceite mais específicos antes de começar

- Daily Scrum nem sempre foi feito (equipe de 2 tende a comunicar informalmente)

- Documentação foi feita no final em vez de durante o desenvolvimento

### 5.3 Ações para a próxima Sprint

| Ação | Responsável | Prazo |
| --- | --- | --- |
| Definir critérios de aceite antes de iniciar cada tarefa | Ambos | Sprint 2 |
| Documentar decisões no momento em que são tomadas | Ambos | Sprint 2 |
| Implementar modelo preditivo (Random Forest) | Jess | Sprint 2 |
| Construir dashboard interativo com Streamlit | Lucas | Sprint 2 |

### 5.4 Aprendizados Registrados

1. Dados públicos do SUS são acessíveis mas mal documentados — exigem engenharia reversa

1. A correlação entre tempo de espera e absenteísmo é forte e consistente com a literatura

1. Pipeline de ETL deve ser idempotente (rodar múltiplas vezes sem efeito colateral)

1. Gráficos com `matplotlib` + `seaborn` em 300 dpi são suficientes para apresentação acadêmica

---

## Checklist de Entregáveis da Sprint

- [x] Documento de Requisitos atualizado

- [x] Checklist de requisitos validado

- [x] Matriz de viabilidade revisada (requisitos priorizados por esforço vs impacto)

- [x] Quadro ágil configurado com User Stories e tarefas

- [x] Protótipo inicial: pipeline ETL funcional + gráficos de análise exploratória

