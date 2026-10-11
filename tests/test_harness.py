from datetime import datetime, timedelta
import pytest

from src.task_analyzer import analyze_tasks, TaskValidationError


def test_cenario_1_sucesso_calculo_metricas():
    """Cenário 1: Entrada válida com tarefas concluídas, atrasadas e pendentes."""
    agora = datetime.now()
    
    tasks = [
        # Tarefa 1: Concluída no prazo (Duração: 4 horas)
        {
            "id_tarefa": 1,
            "titulo": "Tarefa no Prazo",
            "status": "CONCLUIDA",
            "prioridade": "ALTA",
            "data_criacao": agora - timedelta(hours=4),
            "data_limite": agora + timedelta(hours=2),
            "data_conclusao": agora
        },
        # Tarefa 2: Concluída COM ATRASO (Duração: 10 horas, prazo era 5h)
        {
            "id_tarefa": 2,
            "titulo": "Tarefa Atrasada",
            "status": "CONCLUIDA",
            "prioridade": "BAIXA",
            "data_criacao": agora - timedelta(hours=10),
            "data_limite": agora - timedelta(hours=5),
            "data_conclusao": agora
        },
        # Tarefa 3: Pendente
        {
            "id_tarefa": 3,
            "titulo": "Tarefa em Andamento",
            "status": "EM_ANDAMENTO",
            "prioridade": "ALTA",
            "data_criacao": agora - timedelta(hours=1),
            "data_limite": agora + timedelta(hours=5),
            "data_conclusao": None
        }
    ]

    resultado = analyze_tasks(tasks)

    assert resultado["total_tarefas"] == 3
    assert resultado["total_concluidas"] == 2
    assert resultado["total_pendentes"] == 1
    # Tempo médio das 2 concluídas: (4 + 10) / 2 = 7.0 horas
    assert resultado["tempo_medio_conclusao_horas"] == 7.0
    # Taxa de Atraso: 1 de 2 concluídas está atrasada = 50.0%
    assert resultado["taxa_atraso_percentual"] == 50.0
    # Métricas por Prioridade
    assert resultado["metricas_por_prioridade"]["ALTA"]["total_concluidas"] == 1
    assert resultado["metricas_por_prioridade"]["ALTA"]["tempo_medio_conclusao_horas"] == 4.0
    assert resultado["metricas_por_prioridade"]["BAIXA"]["total_concluidas"] == 1
    assert resultado["metricas_por_prioridade"]["BAIXA"]["tempo_medio_conclusao_horas"] == 10.0


def test_cenario_2_excecao_data_invalida():
    """Cenário 2: Valida se lança TaskValidationError para data_conclusao < data_criacao."""
    agora = datetime.now()
    
    tasks = [
        {
            "id_tarefa": 99,
            "titulo": "Tarefa com Data Impossível",
            "status": "CONCLUIDA",
            "prioridade": "MEDIA",
            "data_criacao": agora,
            "data_limite": agora + timedelta(days=1),
            "data_conclusao": agora - timedelta(hours=2)  # Inconsistência!
        }
    ]

    with pytest.raises(TaskValidationError) as exc_info:
        analyze_tasks(tasks)
    
    assert "não pode ser anterior à data de criação" in str(exc_info.value)


def test_casos_de_borda_lista_vazia():
    """Caso de Borda 1: Entrada totalmente vazia."""
    resultado = analyze_tasks([])

    assert resultado["total_tarefas"] == 0
    assert resultado["total_concluidas"] == 0
    assert resultado["total_pendentes"] == 0
    assert resultado["tempo_medio_conclusao_horas"] == 0.0
    assert resultado["taxa_atraso_percentual"] == 0.0
    assert resultado["metricas_por_prioridade"] == {}


def test_casos_de_borda_apenas_pendentes():
    """Caso de Borda 2: Nenhuma tarefa concluída (evita divisão por zero)."""
    agora = datetime.now()
    tasks = [
        {
            "id_tarefa": 1,
            "titulo": "Apenas Pendente",
            "status": "PENDENTE",
            "prioridade": "MEDIA",
            "data_criacao": agora,
            "data_limite": agora + timedelta(days=1),
            "data_conclusao": None
        }
    ]

    resultado = analyze_tasks(tasks)

    assert resultado["total_tarefas"] == 1
    assert resultado["total_concluidas"] == 0
    assert resultado["total_pendentes"] == 1
    assert resultado["tempo_medio_conclusao_horas"] == 0.0
    assert resultado["taxa_atraso_percentual"] == 0.0