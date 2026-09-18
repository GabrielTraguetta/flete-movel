import flet as ft

PRIORITY_COLOR = {
    "alta": "#FF6B6B",
    "media": "#F2C94C",
    "baixa": "#6FCF97",
}

PRIORITY_LABEL = {
    "alta": "Alta",
    "media": "Média",
    "baixa": "Baixa",
}

BG_LISTA = "#161B33"
BG_NOVA = "#241B3D"
BG_DETALHE = "#1B2E3D"
BG_DESTAQUE = "#5C7CFA"


def main(page: ft.Page):

    page.title = "App de Tarefas"

    tasks = [
        {
            "id": 1,
            "title": "Estudar Flet",
            "description": "Terminar os mini-exercícios da Aula 1.",
            "priority": "alta",
            "done": False,
        },
        {
            "id": 2,
            "title": "Revisar POO em Python",
            "description": "Classes, atributos e métodos.",
            "priority": "media",
            "done": False,
        },
    ]

    next_id = 3

    def limpar_pagina():
        page.controls.clear()


    def cabecalho(titulo, voltar=False):

        controles = []

        if voltar:
            controles.append(
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color="#FFFFFF",
                    on_click=lambda e: mostrar_lista(),
                )
            )

        controles.append(
            ft.Text(
                titulo,
                size=22,
                weight=ft.FontWeight.BOLD,
                color="#FFFFFF",
            )
        )

        return ft.Container(
            padding=ft.Padding(
                left=10,
                right=10,
                top=20,
                bottom=20,
            ),
            content=ft.Row(
                controls=controles,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def mostrar_lista():

        limpar_pagina()

        page.bgcolor = BG_LISTA

        # Busca
        busca = ft.TextField(
            label="Buscar tarefa",
            width=300,
            color="#FFFFFF",
            label_style=ft.TextStyle(color="#B7A9E0"),
            border_color="#4A3F7A",
            focused_border_color=BG_DESTAQUE,
        )

        lista = ft.ListView(
            expand=True,
            spacing=8,
            width=340,
        )

        # Contador
        concluidas = sum(1 for tarefa in tasks if tarefa["done"])

        contador = ft.Text(
            f"{concluidas} de {len(tasks)} tarefas concluídas",
            color="#B7A9E0",
        )

        # ----------------------------------------------------
        # CRIAR LINHAS
        # ----------------------------------------------------

        def atualizar_lista(e=None):

            lista.controls.clear()

            texto_busca = busca.value.lower() if busca.value else ""

            # Ordena: alta -> média -> baixa
            ordem = {
                "alta": 1,
                "media": 2,
                "baixa": 3,
            }

            tarefas_ordenadas = sorted(
                tasks,
                key=lambda t: ordem[t["priority"]]
            )

            for tarefa in tarefas_ordenadas:

                if texto_busca not in tarefa["title"].lower():
                    continue

                def alterar_concluida(e, t=tarefa):

                    t["done"] = e.control.value

                    mostrar_lista()

                def abrir_detalhe(e, t=tarefa):

                    mostrar_detalhe(t["id"])

                linha = ft.Container(
                    padding=12,
                    border_radius=10,
                    bgcolor="#232A4D",

                    content=ft.Row(
                        controls=[

                            ft.Checkbox(
                                value=tarefa["done"],
                                on_change=alterar_concluida,
                                active_color=BG_DESTAQUE,
                            ),

                            # Bolinha da prioridade
                            ft.Container(
                                width=10,
                                height=10,
                                border_radius=5,
                                bgcolor=PRIORITY_COLOR[
                                    tarefa["priority"]
                                ],
                            ),

                            # Título
                            ft.Text(
                                tarefa["title"],
                                expand=True,
                                color=(
                                    "#6E7695"
                                    if tarefa["done"]
                                    else "#E9ECFB"
                                ),
                            ),

                            # Seta
                            ft.Icon(
                                ft.Icons.CHEVRON_RIGHT,
                                color="#8892C4",
                            ),
                        ]
                    ),

                    on_click=abrir_detalhe,
                )

                lista.controls.append(linha)

            page.update()

        busca.on_change = atualizar_lista

        atualizar_lista()

        botao_adicionar = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            bgcolor=BG_DESTAQUE,
            on_click=lambda e: mostrar_nova_tarefa(),
        )


        page.add(
            ft.Column(
                expand=True,

                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),

                controls=[

                    cabecalho(
                        "Minhas Tarefas"
                    ),

                    busca,

                    contador,

                    lista,

                    ft.Container(
                        padding=20,
                        content=ft.Row(
                            alignment=(
                                ft.MainAxisAlignment.END
                            ),
                            controls=[
                                botao_adicionar
                            ],
                        ),
                    ),
                ],
            )
        )

        page.update()


    def mostrar_nova_tarefa(tarefa_editar=None):

        limpar_pagina()

        page.bgcolor = BG_NOVA


        titulo = ft.TextField(
            label="Título",
            width=300,
            color="#FFFFFF",
            label_style=ft.TextStyle(
                color="#B7A9E0"
            ),
            border_color="#4A3F7A",
            focused_border_color=BG_DESTAQUE,
        )

        descricao = ft.TextField(
            label="Descrição",
            multiline=True,
            min_lines=3,
            width=300,
            color="#FFFFFF",
            label_style=ft.TextStyle(
                color="#B7A9E0"
            ),
            border_color="#4A3F7A",
            focused_border_color=BG_DESTAQUE,
        )

        prioridade = ft.RadioGroup(
            value="media",

            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,

                controls=[

                    ft.Radio(
                        value="alta",
                        label="Alta",
                        label_style=ft.TextStyle(
                            color="#D8CFF2"
                        ),
                        fill_color=BG_DESTAQUE,
                    ),

                    ft.Radio(
                        value="media",
                        label="Média",
                        label_style=ft.TextStyle(
                            color="#D8CFF2"
                        ),
                        fill_color=BG_DESTAQUE,
                    ),

                    ft.Radio(
                        value="baixa",
                        label="Baixa",
                        label_style=ft.TextStyle(
                            color="#D8CFF2"
                        ),
                        fill_color=BG_DESTAQUE,
                    ),
                ],
            ),
        )

        mensagem = ft.Text(
            "",
            color="#FF6B6B",
        )


        if tarefa_editar is not None:

            titulo.value = tarefa_editar["title"]

            descricao.value = tarefa_editar["description"]

            prioridade.value = tarefa_editar["priority"]

        def salvar(e):

            nonlocal next_id

            if not titulo.value or not titulo.value.strip():

                mensagem.value = "Informe um título."

                page.update()

                return

            if tarefa_editar is not None:

                tarefa_editar["title"] = titulo.value.strip()

                tarefa_editar["description"] = (
                    descricao.value.strip()
                    if descricao.value
                    else ""
                )

                tarefa_editar["priority"] = prioridade.value

            else:

                nova_tarefa = {
                    "id": next_id,
                    "title": titulo.value.strip(),
                    "description": (
                        descricao.value.strip()
                        if descricao.value
                        else ""
                    ),
                    "priority": prioridade.value,
                    "done": False,
                }

                tasks.append(nova_tarefa)

                next_id += 1

            mostrar_lista()

        def cancelar(e):

            mostrar_lista()

       
        page.add(
            ft.Column(
                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),

                spacing=20,

                controls=[

                    cabecalho(
                        "Editar tarefa"
                        if tarefa_editar is not None
                        else "Nova tarefa",
                        voltar=True,
                    ),

                    titulo,

                    descricao,

                    ft.Text(
                        "Prioridade:",
                        color="#D8CFF2",
                    ),

                    prioridade,

                    mensagem,

                    ft.Row(
                        alignment=(
                            ft.MainAxisAlignment.CENTER
                        ),

                        controls=[

                            ft.TextButton(
                                "Cancelar",
                                on_click=cancelar,
                            ),

                            ft.ElevatedButton(
                                "Salvar",
                                on_click=salvar,
                                bgcolor=BG_DESTAQUE,
                                color="#161B33",
                            ),
                        ],
                    ),
                ],
            )
        )

        page.update()


    def mostrar_detalhe(task_id):

        limpar_pagina()

        page.bgcolor = BG_DETALHE

        tarefa = next(
            (
                t
                for t in tasks
                if t["id"] == task_id
            ),
            None,
        )


        if tarefa is None:

            page.add(
                ft.Column(
                    horizontal_alignment=(
                        ft.CrossAxisAlignment.CENTER
                    ),

                    controls=[

                        cabecalho(
                            "Tarefa não encontrada",
                            voltar=True,
                        ),

                        ft.Text(
                            "Essa tarefa não existe.",
                            color="#D6E8F0",
                        ),
                    ],
                )
            )

            page.update()

            return

        def excluir(e):

            tasks.remove(tarefa)

            mostrar_lista()

        def editar(e):

            mostrar_nova_tarefa(tarefa)

        page.add(
            ft.Column(

                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),

                spacing=20,

                controls=[

                    cabecalho(
                        "Detalhe da tarefa",
                        voltar=True,
                    ),

                    ft.Text(
                        tarefa["title"],
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#D6E8F0",
                        text_align=ft.TextAlign.CENTER,
                    ),

                    ft.Row(
                        alignment=(
                            ft.MainAxisAlignment.CENTER
                        ),

                        controls=[

                            ft.Container(
                                width=12,
                                height=12,
                                border_radius=6,
                                bgcolor=(
                                    PRIORITY_COLOR[
                                        tarefa["priority"]
                                    ]
                                ),
                            ),

                            ft.Text(
                                "Prioridade "
                                + PRIORITY_LABEL[
                                    tarefa["priority"]
                                ],
                                color="#A9C7D6",
                            ),
                        ],
                    ),

                    ft.Container(
                        width=300,

                        content=ft.Text(
                            tarefa["description"]
                            or "(sem descrição)",

                            color="#D6E8F0",

                            text_align=(
                                ft.TextAlign.CENTER
                            ),
                        ),
                    ),

                    ft.ElevatedButton(
                        "Editar",
                        icon=ft.Icons.EDIT,
                        on_click=editar,
                        bgcolor=BG_DESTAQUE,
                        color="#FFFFFF",
                    ),

                    ft.ElevatedButton(
                        "Excluir",
                        icon=ft.Icons.DELETE,
                        on_click=excluir,
                        bgcolor="#FF6B6B",
                        color="#1B2E3D",
                    ),
                ],
            )
        )

        page.update()

    mostrar_lista()

ft.app(main)