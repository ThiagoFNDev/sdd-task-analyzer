# Governança de Contexto e Regras para Assistentes de IA (CONTEXT_RULES)

## 1. Diretrizes de Código
- **Linguagem:** Python 3.11 ou superior.
- **Tipagem:** Utilização obrigatória de *Type Hints* em 100% das assinaturas de funções e métodos.
- **Bibliotecas:** Permitido apenas o uso da Standard Library do Python para o código-fonte em `src/`. Nenhuma biblioteca externa não autorizada deve ser importada no módulo principal.

## 2. Tratamento de Erros e Resiliência
- **Exceção Customizada:** Lançar estritamente `TaskValidationError` quando houver inconsistência nos dados (ex.: `data_conclusao < data_criacao`).
- **Divisão por Zero:** O sistema nunca deve lançar `ZeroDivisionError`. Se a lista estiver vazia ou não houver tarefas concluídas, os indicadores numéricos (médias e porcentagens) devem retornar `0.0`.
- **Status Válidos:** Considerar como tarefas pendentes aquelas com status `'PENDENTE'` ou `'EM_ANDAMENTO'`. Considerar concluídas apenas aquelas com status `'CONCLUIDA'`.

## 3. Padrão de Projeto
- Funções puras e modulares.
- Código limpo, sem dependências colaterais globais.