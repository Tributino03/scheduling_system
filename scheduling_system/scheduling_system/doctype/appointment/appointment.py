# Copyright (c) 2025, Gustavo Tributino and contributors
# For license information, please see license.txt
# Importando as bibliotecas necessárias
import frappe
from frappe.model.document import Document
from frappe.utils import add_to_date, get_datetime

def verificar_conflito_horario(doc, method):
    todos_compromissos = frappe.get_list(
        "Appointment",
        filters=[
            ["seller", "=", doc.seller],
            ["name", "!=", doc.name],
            ["start_date", "<=", doc.end_date],
            ["end_date", ">=", doc.start_date],
        ],
        fields=["name"]
    )
    
    if len(todos_compromissos) > 0:
        frappe.throw("O vendedor já possui outro compromisso agendado neste horário!")

class Appointment(Document):

    def validate(self):
        verificar_conflito_horario(self, "validate")
    
    def before_insert(self):
        self.calcular_data_fim()
    
    def calcular_data_fim(self):
        if self.start_date and self.duration:
            try:
                
                if isinstance(self.duration, str) and '.' in self.duration:
                    try:
                        duracao_decimal = float(self.duration)
                        horas = int(duracao_decimal)
                        minutos = int((duracao_decimal - horas) * 60)
                    except ValueError:
                        frappe.throw("A duração está em um formato inválido. Verifique se é um número válido.")
                else:
                    
                    partes_duracao = str(self.duration).split(":")
                    if len(partes_duracao) == 3:
                        horas = int(partes_duracao[0])
                        minutos = int(partes_duracao[1])
                        segundos = float(partes_duracao[2]) if len(partes_duracao[2]) > 0 else 0
                    elif len(partes_duracao) == 2:
                        horas = int(partes_duracao[0])
                        minutos = int(partes_duracao[1])
                        segundos = 0
                    else:
                        frappe.throw("Formato de duração inválido. Certifique-se de que a duração seja fornecida como 'hh:mm:ss' ou 'hh:mm'.")
                    
                    
                    total_minutos = (horas * 60) + minutos + (segundos / 60)

                data_inicio = get_datetime(self.start_date)
                self.end_date = add_to_date(data_inicio, minutes=total_minutos)

            except Exception as e:
                frappe.throw(f"Erro ao calcular a data de término: {str(e)}. Verifique se a duração está no formato correto.")
