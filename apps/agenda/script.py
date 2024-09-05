import holidays
from datetime import date, timedelta
from django.utils import timezone
from .models import Evento
from users.models import Empresa
from users.models import User
from datetime import date, timedelta

def adicionar_feriados_e_datas_comemorativas(empresa, user):
    # Obtém o ano atual
    ano_atual = date.today().year

    # Obter feriados nacionais do Brasil usando a biblioteca holidays
    br_holidays = holidays.Brazil(years=ano_atual)

    # Função para calcular a Black Friday
    def black_friday(year):
        last_day_of_november = date(year, 11, 30)
        while last_day_of_november.weekday() != 4:  # 4 é sexta-feira
            last_day_of_november -= timedelta(days=1)
        return last_day_of_november

    # Adicionar Black Friday ao calendário
    br_holidays[black_friday(ano_atual)] = "Black Friday"

    # Adicionar outros eventos importantes, como Dia das Mães, Dia dos Pais
    def dia_das_maes(year):
        first_day_of_may = date(year, 5, 1)
        days_to_sunday = 6 - first_day_of_may.weekday()  # 6 é domingo
        second_sunday = first_day_of_may + timedelta(days=days_to_sunday + 7)
        return second_sunday

    br_holidays[dia_das_maes(ano_atual)] = "Dia das Mães"

    # Iterar sobre os feriados e criar os eventos no banco de dados
    for feriado_data, nome_feriado in br_holidays.items():
        # Converter a data ingênua para timezone-aware
        data_inicio = timezone.make_aware(timezone.datetime.combine(feriado_data, timezone.datetime.min.time()))
        data_fim = timezone.make_aware(timezone.datetime.combine(feriado_data, timezone.datetime.min.time()))

        # Usar get_or_create para evitar duplicações por empresa
        Evento.objects.get_or_create(
            user=user,
            titulo=nome_feriado,
            resumo=f"Feriado ou data comemorativa: {nome_feriado}",
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa  # Garante que o evento é criado para a empresa específica
        )

def gerar_eventos_anuais():
    empresas = Empresa.objects.filter(is_active=True)
    for empresa in empresas:
        user = User.objects.filter(empresa=empresa, if_funcionario=False).first()
        adicionar_feriados_e_datas_comemorativas(empresa, user)