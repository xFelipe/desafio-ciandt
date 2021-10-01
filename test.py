from unittest import TestCase
from job_scheduler import schedule

SEGUNDO = 1
MINUTO = 60 * SEGUNDO
HORA = 60 * MINUTO

class TestJobScheduler(TestCase):
    def setUp(self):
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
            self.jobs, inicio='2019-11-10 09:00:00', fim='2019-11-11 12:00:00'
        )
        expected = [
            [1,3],
            [2]
        ]
        assert result == expected

    def test_janela_de_tempo_invalida(self):
        self.assertRaises(
            ValueError,
            schedule,
            self.jobs,
            inicio='2019-11-11 12:00:00',
            fim='2019-11-10 09:00:00'
        )
