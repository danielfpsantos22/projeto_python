import json
from datetime import datetime, timedelta
from collections import Counter
import os

# =============================================================================
# Variáveis Globais
# =============================================================================
NOME_ARQUIVO_DADOS = "dados_tarefas.json"
lista_tarefas = []
PRIORIDADES = ["Urgente", "Alta", "Média", "Baixa"]
STATUS = ["Pendente", "Fazendo", "Concluída"]
ORIGENS = ["E-mail", "Telefone", "Chamado do Sistema"]
proximo_id = 1  # Contador para IDs únicos

# =============================================================================
# Funções de Persistência (JSON)
# =============================================================================

def carregar_dados():
    """
    Carrega a lista de tarefas do arquivo JSON e define o próximo ID.
    (Item EXTRA) Cria o arquivo se ele não existir.
    """
    global lista_tarefas, proximo_id
    
    print(f"Tentando carregar dados de '{NOME_ARQUIVO_DADOS}'...")
    
    if not os.path.exists(NOME_ARQUIVO_DADOS):
        # (Item EXTRA) Arquivos criados se não existirem
        print(f"Arquivo '{NOME_ARQUIVO_DADOS}' não encontrado. Criando um novo.")
        lista_tarefas = []
        proximo_id = 1
        return

    try:
        with open(NOME_ARQUIVO_DADOS, 'r') as f:
            data = json.load(f)
            lista_tarefas = data.get("tarefas", [])
            proximo_id = data.get("proximo_id", 1)
            
            # Converte as strings de data de volta para objetos datetime
            for tarefa in lista_tarefas:
                if "data_conclusao" in tarefa and tarefa["data_conclusao"]:
                    tarefa["data_conclusao"] = datetime.fromisoformat(tarefa["data_conclusao"])
            
            print(f"Dados carregados com sucesso! {len(lista_tarefas)} tarefas encontradas.")
            
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON. O arquivo '{NOME_ARQUIVO_DADOS}' pode estar corrompido. Iniciando com lista vazia.")
        lista_tarefas = []
        proximo_id = 1
    except Exception as e:
        print(f"Erro inesperado ao carregar dados: {e}. Iniciando com lista vazia.")
        lista_tarefas = []
        proximo_id = 1

def salvar_dados():
    """
    Salva a lista de tarefas e o próximo ID no arquivo JSON.
    As datas de conclusão são convertidas para strings (ISO format) para serialização.
    """
    global lista_tarefas, proximo_id
    
    # Prepara os dados para salvar (converte datetime para string)
    tarefas_para_salvar = []
    for tarefa in lista_tarefas:
        temp_tarefa = tarefa.copy()
        if "data_conclusao" in temp_tarefa and temp_tarefa["data_conclusao"]:
            # Converte datetime para string ISO 8601
            temp_tarefa["data_conclusao"] = temp_tarefa["data_conclusao"].isoformat()
        tarefas_para_salvar.append(temp_tarefa)

    data_to_save = {
        "tarefas": tarefas_para_salvar,
        "proximo_id": proximo_id
    }
    
    try:
        with open(NOME_ARQUIVO_DADOS, 'w') as f:
            json.dump(data_to_save, f, indent=4)
        print(f"Dados salvos com sucesso em '{NOME_ARQUIVO_DADOS}'.")
    except Exception as e:
        print(f"Erro ao salvar dados em JSON: {e}")

# =============================================================================
# Funções de Validação e Utilitárias
# =============================================================================

def validar_opcao_lista(opcao, lista):
    """Valida se uma opção existe em uma lista (case-insensitive)"""
    opcoes_lower = [item.lower() for item in lista]
    if opcao.lower() in opcoes_lower:
        idx = opcoes_lower.index(opcao.lower())
        return lista[idx]  # Retorna a versão correta com capitalização
    return None

def validar_entrada_numerica(mensagem, minimo=None, maximo=None):
    """Valida entrada numérica com tratamento de exceções"""
    while True:
        entrada = input(mensagem).strip()
        if not entrada:
            return None # Permite retorno None se a entrada for opcional
        try:
            numero = int(entrada)
            
            if minimo is not None and numero < minimo:
                print(f"Erro: O número deve ser maior ou igual a {minimo}")
                continue
                
            # Verifica o máximo (exclusivo)
            if maximo is not None and numero >= maximo:
                print(f"Erro: O índice deve ser menor que {maximo}")
                continue
                
            return numero
        except ValueError:
            print("Erro: Digite um número inteiro válido!")
            continue

def obter_proximo_id():
    """Retorna o próximo ID único disponível"""
    global proximo_id
    id_atual = proximo_id
    proximo_id += 1
    return id_atual

# =============================================================================
# Funções do Sistema de Gerenciamento de Tarefas
# =============================================================================

def criar_tarefa():
    """Cria uma nova tarefa e adiciona à lista global de tarefas"""
    global lista_tarefas
    
    print("\n--- Nova Tarefa ---")
    
    # Validação do título
    titulo = input("Título da tarefa: ").strip()
    if not titulo:
        print("Erro: Título não pode estar vazio!")
        return
    
    # Validação da prioridade
    while True:
        print(f"\nPrioridades disponíveis: {', '.join(PRIORIDADES)}")
        prioridade_input = input("Prioridade: ").strip()
        prioridade = validar_opcao_lista(prioridade_input, PRIORIDADES)
        
        if prioridade:
            break
        print(f"Prioridade inválida! Use uma das opções: {PRIORIDADES}")
    
    # Validação da origem
    while True:
        print(f"\nOrigens disponíveis: {', '.join(ORIGENS)}")
        origem_input = input("Origem: ").strip()
        origem = validar_opcao_lista(origem_input, ORIGENS)
        
        if origem:
            break
        print(f"Origem inválida! Use uma das opções: {ORIGENS}")
    
    # Criação da tarefa com ID único
    tarefa = {
        "id": obter_proximo_id(),
        "titulo": titulo,
        "prioridade": prioridade,
        "status": "Pendente",
        "origem": origem,
        "data_conclusao": None # Garante que a chave existe para JSON
    }
    
    lista_tarefas.append(tarefa)
    salvar_dados() # Salva após a criação
    print(f"✓ Tarefa criada com sucesso! ID: {tarefa['id']}")

def verificar_urgencia():
    """Busca tarefa mais urgente e atualiza status para 'Fazendo'"""
    global lista_tarefas
    
    # Verifica se há tarefa em andamento
    tarefa_em_andamento = next((t for t in lista_tarefas if t["status"] == "Fazendo"), None)
    
    if tarefa_em_andamento:
        print(f"\nJá existe uma tarefa em andamento: '{tarefa_em_andamento['titulo']}' (ID: {tarefa_em_andamento['id']})")
        return
    
    # Busca por prioridade (da mais alta para a mais baixa)
    tarefa_selecionada = None
    for prioridade in PRIORIDADES:
        for tarefa in lista_tarefas:
            if tarefa["prioridade"] == prioridade and tarefa["status"] == "Pendente":
                tarefa_selecionada = tarefa
                break
        if tarefa_selecionada:
            break
    
    if tarefa_selecionada:
        tarefa_selecionada["status"] = "Fazendo"
        salvar_dados() # Salva a mudança de status
        print(f"\n✓ Tarefa selecionada para execução:")
        print(f"  ID: {tarefa_selecionada['id']}")
        print(f"  Título: {tarefa_selecionada['titulo']}")
        print(f"  Prioridade: {tarefa_selecionada['prioridade']}")
        print(f"  Origem: {tarefa_selecionada['origem']}")
    else:
        print("Nenhuma tarefa pendente encontrada!")

def atualizar_prioridade():
    """Permite alterar a prioridade de uma tarefa"""
    global lista_tarefas
    
    if not lista_tarefas:
        print("Nenhuma tarefa cadastrada!")
        return
    
    print("\n--- Atualizar Prioridade ---")
    listar_tarefas(mostrar_indices=True) # Lista com índices
    
    # Validação do índice com tratamento de exceção
    indice = validar_entrada_numerica("\nÍndice da tarefa a atualizar: ", 0, len(lista_tarefas))
    if indice is None or indice >= len(lista_tarefas):
        print("Índice inválido ou operação cancelada.")
        return
    
    tarefa = lista_tarefas[indice]
    print(f"\nTarefa selecionada: '{tarefa['titulo']}' (ID: {tarefa['id']})")
    print(f"Prioridade atual: {tarefa['prioridade']}")
    
    # Validação da nova prioridade
    while True:
        print(f"Prioridades disponíveis: {', '.join(PRIORIDADES)}")
        nova_prioridade_input = input("Nova prioridade: ").strip()
        nova_prioridade = validar_opcao_lista(nova_prioridade_input, PRIORIDADES)
        
        if nova_prioridade:
            break
        print(f"Prioridade inválida! Use uma das opções: {PRIORIDADES}")
    
    lista_tarefas[indice]["prioridade"] = nova_prioridade
    salvar_dados() # Salva a mudança de prioridade
    print("✓ Prioridade atualizada com sucesso!")

def concluir_tarefa():
    """Marca tarefa como concluída e adiciona data de conclusão"""
    global lista_tarefas
    
    if not lista_tarefas:
        print("Nenhuma tarefa cadastrada!")
        return
    
    # Encontra tarefa em andamento (Prioriza a que está sendo Feito)
    tarefa_em_andamento = next((t for t in lista_tarefas if t["status"] == "Fazendo"), None)
    
    if tarefa_em_andamento:
        print(f"\nTarefa em andamento selecionada: '{tarefa_em_andamento['titulo']}' (ID: {tarefa_em_andamento['id']})")
    else:
        # Prioriza uma tarefa pendente se não houver em andamento
        tarefas_pendentes = [t for t in lista_tarefas if t["status"] == "Pendente"]
        
        if not tarefas_pendentes:
            print("Não há tarefas em andamento ou pendentes disponíveis para concluir!")
            return
        
        print("\nNenhuma tarefa em andamento. Escolha uma Pendente:")
        for i, tarefa in enumerate(tarefas_pendentes):
            print(f"{i}: {tarefa['titulo']} (ID: {tarefa['id']}, {tarefa['prioridade']})")
        
        escolha_indice = validar_entrada_numerica("\nEscolha o índice da tarefa para concluir: ", 0, len(tarefas_pendentes))
        if escolha_indice is None:
            return
        
        tarefa_em_andamento = tarefas_pendentes[escolha_indice]
    
    # Processa a conclusão
    tarefa_em_andamento["status"] = "Concluída"
    tarefa_em_andamento["data_conclusao"] = datetime.now()
    salvar_dados() # Salva a conclusão
    print(f"✓ Tarefa '{tarefa_em_andamento['titulo']}' (ID: {tarefa_em_andamento['id']}) concluída com sucesso!")

def listar_tarefas(mostrar_indices=False):
    """Exibe um resumo das tarefas, opcionalmente com índices para seleção"""
    global lista_tarefas

    if not lista_tarefas:
        print("Nenhuma tarefa cadastrada!")
        return

    print("\n--- Lista de Tarefas (Resumo) ---")
    for i, t in enumerate(lista_tarefas):
        titulo = t.get("titulo", "-")
        prioridade = t.get("prioridade", "-")
        status = t.get("status", "-")
        id_tarefa = t.get("id", "-")
        prefixo = f"{i}: " if mostrar_indices else ""
        print(f"{prefixo}[{id_tarefa}] {titulo} ({prioridade}) - {status}")

def estatisticas():
    """Mostra estatísticas simples sobre as tarefas cadastradas"""
    global lista_tarefas

    if not lista_tarefas:
        print("Nenhuma tarefa cadastrada!")
        return

    prioridades = Counter(t.get("prioridade", "-") for t in lista_tarefas)
    status = Counter(t.get("status", "-") for t in lista_tarefas)
    origens = Counter(t.get("origem", "-") for t in lista_tarefas)

    print("\n--- Estatísticas ---")
    print(f"Total de tarefas: {len(lista_tarefas)}")
    print("Por prioridade:")
    for p in PRIORIDADES:
        print(f"  {p}: {prioridades.get(p, 0)}")
    print("Por status:")
    for s in STATUS:
        print(f"  {s}: {status.get(s, 0)}")
    print("Por origem:")
    for o in ORIGENS:
        print(f"  {o}: {origens.get(o, 0)}")

def relatorio_tarefas():
    """Exibe um relatório completo com todas as tarefas cadastradas."""
    global lista_tarefas

    if not lista_tarefas:
        print("Nenhuma tarefa cadastrada!")
        return

    print("\n--- Relatório Completo de Tarefas ---")
    for i, t in enumerate(lista_tarefas):
        titulo = t.get("titulo", "-")
        prioridade = t.get("prioridade", "-")
        status = t.get("status", "-")
        origem = t.get("origem", "-")
        id_tarefa = t.get("id", "-")
        data = t.get("data_conclusao")
        
        if data and isinstance(data, datetime):
            data_str = data.strftime("%Y-%m-%d %H:%M:%S")
        else:
            data_str = "-"
            
        print(f"{i}: ID:{id_tarefa} | {titulo} | Prioridade: {prioridade} | Status: {status} | Origem: {origem} | Conclusão: {data_str}")

def excluir_concluidas_antigas():
    """Exclui tarefas com status 'Concluída' mais antigas que N dias (padrão 30)."""
    global lista_tarefas

    concluidas = [t for t in lista_tarefas if t.get("status") == "Concluída"]
    if not concluidas:
        print("Nenhuma tarefa concluída encontrada!")
        return

    print(f"\nExistem {len(concluidas)} tarefas concluídas.")
    
    # Validação dos dias
    entrada = input("Remover tarefas concluídas há quantos dias (padrão 30): ").strip()
    dias = int(entrada) if entrada and entrada.isdigit() and int(entrada) >= 0 else 30
    
    corte = datetime.now() - timedelta(days=dias)

    def tarefa_antiga(t):
        data = t.get("data_conclusao")
        # Se não tiver data_conclusao, não a considera para exclusão por antiguidade, a menos que se defina
        if not isinstance(data, datetime):
            return False
        return data < corte

    para_remover = [t for t in lista_tarefas if t.get("status") == "Concluída" and tarefa_antiga(t)]
    if not para_remover:
        print(f"Nenhuma tarefa concluída com mais de {dias} dias encontrada!")
        return

    print(f"Tarefas a serem removidas ({len(para_remover)}):")
    for t in para_remover:
        data = t.get("data_conclusao").strftime("%Y-%m-%d") if t.get("data_conclusao") else "-"
        print(f"  - ID: {t['id']}, Título: {t['titulo']} (Concluída em: {data})")

    confirm = input(f"\nConfirma a exclusão de {len(para_remover)} tarefas concluídas? (s/n): ").strip().lower()
    if confirm not in ("s", "sim", "y", "yes"):
        print("Operação cancelada.")
        return

    # Filtra a lista_tarefas, mantendo apenas as que NÃO estão em 'para_remover'
    tarefas_mantidas = []
    ids_remover = {t['id'] for t in para_remover}
    for t in lista_tarefas:
        if t.get('id') not in ids_remover:
            tarefas_mantidas.append(t)
    
    lista_tarefas = tarefas_mantidas

    salvar_dados() # Salva a lista após a exclusão
    print(f"✓ {len(para_remover)} tarefa(s) concluída(s) excluída(s) com sucesso!")

def menu_principal():
    """Menu principal do sistema de gerenciamento de tarefas"""
    
    while True:
        print()
        print("-" * 50)
        print("- - - Sistema de Gerenciamento de Tarefas - - -")
        print("-" * 50)
        print("1. Criar Nova Tarefa")
        print("2. Buscar Tarefa Mais Urgente (Coloca em 'Fazendo')")
        print("3. Atualizar Prioridade")
        print("4. Concluir Tarefa")
        print("5. Excluir Tarefas Concluídas Antigas")
        print("6. Relatório Completo")
        print("7. Listar Tarefas (Resumo)")
        print("8. Estatísticas")
        print("0. Sair")
        print("-" * 50)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            criar_tarefa()
        elif opcao == "2":
            verificar_urgencia()
        elif opcao == "3":
            atualizar_prioridade()
        elif opcao == "4":
            concluir_tarefa()
        elif opcao == "5":
            excluir_concluidas_antigas()
        elif opcao == "6":
            relatorio_tarefas()
        elif opcao == "7":
            listar_tarefas()
        elif opcao == "8":
            estatisticas()
        elif opcao == "0":
            print("Salvando dados e saindo do sistema...")
            salvar_dados() # Salva ao sair
            break
        else:
            print("Opção inválida! Tente novamente.")

# =============================================================================
# Execução Principal
# =============================================================================
if __name__ == "__main__":
    print("Sistema de Gerenciamento de Tarefas Iniciando...Aguarde...")
    carregar_dados() # Carrega os dados ao iniciar
    menu_principal()