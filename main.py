if __name__ == '__main__':
    try:
        # from codigos.outros import write_gerador
        import game
        # game.run()
        from codigos.interfaces import main_menu
        main_menu.main_menu()
    except KeyboardInterrupt:
        print('Jogo encerrado pelo console')
    except Exception as e:
        print(f'Ocorreu um erro:\n {str(e)}')
