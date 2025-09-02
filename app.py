import sqlite3

conn = sqlite3.connect('todos.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT 0
)
''')
conn.commit()

def add_todo(title, description):
    cursor.execute('INSERT INTO todos (title, description) VALUES (?, ?)', (title, description))
    conn.commit()
    print("Todo added.")

def list_todos():
    cursor.execute('SELECT id, title, description, completed FROM todos')
    for row in cursor.fetchall():
        print(row)

def update_todo(todo_id, title, description, completed):
    cursor.execute('UPDATE todos SET title=?, description=?, completed=? WHERE id=?', (title, description, completed, todo_id))
    conn.commit()
    print("Todo updated.")

def delete_todo(todo_id):
    cursor.execute('DELETE FROM todos WHERE id=?', (todo_id,))
    conn.commit()
    print("Todo deleted.")

# Simple CLI loop
while True:
    print("\n1. Add Todo\n2. List Todos\n3. Update Todo\n4. Delete Todo\n5. Exit")
    choice = input("Choose an option: ")
    if choice == '1':
        title = input("Title: ")
        description = input("Description: ")
        add_todo(title, description)
    elif choice == '2':
        list_todos()
    elif choice == '3':
        todo_id = int(input("Todo ID to update: "))
        title = input("New Title: ")
        description = input("New Description: ")
        completed = int(input("Completed? (0/1): "))
        update_todo(todo_id, title, description, completed)
    elif choice == '4':
        todo_id = int(input("Todo ID to delete: "))
        delete_todo(todo_id)
    elif choice == '5':
        break
    else:
        print("Invalid choice.")

conn.close()