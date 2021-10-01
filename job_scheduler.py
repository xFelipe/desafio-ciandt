from datetime import datetime, timedelta

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def schedule(jobs, inicio, fim):
    datetime_inicio = datetime.strptime(inicio, DATETIME_FORMAT)
    datetime_fim = datetime.strptime(fim, DATETIME_FORMAT)
    janela_de_tempo = datetime_fim-datetime_inicio
    if janela_de_tempo < timedelta(0):
        raise ValueError(
            f'Não é possível trabalhar com janela de tempo negativa ({janela_de_tempo}).'
        )
    print(janela_de_tempo)
    