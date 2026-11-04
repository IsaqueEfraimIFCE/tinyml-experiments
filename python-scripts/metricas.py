import os
import glob
import time
import numpy as np
import tensorflow as tf
import psutil
import csv

# Caminho para a pasta contendo os modelos .tflite
pasta_modelos = 'models'

# Lista todos os arquivos .tflite na pasta
caminhos_modelos = glob.glob(os.path.join(pasta_modelos, '*.tflite'))

# Nome do arquivo CSV de saída
arquivo_saida = 'resultados_modelos.csv'

# Cabeçalho do CSV
cabecalho = [
    'nome_modelo',
    'tempo_medio_ms',
    'tempo_min_ms',
    'tempo_max_ms',
    'desvio_padrao_ms',
    'memoria_antes_bytes',
    'memoria_depois_bytes',
    'variacao_memoria_bytes',
    'tamanho_entrada_bytes',
    'tamanho_modelo_bytes'
]

# Abre o arquivo CSV para escrita
with open(arquivo_saida, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(cabecalho)

    # Itera sobre cada modelo
    for caminho_modelo in caminhos_modelos:
        nome_modelo = os.path.basename(caminho_modelo)

        try:
            # Carrega o modelo TFLite
            interpreter = tf.lite.Interpreter(model_path=caminho_modelo)
            interpreter.allocate_tensors()

            # Obtém detalhes dos tensores de entrada e saída
            detalhes_entrada = interpreter.get_input_details()
            detalhes_saida = interpreter.get_output_details()

            # Gera dados de entrada aleatórios com a forma esperada
            forma_entrada = detalhes_entrada[0]['shape']
            tipo_dado = detalhes_entrada[0]['dtype']
            entrada = np.random.rand(*forma_entrada).astype(tipo_dado)

            # Define o tensor de entrada
            interpreter.set_tensor(detalhes_entrada[0]['index'], entrada)

            # Mede o tempo de execução e o uso de memória para N inferências
            tempos = []
            N = 100000  # Ajuste aqui conforme necessidade
            processo = psutil.Process(os.getpid())
            memoria_antes = processo.memory_info().rss  # em bytes

            for _ in range(N):
                inicio = time.perf_counter()
                interpreter.invoke()
                fim = time.perf_counter()
                tempos.append((fim - inicio) * 1000)  # converte para ms

            memoria_depois = processo.memory_info().rss  # em bytes

            # Calcula métricas
            tempo_medio_ms = np.mean(tempos)
            tempo_min_ms = np.min(tempos)
            tempo_max_ms = np.max(tempos)
            desvio_padrao_ms = np.std(tempos)
            variacao_memoria = memoria_depois - memoria_antes
            tamanho_entrada = entrada.nbytes
            tamanho_modelo = os.path.getsize(caminho_modelo)

            # Escreve os resultados no CSV
            writer.writerow([
                nome_modelo,
                f"{tempo_medio_ms:.3f}",
                f"{tempo_min_ms:.3f}",
                f"{tempo_max_ms:.3f}",
                f"{desvio_padrao_ms:.3f}",
                memoria_antes,
                memoria_depois,
                variacao_memoria,
                tamanho_entrada,
                tamanho_modelo
            ])

            # Imprime resultados
            print(f"Processado: {nome_modelo}")
            print(f"  Tempo médio: {tempo_medio_ms:.3f} ms")
            print(f"  Tempo mínimo: {tempo_min_ms:.3f} ms")
            print(f"  Tempo máximo: {tempo_max_ms:.3f} ms")
            print(f"  Desvio padrão: {desvio_padrao_ms:.3f} ms")
            print(f"  Variação de memória: {variacao_memoria} bytes\n")

        except Exception as e:
            print(f"Erro ao processar {nome_modelo}: {e}")
