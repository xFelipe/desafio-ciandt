from datetime import datetime, timedelta

FORMATO_DE_DATA_E_HORA = '%Y-%m-%d %H:%M:%S'
TEMPO_MAXIMO_POR_ARRAY_DE_JOBS = timedelta(hours=8)

class JanelaTempoNegativaError(ValueError): pass
class TempoMaximoPorJobExcedidoError(ValueError): pass
class PrazoInsuficienteError(ValueError): pass
class PrazoJobInsuficienteError(ValueError): pass


def _string_para_datetime(data: str) -> datetime:
    return datetime.strptime(data, FORMATO_DE_DATA_E_HORA)


def _tempo_total(jobs: list) -> timedelta:
    if not jobs:
        return None
    return sum(
        [timedelta(seconds=job['Tempo estimado']) for job in jobs],
        timedelta()
    )


def _validar_job(job:dict , inicio: datetime, prazo: datetime):
    """Levanta exceção caso exista algum problema com o job de acordo com
    o inicio de execução e o prazo.
    """
    tempo_job = timedelta(seconds=job['Tempo estimado'])
    prazo_job = _string_para_datetime(job['Data Máxima de conclusão'])
    if tempo_job > TEMPO_MAXIMO_POR_ARRAY_DE_JOBS:
        raise TempoMaximoPorJobExcedidoError(
            f'Job {job["ID"]} - ({tempo_job}) excede o '
            f'tempo máximo de {TEMPO_MAXIMO_POR_ARRAY_DE_JOBS}.'
        )

    if inicio + tempo_job > prazo:
        raise PrazoInsuficienteError(
            f'Janela de tempo de execução ({prazo-inicio}) é insuficiente '
            f'para execução do job {job["ID"]} ({tempo_job}).'
        )

    if inicio + tempo_job > prazo_job:
        raise PrazoJobInsuficienteError(
            f'O prazo de execução({prazo_job}) do job {job["ID"]} é'
            f'insuficiente para sua janela de tempo de execução ({tempo_job}) '
            f'ao iniciar execução no momento ({inicio}).'
        )


def _adicionar_job_ao_conjunto(job: dict, conjunto: list,
                               inicio: datetime, prazo: datetime):
    """Valida e diciona jobs ao menor array do conjunto. Caso não caiba ou não
    exista um array, adiciona um array vazio ao conjunto antes.
    """
    tempo_job = timedelta(seconds=job['Tempo estimado'])
    prazo_job = _string_para_datetime(job['Data Máxima de conclusão'])

    _validar_job(job, inicio, prazo)

    menor_array = min(conjunto, key=_tempo_total) if conjunto else None
    tempo_menor_array = _tempo_total(menor_array)
    novo_array_e_necessario: bool = (
        len(conjunto) == 0
        or tempo_menor_array + tempo_job > TEMPO_MAXIMO_POR_ARRAY_DE_JOBS
        or tempo_menor_array + tempo_job + inicio > prazo
        or tempo_menor_array + tempo_job + inicio > prazo_job
    )
    if novo_array_e_necessario:
        menor_array = []
        conjunto.append(menor_array)
    menor_array.append(job)


def schedule(jobs: list, inicio: str, fim: str):
    """Ordena o agendamento de jobs de acordo com o tempo de execução inicial, 
    com o prazo geral e o prazo de cada job e retorna os id's dos jobs em 
    arrays ordenados ou retorna erro caso não seja possível executar algum
    job de acordo com os prazos.
    """
    jobs_priorizados = sorted(
        jobs,
        key=lambda job: _string_para_datetime(job['Data Máxima de conclusão'])
    )

    conjunto = []
    for job in jobs_priorizados:
        _adicionar_job_ao_conjunto(
            job,
            conjunto, 
            inicio=_string_para_datetime(inicio),
            prazo=_string_para_datetime(fim)
        )

    return [[job['ID'] for job in array] for array in conjunto]
