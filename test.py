from unittest import TestCase
from job_scheduler import (schedule, TempoMaximoPorJobExcedidoError,
                           PrazoInsuficienteError, PrazoJobInsuficienteError)

SEGUNDO = 1
MINUTO = 60 * SEGUNDO
HORA = 60 * MINUTO


class TestJobScheduler(TestCase):
    def setUp(self):
        self.inicio = '2019-11-10 09:00:00'
        self.fim = '2019-11-11 12:00:00'
        self.jobs = [
            {
                "ID": 1,
                "Descrição": "Importação de arquivos de fundos",
                "Data Máxima de conclusão": "2019-11-10 12:00:00",
                "Tempo estimado": 2 * HORA
            },
            {
                "ID": 2,
                "Descrição": "Importação de dados da Base Legada",
                "Data Máxima de conclusão": "2019-11-11 12:00:00",
                "Tempo estimado": 4 * HORA
            },
            {
                "ID": 3,
                "Descrição": "Importação de dados de integração",
                "Data Máxima de conclusão": "2019-11-11 08:00:00",
                "Tempo estimado": 6 * HORA
            }
        ]

    def test_scheduling_job(self):
        result = schedule(
            self.jobs, inicio=self.inicio, fim=self.fim
        )
        expected = [
            [1,3],
            [2]
        ]
        assert result == expected

    def test_tempo_estimado_de_job_inválido(self):
        job_com_tempo_estimado_inválido = [
            {
                "ID": 1,
                "Descrição": "Importação de arquivos de fundos",
                "Data Máxima de conclusão": "2019-11-10 10:30:00",
                "Tempo estimado": 9 * HORA
            }
        ]
        self.assertRaises(
            TempoMaximoPorJobExcedidoError,
            schedule,
            job_com_tempo_estimado_inválido,
            self.inicio,
            self.fim
        )

    def test_prazo_insuficiente(self):
        job_de_2_horas = [
            {
                "ID": 1,
                "Descrição": "Importação de arquivos de fundos",
                "Data Máxima de conclusão": "2019-11-10 12:00:00",
                "Tempo estimado": 2 * HORA
            }
        ]
        inicio = '2019-11-10 09:00:00'
        fim_apos_1_hora = '2019-11-10 10:00:00'

        self.assertRaises(
            PrazoInsuficienteError,
            schedule,
            job_de_2_horas,
            inicio,
            fim_apos_1_hora
        )

    def test_prazo_do_job_insuficiente(self):
        job_data_maxima_conclusao_proxima = [
            {
                "ID": 1,
                "Descrição": "Importação de arquivos de fundos",
                "Data Máxima de conclusão": '2019-11-10 10:00:00',
                "Tempo estimado": 2 * HORA
            }
        ]
        inicio = '2019-11-10 09:00:00'
        fim = '2019-11-10 15:00:00'

        self.assertRaises(
            PrazoJobInsuficienteError,
            schedule,
            job_data_maxima_conclusao_proxima,
            inicio,
            fim
        )
