from datetime import datetime, timedelta

FORMATO_DE_DATA_E_HORA = '%Y-%m-%d %H:%M:%S'


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
            job['Data Máxima de conclusão'],FORMATO_DE_DATA_E_HORA
        )
    )

    conjunto = []
