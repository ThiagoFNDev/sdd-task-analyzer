# Contrato de Especificação Técnica SDD - TaskAnalyzer

## 1. Função Principal: `analyze_tasks`
- **Entrada:** `tasks: list[dict[str, Any]]`
- **Saída:** `dict[str, Any]` contendo:
  - `total_tarefas`: int
  - `total_concluidas`: int
  - `total_pendentes`: int
  - `tempo_medio_conclusao_horas`: float (arredondado em 2 casas)
  - `taxa_atraso_percentual`: float (arredondado em 2 casas)
  - `metricas_por_prioridade`: dict[str, dict[str, float | int]]

## 2. Campos Obrigatórios do Dicionário de Tarefa
- `id_tarefa` (int)
- `titulo` (str)
- `status` (str) -> `'PENDENTE'`, `'EM_ANDAMENTO'`, `'CONCLUIDA'`
- `prioridade` (str) -> `'BAIXA'`, `'MEDIA'`, `'ALTA'`
- `data_criacao` (datetime)
- `data_limite` (datetime)
- `data_conclusao` (datetime | None)

## 3. Regras de Negócio
1. Se `data_conclusao` for fornecida e `data_conclusao < data_criacao`, disparar a exceção `TaskValidationError`.
2. Uma tarefa é considerada **atrasada** se `status == 'CONCLUIDA'` e `data_conclusao > data_limite`.
3. O cálculo de tempo de conclusão de cada tarefa é a diferença em horas entre `data_conclusao` e `data_criacao`.