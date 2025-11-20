# =============================================================================
# Variáveis Globais
# =============================================================================
lista_tarefas = []
PRIORIDADES = ["Urgente", "Alta", "Média", "Baixa"]
STATUS = ["Pendente", "Fazendo", "Concluída"]
ORIGENS = ["E-mail", "Telefone", "Chamado do Sistema"]
proximo_id = 1  # Contador para IDs únicos
 
# =============================================================================
# Funções de Validação e Utilitárias
# =============================================================================
 
def validar_opcao_lista(opcao, lista):
    """Valida se uma opção existe em uma lista (case-insensitive)"""
    print(f"Validando opção '{opcao}' na lista {lista}")
    
    opcoes_lower = [item.lower() for item in lista]
    if opcao.lower() in opcoes_lower:
        idx = opcoes_lower.index(opcao.lower())
        return lista[idx]  # Retorna a versão correta com capitalização
    return None
 
def validar_entrada_numerica(mensagem, minimo=None, maximo=None):
    """Valida entrada numérica com tratamento de exceções"""
    print(f"Validando entrada numérica: {mensagem}")
    
    try:
        numero = int(input(mensagem))
        
        if minimo is not None and numero < minimo:
            print(f"Erro: O número deve ser maior ou igual a {minimo}")
            return None
            
        if maximo is not None and numero >= maximo:
            print(f"Erro: O número deve ser menor que {maximo}")
            return None
            
        return numero
    except ValueError:
        print("Erro: Digite um número válido!")
        return None
 
def obter_proximo_id():
    """Retorna o próximo ID único disponível"""
    global proximo_id
    print(f"Obtendo próximo ID: {proximo_id}")
    
    id_atual = proximo_id
    proximo_id += 1
    return id_atual
 
# =============================================================================
# Funções do Sistema
# =============================================================================
 
def criar_tarefa():
    """Cria uma nova tarefa e adiciona à lista global de tarefas"""
    print("Executando a função criar_tarefa")
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
        "origem": origem
    }
    
    lista_tarefas.append(tarefa)
    print(f"✓ Tarefa criada com sucesso! ID: {tarefa['id']}")
 
def verificar_urgencia():
    """Busca tarefa mais urgente e atualiza status para 'Fazendo'"""
    print("Executando a função verificar_urgencia")
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
        print(f"\n✓ Tarefa selecionada para execução:")
        print(f"  ID: {tarefa_selecionada['id']}")
        print(f"  Título: {tarefa_selecionada['titulo']}")
        print(f"  Prioridade: {tarefa_selecionada['prioridade']}")
        print(f"  Origem: {tarefa_selecionada['origem']}")
    else:
        print("Nenhuma tarefa pendente encontrada!")
 
def atualizar_prioridade():
    """Permite alterar a prioridade de uma tarefa"""
    print("Executando a função atualizar_prioridade")
    global lista_tarefas
    
    if not lista_tarefas:
        print("Nenhuma tarefa cadastrada!")
        return
    
    print("\n--- Atualizar Prioridade ---")
    listar_tarefas()
    
    # Validação do índice com tratamento de exceção
    indice = validar_entrada_numerica("\nÍndice da tarefa a atualizar: ", 0, len(lista_tarefas))
    if indice is None:
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
    print("✓ Prioridade atualizada com sucesso!")
 
def concluir_tarefa():
    """Marca tarefa como concluída e adiciona data de conclusão"""
    print("Executando a função concluir_tarefa")
    global lista_tarefas
    
    if not lista_tarefas:
        print("Nenhuma tarefa cadastrada!")
        return
    
    # Encontra tarefa em andamento
    tarefa_em_andamento = next((t for t in lista_tarefas if t["status"] == "Fazendo"), None)
    
    if not tarefa_em_andamento:
        print("Nenhuma tarefa em andamento para concluir!")
        # Mostra tarefas pendentes para o usuário escolher
        tarefas_pendentes = [t for t in lista_tarefas if t["status"] == "Pendente"]
        
        if not tarefas_pendentes:
            print("Não há tarefas pendentes disponíveis!")
            return
        
        print("\nTarefas pendentes disponíveis:")
        for i, tarefa in enumerate(tarefas_pendentes):
            print(f"{i}: {tarefa['titulo']} (ID: {tarefa['id']}, {tarefa['prioridade']})")
        
        # Validação da escolha com tratamento de exceção
        escolha = validar_entrada_numerica("\nEscolha o índice da tarefa para concluir: ", 0, len(tarefas_pendentes))
        if escolha is None:
            return
        
        tarefa_em_andamento = tarefas_pendentes[escolha]
    
    from datetime import datetime
    tarefa_em_andamento["status"] = "Concluída"
    tarefa_em_andamento["data_conclusao"] = datetime.now()
    print(f"✓ Tarefa '{tarefa_em_andamento['titulo']}' (ID: {tarefa_em_andamento['id']}) concluída com sucesso!")
 
def listar_tarefas():
    """Exibe um resumo das tarefas com índices para seleção"""
    print("Executando a função listar_tarefas")
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
        print(f"{i}: [{id_tarefa}] {titulo} ({prioridade}) - {status}")
 
def estatisticas():
    """Mostra estatísticas simples sobre as tarefas cadastradas"""
    print("Executando a função estatisticas")
    global lista_tarefas
 
    if not lista_tarefas:
        print("Nenhuma tarefa cadastrada!")
        return
 
    from collections import Counter
    prioridades = Counter(t.get("prioridade", "-") for t in lista_tarefas)
    status = Counter(t.get("status", "-") for t in lista_tarefas)
    origens = Counter(t.get("origem", "-") for t in lista_tarefas)
 
    print("\n--- Estatísticas ---")
    print(f"Total de tarefas: {len(lista_tarefas)}")
    print("Por prioridade:")
    for p in PRIORIDADES:
        print(f"  {p}: {prioridades.get(p, 0)}")
    print("Por status:")
    for s in STATUS:
        print(f"  {s}: {status.get(s, 0)}")
    print("Por origem:")
    for o in ORIGENS:
        print(f"  {o}: {origens.get(o, 0)}")
 
def relatorio_tarefas():
    """Exibe um relatório completo com todas as tarefas cadastradas."""
    print("Executando a função relatorio_tarefas")
    global lista_tarefas
 
    if not lista_tarefas:
        print("Nenhuma tarefa cadastrada!")
        return
 
    from datetime import datetime
    print("\n--- Relatório Completo de Tarefas ---")
    for i, t in enumerate(lista_tarefas):
        titulo = t.get("titulo", "-")
        prioridade = t.get("prioridade", "-")
        status = t.get("status", "-")
        origem = t.get("origem", "-")
        id_tarefa = t.get("id", "-")
        data = t.get("data_conclusao")
        
        if data and hasattr(data, "strftime"):
            data_str = data.strftime("%Y-%m-%d %H:%M:%S")
        else:
            data_str = "-"
            
        print(f"{i}: ID:{id_tarefa} | {titulo} | Prioridade: {prioridade} | Status: {status} | Origem: {origem} | Conclusão: {data_str}")
 
def excluir_concluidas_antigas():
    """Exclui tarefas com status 'Concluída' mais antigas que N dias (padrão 30)."""
    print("Executando a função excluir_concluidas_antigas")
    global lista_tarefas
 
    concluidas = [t for t in lista_tarefas if t.get("status") == "Concluída"]
    if not concluidas:
        print("Nenhuma tarefa concluída encontrada!")
        return
 
    print(f"\nExistem {len(concluidas)} tarefas concluídas.")
    
    # Validação dos dias com tratamento de exceção
    entrada = input("Remover tarefas concluídas há quantos dias (padrão 30): ").strip()
    dias = validar_entrada_numerica("", minimo=0) if entrada else 30
    
    if dias is None:
        return
 
    from datetime import datetime, timedelta
    corte = datetime.now() - timedelta(days=dias)
 
    def tarefa_antiga(t):
        data = t.get("data_conclusao")
        if not data:
            return True
        return data < corte
 
    para_remover = [t for t in lista_tarefas if t.get("status") == "Concluída" and tarefa_antiga(t)]
    if not para_remover:
        print(f"Nenhuma tarefa concluída com mais de {dias} dias encontrada!")
        return
 
    print(f"Tarefas a serem removidas ({len(para_remover)}):")
    for t in para_remover:
        print(f"  - ID: {t['id']}, Título: {t['titulo']}")
 
    confirm = input(f"\nConfirma a exclusão de {len(para_remover)} tarefas concluídas? (s/n): ").strip().lower()
    if confirm not in ("s", "sim", "y", "yes"):
        print("Operação cancelada.")
        return
 
    lista_tarefas = [t for t in lista_tarefas if not (t.get("status") == "Concluída" and tarefa_antiga(t))]
    print(f"✓ {len(para_remover)} tarefa(s) concluída(s) excluída(s) com sucesso!")
 
def menu_principal():
    """Menu principal do sistema de gerenciamento de tarefas"""
    print("Executando a função menu_principal")
    
    while True:
        print()
        print("-" * 50)
        print("- - - Sistema de Gerenciamento de Tarefas - - -")
        print("-" * 50)
        print("1. Criar Nova Tarefa")
        print("2. Buscar Tarefa Mais Urgente")
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
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida! Tente novamente.")
 
# =============================================================================
# Execução Principal
# =============================================================================
if __name__ == "__main__":
    print("Sistema de Gerenciamento de Tarefas Iniciando...Aguarde...")
    menu_principal()