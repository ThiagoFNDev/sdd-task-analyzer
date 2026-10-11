from datetime import datetime
from typing import Any, Dict, List, TypedDict


class TaskValidationError(Exception):
    """Exceção lançada quando os dados de uma tarefa são inconsistentes."""
    pass


class PriorityMetric(TypedDict):
    total_concluidas: int
    tempo_medio_conclusao_horas: float


class AnalysisResult(TypedDict):
    total_tarefas: int
    total_concluidas: int
    total_pendentes: int
    tempo_medio_conclusao_horas: float
    taxa_atraso_percentual: float
    metricas_por_prioridade: Dict[str, PriorityMetric]


def analyze_tasks(tasks: List[Dict[str, Any]]) -> AnalysisResult:
    """
    Analisa um conjunto de tarefas e calcula métricas operacionais e de produtividade.

    :param tasks: Lista de dicionários representando as tarefas.
    :return: Dicionário tipado contendo as métricas consolidadas.
    :raises TaskValidationError: Se a data de conclusão for anterior à data de criação.
    """
    if not tasks:
        return {
            "total_tarefas": 0,
            "total_concluidas": 0,
            "total_pendentes": 0,
            "tempo_medio_conclusao_horas": 0.0,
            "taxa_atraso_percentual": 0.0,
            "metricas_por_prioridade": {}
        }

    total_tarefas: int = len(tasks)
    concluidas: List[Dict[str, Any]] = []
    total_pendentes: int = 0

    # Dicionário auxiliar para agrupamento por prioridade
    prioridades_map: Dict[str, List[Dict[str, Any]]] = {}

    for task in tasks:
        status: str = str(task.get("status", "")).upper()
        prioridade: str = str(task.get("prioridade", "MEDIA")).upper()

        data_criacao: datetime = task["data_criacao"]
        data_conclusao: datetime | None = task.get("data_conclusao")

        # Validação de consistência temporal (Regra de Negócio)
        if data_conclusao is not None and data_conclusao < data_criacao:
            raise TaskValidationError(
                f"Data de conclusão ({data_conclusao}) não pode ser anterior à "
                f"data de criação ({data_criacao}) na tarefa ID {task.get('id_tarefa')}."
            )

        if status == "CONCLUIDA":
            concluidas.append(task)
            if prioridade not in prioridades_map:
                prioridades_map[prioridade] = []
            prioridades_map[prioridade].append(task)
        else:
            total_pendentes += 1

    total_concluidas: int = len(concluidas)

    # Prevenção de divisão por zero caso não existam tarefas concluídas
    if total_concluidas == 0:
        return {
            "total_tarefas": total_tarefas,
            "total_concluidas": 0,
            "total_pendentes": total_pendentes,
            "tempo_medio_conclusao_horas": 0.0,
            "taxa_atraso_percentual": 0.0,
            "metricas_por_prioridade": {}
        }

    # Cálculo do Tempo Médio e Atrasos
    soma_horas_total: float = 0.0
    total_atrasadas: int = 0

    for task in concluidas:
        dt_criacao: datetime = task["data_criacao"]
        dt_conclusao: datetime = task["data_conclusao"]
        dt_limite: datetime = task["data_limite"]

        # Horas decorridas
        duracao_horas: float = (dt_conclusao - dt_criacao).total_seconds() / 3600.0
        soma_horas_total += duracao_horas

        # Checagem de Atraso
        if dt_conclusao > dt_limite:
            total_atrasadas += 1

    tempo_medio_geral: float = round(soma_horas_total / total_concluidas, 2)
    taxa_atraso: float = round((total_atrasadas / total_concluidas) * 100.0, 2)

    # Métricas por Prioridade
    metricas_prioridade: Dict[str, PriorityMetric] = {}
    for prio, sub_list in prioridades_map.items():
        sub_total = len(sub_list)
        sub_soma_horas = sum(
            (t["data_conclusao"] - t["data_criacao"]).total_seconds() / 3600.0
            for t in sub_list
        )
        metricas_prioridade[prio] = {
            "total_concluidas": sub_total,
            "tempo_medio_conclusao_horas": round(sub_soma_horas / sub_total, 2)
        }

    return {
        "total_tarefas": total_tarefas,
        "total_concluidas": total_concluidas,
        "total_pendentes": total_pendentes,
        "tempo_medio_conclusao_horas": tempo_medio_geral,
        "taxa_atraso_percentual": taxa_atraso,
        "metricas_por_prioridade": metricas_prioridade
    }