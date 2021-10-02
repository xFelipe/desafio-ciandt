from datetime import datetime, timedelta

FORMATO_DE_DATA_E_HORA = '%Y-%m-%d %H:%M:%S'
TEMPO_MAXIMO_POR_ARRAY_DE_JOBS = timedelta(hours=8)


def _tempo_total(jobs: list) -> timedelta:
    if not jobs:
        return None
    return sum(
        [timedelta(seconds=job['Tempo estimado']) for job in jobs],
        timedelta()
    )


def _adicionar_job_ao_conjunto(job: dict, conjunto: list,
                               inicio: datetime, prazo: datetime):
    """Adiciona jobs ao menor array do conjunto. Caso não caiba ou não exista
    um array, adiciona um array vazio ao conjunto antes.
    """
    tempo_job = timedelta(seconds=job['Tempo estimado'])
    menor_array = min(conjunto, key=_tempo_total) if conjunto else None
    tempo_menor_array = _tempo_total(menor_array)
    novo_array_e_necessario: bool = (
        len(conjunto) == 0
        or tempo_menor_array + tempo_job > TEMPO_MAXIMO_POR_ARRAY_DE_JOBS
        or tempo_menor_array + tempo_job + inicio > prazo
        or tempo_menor_array + tempo_job + inicio > datetime.strptime(
            job['Data Máxima de conclusão'], FORMATO_DE_DATA_E_HORA
        )
    )
    if novo_array_e_necessario:
        menor_array = []
        conjunto.append(menor_array)
    menor_array.append(job)


def schedule(jobs, inicio: str, fim: str):
    datetime_inicio = datetime.strptime(inicio, FORMATO_DE_DATA_E_HORA)
    datetime_fim = datetime.strptime(fim, FORMATO_DE_DATA_E_HORA)
    janela_de_tempo = datetime_fim - datetime_inicio

    if janela_de_tempo < timedelta(0):
        raise ValueError(
            'Não é possível trabalhar com '
            f'janela de tempo negativa ({janela_de_tempo}).'
        )
    jobs_priorizados = sorted(
        jobs,
        key=lambda job: datetime.strptime(
            job['Data Máxima de conclusão'], FORMATO_DE_DATA_E_HORA
        )
    )

    conjunto = []
    for job in jobs_priorizados:
        _adicionar_job_ao_conjunto(job, conjunto, datetime_inicio, datetime_fim)

    return [[job['ID'] for job in array] for array in conjunto]
