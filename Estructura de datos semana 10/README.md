# 🛍️ Product Gallery — Doubly Linked List

**Course:** Data Structures — Week 10  
**Topic:** Doubly Linked List  
**Language:** Python 3.10+  
**GUI:** Tkinter (built into Python, no extra installation required)

---

## 📌 Project Context

This project implements a **Doubly Linked List** as the core data structure for managing a product catalog. Each product is stored as a **node** containing data (name, category, price, description) and two pointers: one to the previous node (`previous`) and one to the next node (`next`).

```
NULL ← [Laptop] ⟷ [Headphones] ⟷ [Chair] → NULL
         head                                 tail
                        ↑
                     current
```

The application demonstrates the structure in real time:
- The traversal strip shows the **full forward order** of the list, highlighting the current node.
- The product card shows the **`previous` and `next` pointer values** of the active node.
- The catalog popup shows the **traversal in both directions**.

---

## 🗂️ Project Structure

```
Estructura de datos semana 10/
│
├── galeria_productos.py   # Full source code (single file)
└── README.md              # This file
```

### Main Classes

| Class | Responsibility |
|---|---|
| `ProductNode` | List node: product data + `previous` / `next` pointers |
| `DoublyLinkedProductList` | Doubly linked list: `head`, `tail`, `current` and all methods |
| `ProductGalleryApp` | Tkinter GUI wired to the list |

### List Methods

| Method | Description |
|---|---|
| `add_product()` | Inserts a new node at the tail |
| `remove_product()` | Removes a node by name and re-links surrounding pointers |
| `next_product()` | Advances the `current` pointer forward |
| `previous_product()` | Moves the `current` pointer backward |
| `search_product()` | Finds a node by name and sets it as `current` |
| `traverse_forward()` | Iterates from `head` to `tail` using the `next` pointer |
| `traverse_backward()` | Iterates from `tail` to `head` using the `previous` pointer |
| `get_all_products()` | Returns all products as a list of dictionaries |

---

## ▶️ How to Run

### Requirements

- **Python 3.10 or higher** installed on your system.
- Tkinter is bundled with Python on Windows — no extra packages needed.

### Check Python installation

Open a terminal (CMD or PowerShell) and run:

```bash
python --version
```

You should see something like `Python 3.11.x`.

### Run the program

Navigate to the project folder and execute:

```bash
python galeria_productos.py
```

Alternatively, you can **double-click** the file `galeria_productos.py` if Python is associated with `.py` files on your system.

---

## 🖥️ Interface Features

| Button | Action |
|---|---|
| **Anterior** | Navigate to the previous node in the list |
| **Siguiente** | Navigate to the next node in the list |
| **Agregar producto** | Add a new node at the tail of the list |
| **Eliminar producto** | Remove the node matching the typed name |
| **Buscar producto** | Search by name and set it as the current node |
| **Mostrar catálogo** | Open a popup with all products and both traversals |

> **To delete or search:** type the exact product name in the **Nombre** field before clicking the button.

---

## 📦 Preloaded Sample Products

The list is initialized with 5 products on startup:

1. Laptop UltraBook Pro — Electronics
2. Auriculares ANC Studio — Audio
3. Silla Ergonómica Flex — Furniture
4. Monitor 4K Curvo 34" — Electronics
5. Teclado Mecánico RGB — Peripherals
