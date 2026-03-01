import os
from rich.console import Console

def run_nano():
    console = Console()
    console.clear()
    
    filename = console.input("[bold cyan]Podaj nazwę pliku do edycji (np. plik.txt): [/bold cyan]").strip()
    if not filename:
        console.print("[red]Nie podano nazwy pliku. Anulowano.[/red]")
        return

    content = []
    # Wczytywanie istniejącego pliku
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read().splitlines()
        except Exception as e:
            console.print(f"[bold red]Błąd odczytu pliku: {e}[/bold red]")
            return

    def print_editor():
        console.clear()
        console.print(f"[black on white] PyNano - Edytor pliku: {filename} [/black on white]")
        console.print("[cyan]Instrukcje:[/cyan]")
        console.print(" Wpisz po prostu tekst, aby [bold]dodać go na sam koniec[/bold] pliku.")
        console.print(" [yellow]:e <nr>[/yellow] - edytuj linię, [yellow]:d <nr>[/yellow] - usuń linię, [yellow]:i <nr>[/yellow] - wstaw nową przed linią")
        console.print(" [yellow]:p[/yellow] - odśwież widok, [yellow]:wq[/yellow] - zapisz i wyjdź, [yellow]:q[/yellow] - wyjdź bez zapisu")
        console.print("-" * 55)
        
        # Wyświetlanie ponumerowanych linii
        for i, line in enumerate(content):
            console.print(f"[dim]{i + 1:3} |[/dim] {line}")
        console.print("-" * 55)

    # Pierwsze rysowanie ekranu edytora
    print_editor()

    # Główna pętla
    while True:
        try:
            cmd = console.input("[bold green]>[/bold green] ").strip()
            
            # Zapisz i wyjdź
            if cmd == ":wq":
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write("\n".join(content) + "\n")
                    console.print(f"\n[bold green]✅ Pomyślnie zapisano plik: {filename}[/bold green]")
                except Exception as e:
                    console.print(f"\n[bold red]❌ Błąd zapisu: {e}[/bold red]")
                break
            
            # Wyjdź bez zapisu
            elif cmd == ":q":
                console.print("\n[bold red]Wyjście bez zapisywania zmian.[/bold red]")
                break
            
            # Odśwież widok
            elif cmd == ":p":
                print_editor()
            
            # Edycja istniejącej linii
            elif cmd.startswith(":e "):
                try:
                    line_num = int(cmd[3:].strip()) - 1
                    if 0 <= line_num < len(content):
                        console.print(f"[dim]Obecny tekst:[/dim] {content[line_num]}")
                        new_line = console.input("[bold yellow]Nowy tekst:[/bold yellow] ")
                        content[line_num] = new_line
                        print_editor()
                    else:
                        console.print("[red]Nieprawidłowy numer linii![/red]")
                except ValueError:
                    console.print("[red]Podaj poprawny numer linii, np. :e 2[/red]")
            
            # Usuwanie linii
            elif cmd.startswith(":d "):
                try:
                    line_num = int(cmd[3:].strip()) - 1
                    if 0 <= line_num < len(content):
                        del content[line_num]
                        print_editor()
                    else:
                        console.print("[red]Nieprawidłowy numer linii![/red]")
                except ValueError:
                    console.print("[red]Podaj poprawny numer linii, np. :d 2[/red]")
            
            # Wstawianie nowej linii między istniejącymi
            elif cmd.startswith(":i "):
                try:
                    line_num = int(cmd[3:].strip()) - 1
                    if 0 <= line_num <= len(content):
                        new_line = console.input("[bold yellow]Wpisz nową linię:[/bold yellow] ")
                        content.insert(line_num, new_line)
                        print_editor()
                    else:
                        console.print("[red]Nieprawidłowy numer linii![/red]")
                except ValueError:
                    console.print("[red]Podaj poprawny numer linii, np. :i 2[/red]")
            
            # Zwykłe dodawanie tekstu na koniec pliku
            elif cmd:
                content.append(cmd)
                print_editor()

        except (EOFError, KeyboardInterrupt):
            # Obsługa skrótu Ctrl+C
            console.print("\n[bold red]Przerwano. Wyjście bez zapisu.[/bold red]")
            break

def register(mod_commands):
    mod_commands['nano'] = run_nano
