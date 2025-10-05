#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulador de Dados de Sensores - Projeto Smart Office
====================================================

Este script gera dados simulados de sensores para um projeto Smart Office,
incluindo sensores de temperatura, luminosidade e ocupação.

Autor: [Maycon Ferreira]
Data: [03/10/2025]
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def gerar_timestamps_7_dias():
    """
    Gera timestamps para 7 dias consecutivos com intervalos de 15 minutos.
    
    Returns:
        list: Lista de timestamps no formato datetime
    """
    # Data de início (pode ser ajustada conforme necessário)
    data_inicio = datetime(2024, 1, 15, 0, 0, 0)  # 15 de janeiro de 2024, meia-noite
    
    # Gerar timestamps a cada 15 minutos por 7 dias
    timestamps = []
    for dia in range(7):  # 7 dias
        for hora in range(0, 24):  # 24 horas
            for minuto in range(0, 60, 15):  # A cada 15 minutos
                timestamp = data_inicio + timedelta(days=dia, hours=hora, minutes=minuto)
                timestamps.append(timestamp)
    
    return timestamps

def simular_temperatura(timestamp):
    """
    Simula dados de temperatura com variação diurna/nocturna.
    
    Args:
        timestamp (datetime): Timestamp do registro
        
    Returns:
        float: Valor da temperatura em Celsius
    """
    hora = timestamp.hour
    dia_semana = timestamp.weekday()  # 0 = segunda, 6 = domingo
    
    # Temperatura base varia entre 18-25°C
    temp_base = 21.5
    
    # Variação diurna: mais quente durante o dia (9h-18h)
    if 9 <= hora <= 18:
        # Horário comercial: temperatura mais alta
        variacao_diurna = 3.5 * np.sin((hora - 9) * np.pi / 9)  # Pico ao meio-dia
        temp_base += variacao_diurna
    elif 19 <= hora <= 23 or 0 <= hora <= 6:
        # Noite/madrugada: temperatura mais baixa
        temp_base -= 2.0
    else:
        # Transição manhã/tarde
        temp_base += 1.0
    
    # Variação aleatória para simular flutuações naturais
    variacao_aleatoria = np.random.normal(0, 0.8)
    
    # Fins de semana podem ter ligeira variação (menos atividade)
    if dia_semana >= 5:  # Sábado (5) ou Domingo (6)
        temp_base -= 0.5
    
    temperatura_final = temp_base + variacao_aleatoria
    
    # Limitar temperatura entre 16°C e 28°C
    return max(16.0, min(28.0, temperatura_final))

def simular_luminosidade(timestamp):
    """
    Simula dados de luminosidade com padrão solar.
    
    Args:
        timestamp (datetime): Timestamp do registro
        
    Returns:
        float: Valor da luminosidade em lux
    """
    hora = timestamp.hour
    minuto = timestamp.minute
    
    # Converter para hora decimal para cálculos mais precisos
    hora_decimal = hora + minuto / 60.0
    
    # Durante a noite (20h às 6h): luminosidade = 0
    if hora_decimal >= 20 or hora_decimal <= 6:
        return 0.0
    
    # Simular nascer do sol (6h às 8h)
    elif 6 < hora_decimal <= 8:
        # Progressão linear de 0 a 500 lux
        return (hora_decimal - 6) * 250
    
    # Simular pôr do sol (18h às 20h)
    elif 18 <= hora_decimal < 20:
        # Progressão linear de 500 a 0 lux
        return (20 - hora_decimal) * 250
    
    # Durante o dia (8h às 18h): simular curva solar
    else:
        # Curva senoidal com pico ao meio-dia (13h)
        # Mapear 8h-18h para 0-π
        x = (hora_decimal - 8) * np.pi / 10
        # Luminosidade máxima de 1000 lux ao meio-dia
        luminosidade_base = 1000 * np.sin(x)
        
        # Adicionar variação aleatória (nuvens, etc.)
        variacao_aleatoria = np.random.normal(0, 50)
        
        return max(0, luminosidade_base + variacao_aleatoria)

def simular_ocupacao(timestamp):
    """
    Simula dados de ocupação com padrão comercial e eventos esporádicos.
    
    Args:
        timestamp (datetime): Timestamp do registro
        
    Returns:
        int: 1 para ocupado, 0 para livre
    """
    hora = timestamp.hour
    dia_semana = timestamp.weekday()  # 0 = segunda, 6 = domingo
    
    # Horário comercial: segunda a sexta, 9h às 18h
    if dia_semana < 5 and 9 <= hora < 18:  # Segunda a sexta
        # Alta probabilidade de ocupação (95%)
        return 1 if random.random() < 0.95 else 0
    
    # Fora do horário comercial em dias úteis
    elif dia_semana < 5:
        # Baixa probabilidade (5% para eventos esporádicos)
        return 1 if random.random() < 0.05 else 0
    
    # Fins de semana
    else:
        # Muito baixa probabilidade (2% para eventos esporádicos)
        return 1 if random.random() < 0.02 else 0

def main():
    """
    Função principal que executa a simulação completa.
    """
    print("Iniciando simulacao de dados do Smart Office...")
    
    # 1. Gerar timestamps para 7 dias
    print("Gerando timestamps para 7 dias...")
    timestamps = gerar_timestamps_7_dias()
    print(f"   OK: {len(timestamps)} timestamps gerados")
    
    # 2. Preparar listas para armazenar os dados
    dados_sensores = []
    
    # 3. Simular dados para cada timestamp
    print("Simulando dados dos sensores...")
    
    for i, timestamp in enumerate(timestamps):
        if i % 100 == 0:  # Progress indicator
            print(f"   Processando: {i}/{len(timestamps)} registros")
        
        # Sensor de Temperatura
        temp_value = simular_temperatura(timestamp)
        dados_sensores.append({
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'sensor_id': 'TEMP01',
            'value': round(temp_value, 2)
        })
        
        # Sensor de Luminosidade
        lux_value = simular_luminosidade(timestamp)
        dados_sensores.append({
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'sensor_id': 'LUX01',
            'value': round(lux_value, 2)
        })
        
        # Sensor de Ocupação
        occ_value = simular_ocupacao(timestamp)
        dados_sensores.append({
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'sensor_id': 'OCCU01',
            'value': occ_value
        })
    
    # 4. Criar DataFrame e salvar em CSV
    print("Criando arquivo CSV...")
    df = pd.DataFrame(dados_sensores)
    
    # Salvar arquivo
    nome_arquivo = 'smart_office_data.csv'
    df.to_csv(nome_arquivo, index=False, encoding='utf-8')
    
    # 5. Exibir estatísticas resumidas
    print("\nEstatisticas dos Dados Gerados:")
    print(f"   Total de registros: {len(df):,}")
    print(f"   Periodo: {df['timestamp'].min()} ate {df['timestamp'].max()}")
    print(f"   Sensores: {df['sensor_id'].nunique()} tipos")
    
    # Estatísticas por sensor
    for sensor in df['sensor_id'].unique():
        dados_sensor = df[df['sensor_id'] == sensor]['value']
        print(f"   {sensor}:")
        print(f"      Media: {dados_sensor.mean():.2f}")
        print(f"      Min: {dados_sensor.min():.2f}")
        print(f"      Max: {dados_sensor.max():.2f}")
    
    print(f"\nSimulacao concluida! Arquivo salvo como: {nome_arquivo}")
    print("Dados prontos para analise do projeto Smart Office!")

if __name__ == "__main__":
    # Definir seed para reprodutibilidade (opcional)
    np.random.seed(42)
    random.seed(42)
    
    # Executar simulação
    main()
