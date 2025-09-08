import json
import os
import argparse

# =========================
# Konfiguracija fajlova
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TASKS_FILE = os.path.join(BASE_DIR, "tasks.json")

# =========================
# Funkcije za rad sa zadacima
# =========================

def load_tasks():
    """Učitava zadatke iz JSON fajla"""
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    """Čuva zadatke u JSON fajl"""
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

def add_task(tasks, description, status="todo"):
    """Dodaje novi zadatak"""
    new_task = {"id": len(tasks)+1, "description": description, "status": status}
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"✅ Zadatak '{description}' dodat!")

def list_tasks(tasks):
    """Ispis svih zadataka, sortirano po statusu i ID-ju"""
    if not tasks:
        print("⚠️ Nema zadataka.")
        return
    # Sortiranje: prvo todo, pa done, zatim po ID
    tasks_sorted = sorted(tasks, key=lambda x: (x['status'] == 'done', x['id']))
    for task in tasks_sorted:
        print(f"{task['id']}. {task['description']} - [{task['status']}]")

def delete_task(tasks, index):
    """Brisanje zadatka po indeksu"""
    if 0 <= index < len(tasks):
        removed = tasks.pop(index)
        # Resetuj ID-jeve posle brisanja
        for i, task in enumerate(tasks):
            task["id"] = i + 1
        save_tasks(tasks)
        print(f"🗑️ Zadatak '{removed['description']}' obrisan!")
    else:
        print("⚠️ Nevažeći broj zadatka.")

def mark_done(tasks, task_id):
    """Označava zadatak kao završen"""
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            save_tasks(tasks)
            print(f"✅ Zadatak '{task['description']}' označen kao završen!")
            return
    print("⚠️ Nije pronađen zadatak sa tim ID-jem.")

def filter_tasks(tasks, status):
    """Prikazuje zadatke po statusu"""
    filtered = [task for task in tasks if task["status"] == status]
    if not filtered:
        print(f"⚠️ Nema zadataka sa statusom '{status}'.")
    else:
        for task in filtered:
            print(f"{task['id']}. {task['description']} - [{task['status']}]")

def search_tasks(tasks, keyword):
    """Pretraga zadataka po ključnoj reči"""
    filtered = [task for task in tasks if keyword.lower() in task["description"].lower()]
    if not filtered:
        print(f"⚠️ Nema zadataka koji sadrže '{keyword}'.")
    else:
        print(f"📋 Zadaci koji sadrže '{keyword}':")
        for task in filtered:
            print(f"{task['id']}. {task['description']} - [{task['status']}]")

def export_tasks(tasks, filename):
    """Export zadataka u drugi JSON fajl"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)
    print(f"💾 Zadaci eksportovani u '{filename}'")

def import_tasks(filename):
    """Import zadataka iz drugog JSON fajla"""
    if not os.path.exists(filename):
        print(f"⚠️ Fajl '{filename}' ne postoji.")
        return []
    with open(filename, "r", encoding="utf-8") as f:
        try:
            imported = json.load(f)
            print(f"📂 Zadaci importovani iz '{filename}'")
            return imported
        except json.JSONDecodeError:
            print(f"⚠️ Fajl '{filename}' nije validan JSON.")
            return []

# =========================
# Interaktivni meni
# =========================
def interactive_menu(tasks):
    """Otvara interaktivni meni ako korisnik ne unese CLI argumente"""
    while True:
        print("\n=== Task Manager ===")
        print("1. Prikazi sve zadatke")
        print("2. Dodaj novi zadatak")
        print("3. Obelezi zadatak kao zavrsen")
        print("4. Obriši zadatak")
        print("5. Pretraga zadataka po ključnoj reči")
        print("6. Export zadataka")
        print("7. Import zadataka")
        print("8. Izlaz")
        print("9. Prikazi zadatke po statusu")

        choice = input("Izaberi opciju (1-9): ")

        if choice == "1":
            list_tasks(tasks)
        elif choice == "2":
            desc = input("Unesi opis zadatka: ")
            add_task(tasks, desc)
        elif choice == "3":
            list_tasks(tasks)
            try:
                task_id = int(input("Unesi ID zadatka koji zelis da oznacis kao zavrsen: "))
                mark_done(tasks, task_id)
            except ValueError:
                print("⚠️ Unesi validan broj.")
        elif choice == "4":
            list_tasks(tasks)
            try:
                index = int(input("Unesi broj zadatka za brisanje: ")) - 1
                delete_task(tasks, index)
            except ValueError:
                print("⚠️ Unesi validan broj.")
        elif choice == "5":
            keyword = input("Unesi ključnu reč za pretragu: ")
            search_tasks(tasks, keyword)
        elif choice == "6":
            filename = input("Unesi ime fajla za export: ")
            export_tasks(tasks, filename)
        elif choice == "7":
            filename = input("Unesi ime fajla za import: ")
            imported = import_tasks(filename)
            if imported:
                tasks.extend(imported)
                # Reset ID-jeva
                for i, task in enumerate(tasks):
                    task["id"] = i + 1
                save_tasks(tasks)
        elif choice == "8":
            print("👋 Izlaz iz Task Managera. Cao!")
            break
        elif choice == "9":
            while True:
                print("\n📂 Filtriranje zadataka:")
                print("1. Samo TODO zadaci")
                print("2. Samo DONE zadaci")
                print("3. Vrati se nazad")
                filter_choice = input("Izaberi opciju: ")
                if filter_choice == "1":
                    filter_tasks(tasks, "todo")
                elif filter_choice == "2":
                    filter_tasks(tasks, "done")
                elif filter_choice == "3":
                    break
                else:
                    print("⚠️ Nevažeći izbor.")
        else:
            print("⚠️ Nevažeća opcija, pokušaj ponovo.")

# =========================
# Glavni deo - CLI i interaktivni meni
# =========================
def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Lista svih zadataka
    subparsers.add_parser("list", help="Prikazi sve zadatke")

    # Dodavanje zadatka
    parser_add = subparsers.add_parser("add", help="Dodaj novi zadatak")
    parser_add.add_argument("description", help="Opis zadatka")

    # Obeležavanje zadatka
    parser_done = subparsers.add_parser("done", help="Obelezi zadatak kao zavrsen")
    parser_done.add_argument("id", type=int, help="ID zadatka")

    # Brisanje zadatka
    parser_delete = subparsers.add_parser("delete", help="Obrisi zadatak")
    parser_delete.add_argument("id", type=int, help="ID zadatka")

    # Filtriranje zadataka
    parser_filter = subparsers.add_parser("filter", help="Prikazi zadatke po statusu")
    parser_filter.add_argument("status", choices=["todo","done"], help="Status zadatka")

    # Pretraga po ključnoj reči
    parser_search = subparsers.add_parser("search", help="Pretraga zadataka po ključnoj reči")
    parser_search.add_argument("keyword", help="Ključna reč")

    # Export zadataka
    parser_export = subparsers.add_parser("export", help="Export zadataka u JSON fajl")
    parser_export.add_argument("filename", help="Ime fajla za export")

    # Import zadataka
    parser_import = subparsers.add_parser("import", help="Import zadataka iz JSON fajla")
    parser_import.add_argument("filename", help="Ime fajla za import")

    args = parser.parse_args()
    tasks = load_tasks()

    # Ako je korisnik unio CLI argument, izvrši ga
    if args.command:
        if args.command == "list":
            list_tasks(tasks)
        elif args.command == "add":
            add_task(tasks, args.description)
        elif args.command == "done":
            mark_done(tasks, args.id)
        elif args.command == "delete":
            delete_task(tasks, args.id-1)
        elif args.command == "filter":
            filter_tasks(tasks, args.status)
        elif args.command == "search":
            search_tasks(tasks, args.keyword)
        elif args.command == "export":
            export_tasks(tasks, args.filename)
        elif args.command == "import":
            imported = import_tasks(args.filename)
            if imported:
                tasks.extend(imported)
                # Reset ID-jeva
                for i, task in enumerate(tasks):
                    task["id"] = i + 1
                save_tasks(tasks)
    else:
        # Ako nema CLI argumenata, otvara se interaktivni meni
        interactive_menu(tasks)

if __name__ == "__main__":
    main()
