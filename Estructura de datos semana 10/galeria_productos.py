# Galería de Productos — Lista Doblemente Enlazada
# Estructura de Datos | Semana 10

import tkinter as tk
from tkinter import ttk, messagebox, font


# ============================================================
# DATA STRUCTURE LAYER
# ============================================================

class ProductNode:
    """Node of the doubly linked list. Holds product data and prev/next pointers."""

    def __init__(self, name: str, category: str, price: float, description: str):
        # Product data attributes
        self.name = name
        self.category = category
        self.price = price
        self.description = description

        # Doubly linked list pointers
        self.previous = None   # Pointer to the previous node
        self.next = None       # Pointer to the next node

    def __str__(self):
        return (f"Product(name='{self.name}', category='{self.category}', "
                f"price={self.price:.2f}, description='{self.description}')")


class DoublyLinkedProductList:
    """
    Doubly Linked List — structure: head <-> node <-> ... <-> tail
    Traversal via 'next' (forward) and 'previous' (backward) pointers.
    """

    def __init__(self):
        self.head = None      # First node in the list
        self.tail = None      # Last node in the list
        self.current = None   # Pointer to the currently selected/displayed node
        self._size = 0        # Internal counter for number of products

    # ADD PRODUCT — inserts at tail
    def add_product(self, name: str, category: str, price: float, description: str) -> ProductNode:
        """
        Pointer logic:
            new_node.previous = old_tail
            old_tail.next     = new_node
            tail              = new_node
        """
        new_node = ProductNode(name, category, price, description)

        if self.head is None:
            # List is empty: the new node is both head and tail
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            # Attach the new node after the current tail
            new_node.previous = self.tail   # New node points back to old tail
            self.tail.next = new_node       # Old tail points forward to new node
            self.tail = new_node            # Update tail to the new node

        self._size += 1
        return new_node

    # REMOVE PRODUCT — deletes by name, re-links surrounding nodes
    def remove_product(self, name: str) -> bool:
        """
        Pointer logic (middle node):
            node.previous.next = node.next
            node.next.previous = node.previous
        Returns True if removed, False if not found.
        """
        target = self._find_node(name)
        if target is None:
            return False  # Product not found

        # --- Re-link the surrounding nodes ---
        prev_node = target.previous
        next_node = target.next

        if prev_node is not None:
            prev_node.next = next_node      # Skip over the removed node (forward)
        else:
            self.head = next_node           # Removed node was the head

        if next_node is not None:
            next_node.previous = prev_node  # Skip over the removed node (backward)
        else:
            self.tail = prev_node           # Removed node was the tail

        # --- Update current pointer so the UI doesn't break ---
        if self.current is target:
            # Prefer moving to next; fall back to previous; set None if list is empty
            if next_node is not None:
                self.current = next_node
            elif prev_node is not None:
                self.current = prev_node
            else:
                self.current = None

        # Isolate removed node (optional but good practice)
        target.previous = None
        target.next = None

        self._size -= 1
        return True

    # NAVIGATE
    def next_product(self) -> ProductNode | None:
        """Advances 'current' one step forward via the 'next' pointer."""
        if self.current is not None and self.current.next is not None:
            self.current = self.current.next
        return self.current

    def previous_product(self) -> ProductNode | None:
        """Moves 'current' one step backward via the 'previous' pointer."""
        if self.current is not None and self.current.previous is not None:
            self.current = self.current.previous
        return self.current

    # SEARCH
    def search_product(self, name: str) -> ProductNode | None:
        """Case-insensitive search. Sets 'current' if found. Returns None otherwise."""
        node = self._find_node(name)
        if node is not None:
            self.current = node
        return node

    def get_all_products(self) -> list[dict]:
        products = []
        node = self.head
        while node is not None:
            products.append({
                "name": node.name,
                "category": node.category,
                "price": node.price,
                "description": node.description,
            })
            node = node.next
        return products

    # TRAVERSAL
    def traverse_forward(self) -> list[str]:
        """head → tail using 'next' pointer."""
        result = []
        node = self.head
        while node is not None:
            result.append(node.name)
            node = node.next
        return result

    def traverse_backward(self) -> list[str]:
        """tail → head using 'previous' pointer."""
        result = []
        node = self.tail
        while node is not None:
            result.append(node.name)
            node = node.previous  # Move backward via 'previous' pointer
        return result

    def _find_node(self, name: str) -> ProductNode | None:
        node = self.head
        while node is not None:
            if node.name.strip().lower() == name.strip().lower():
                return node
            node = node.next
        return None

    # PROPERTIES
    @property
    def size(self) -> int:
        return self._size

    @property
    def is_empty(self) -> bool:
        return self._size == 0


# ============================================================
# GUI LAYER
# ============================================================

# ---- Color palette & design tokens ----
COLORS = {
    "bg_dark":       "#0F1117",   # Main background (deep dark)
    "bg_panel":      "#1A1D27",   # Panel / card background
    "bg_card":       "#22263A",   # Inner card / input background
    "accent":        "#6C63FF",   # Primary accent (violet)
    "accent_hover":  "#8B85FF",   # Accent hover shade
    "accent_alt":    "#FF6584",   # Secondary accent (pink-red)
    "accent_green":  "#43C59E",   # Success / positive action
    "accent_yellow": "#FFD166",   # Warning / search
    "text_primary":  "#EAEDF5",   # Main text
    "text_secondary":"#9CA3BE",   # Subdued text
    "text_muted":    "#5C6280",   # Very muted text
    "border":        "#2E3250",   # Borders
    "shadow":        "#090B14",   # Shadow-like dark
}


class ProductGalleryApp:
    """Tkinter GUI — wired to DoublyLinkedProductList. UI strings in Spanish."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Galería de Productos | Lista Doblemente Enlazada")
        self.root.geometry("950x700")
        self.root.configure(bg=COLORS["bg_dark"])
        self.root.resizable(True, True)
        self.root.minsize(850, 620)

        self.product_list = DoublyLinkedProductList()
        self._load_sample_products()
        self._setup_fonts()
        self._build_ui()
        self._refresh_display()

    # --- Sample data ---
    def _load_sample_products(self):
        self.product_list.add_product(
            name="Laptop UltraBook Pro",
            category="Electrónica",
            price=1299.99,
            description="Laptop de alto rendimiento con procesador i9, 32GB RAM y pantalla 4K OLED."
        )
        self.product_list.add_product(
            name="Auriculares ANC Studio",
            category="Audio",
            price=249.50,
            description="Auriculares inalámbricos con cancelación activa de ruido y 30h de batería."
        )
        self.product_list.add_product(
            name="Silla Ergonómica Flex",
            category="Mobiliario",
            price=389.00,
            description="Silla ergonómica con soporte lumbar ajustable, reposabrazos 4D y malla transpirable."
        )
        self.product_list.add_product(
            name="Monitor 4K Curvo 34\"",
            category="Electrónica",
            price=599.99,
            description="Monitor ultrawide curvo con resolución 4K, 144Hz y panel IPS de 34 pulgadas."
        )
        self.product_list.add_product(
            name="Teclado Mecánico RGB",
            category="Periféricos",
            price=129.00,
            description="Teclado mecánico con switches Cherry MX Red, retroiluminación RGB y estructura de aluminio."
        )

    def _setup_fonts(self):
        self.font_title  = font.Font(family="Segoe UI", size=16, weight="bold")
        self.font_header = font.Font(family="Segoe UI", size=11, weight="bold")
        self.font_label  = font.Font(family="Segoe UI", size=10)
        self.font_value  = font.Font(family="Segoe UI", size=10, weight="bold")
        self.font_btn    = font.Font(family="Segoe UI", size=9, weight="bold")
        self.font_small  = font.Font(family="Segoe UI", size=8)
        self.font_mono   = font.Font(family="Consolas",  size=9)

    def _build_ui(self):

        # ---- Top title bar ----
        self._build_title_bar()

        # ---- Main content frame (left panel + right panel) ----
        content = tk.Frame(self.root, bg=COLORS["bg_dark"])
        content.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(0, weight=1)

        # LEFT: current product display + navigation
        left_frame = tk.Frame(content, bg=COLORS["bg_dark"])
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self._build_product_display(left_frame)
        self._build_navigation_buttons(left_frame)

        # RIGHT: form + action buttons
        right_frame = tk.Frame(content, bg=COLORS["bg_dark"])
        right_frame.grid(row=0, column=1, sticky="nsew")
        self._build_form(right_frame)
        self._build_action_buttons(right_frame)

        # ---- Status bar at bottom ----
        self._build_status_bar()

    def _build_title_bar(self):
        bar = tk.Frame(self.root, bg=COLORS["accent"], height=60)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        inner = tk.Frame(bar, bg=COLORS["accent"])
        inner.pack(expand=True, fill="both", padx=20)

        icon = tk.Label(inner, text="🛍️", font=("Segoe UI Emoji", 20),
                        bg=COLORS["accent"], fg="white")
        icon.pack(side="left", pady=10, padx=(0, 10))

        title_text = tk.Label(
            inner,
            text="Galería de Productos",
            font=self.font_title,
            bg=COLORS["accent"],
            fg="white"
        )
        title_text.pack(side="left", pady=10)

        subtitle = tk.Label(
            inner,
            text="Lista Doblemente Enlazada",
            font=self.font_small,
            bg=COLORS["accent"],
            fg="#D6D3FF"
        )
        subtitle.pack(side="left", padx=(12, 0), pady=(16, 0))

        # Node counter badge
        self.counter_label = tk.Label(
            inner,
            text="",
            font=self.font_small,
            bg="#4A42CC",
            fg="white",
            padx=10, pady=4,
            relief="flat"
        )
        self.counter_label.pack(side="right", pady=15, padx=(0, 5))

    def _build_product_display(self, parent):
        # Section header
        section_lbl = tk.Label(
            parent, text="◉  Producto Actual",
            font=self.font_header,
            bg=COLORS["bg_dark"], fg=COLORS["accent"]
        )
        section_lbl.pack(anchor="w", pady=(12, 6))

        # Card container
        card = tk.Frame(parent, bg=COLORS["bg_panel"],
                        relief="flat", bd=0,
                        highlightbackground=COLORS["border"],
                        highlightthickness=1)
        card.pack(fill="x", pady=(0, 8))

        # Position indicator (e.g., "Nodo 2 / 5")
        pos_frame = tk.Frame(card, bg=COLORS["accent"], height=4)
        pos_frame.pack(fill="x")

        header_row = tk.Frame(card, bg=COLORS["bg_panel"])
        header_row.pack(fill="x", padx=16, pady=(12, 4))

        self.position_label = tk.Label(
            header_row, text="",
            font=self.font_small,
            bg=COLORS["bg_panel"], fg=COLORS["accent"]
        )
        self.position_label.pack(side="right")

        fields_frame = tk.Frame(card, bg=COLORS["bg_panel"])
        fields_frame.pack(fill="x", padx=16, pady=(0, 16))

        self.display_vars = {}
        field_defs = [
            ("Nombre",      "name",        "👤", COLORS["text_primary"]),
            ("Categoría",   "category",    "🏷️",  COLORS["accent_yellow"]),
            ("Precio",      "price",       "💲", COLORS["accent_green"]),
            ("Descripción", "description", "📝", COLORS["text_secondary"]),
        ]

        for label_text, key, icon, color in field_defs:
            row = tk.Frame(fields_frame, bg=COLORS["bg_panel"])
            row.pack(fill="x", pady=4)

            lbl = tk.Label(row, text=f"{icon}  {label_text}:",
                           font=self.font_label,
                           bg=COLORS["bg_panel"], fg=COLORS["text_muted"],
                           width=13, anchor="w")
            lbl.pack(side="left")

            var = tk.StringVar()
            val_lbl = tk.Label(row, textvariable=var,
                               font=self.font_value,
                               bg=COLORS["bg_panel"], fg=color,
                               anchor="w", wraplength=340, justify="left")
            val_lbl.pack(side="left", fill="x", expand=True)
            self.display_vars[key] = var

        ptr_frame = tk.Frame(card, bg=COLORS["bg_card"],
                             relief="flat", bd=0)
        ptr_frame.pack(fill="x", padx=16, pady=(0, 14))

        self.ptr_label = tk.Label(
            ptr_frame,
            text="",
            font=self.font_mono,
            bg=COLORS["bg_card"], fg=COLORS["text_muted"],
            padx=10, pady=6,
            anchor="w", justify="left"
        )
        self.ptr_label.pack(fill="x")

    def _build_navigation_buttons(self, parent):
        nav_frame = tk.Frame(parent, bg=COLORS["bg_dark"])
        nav_frame.pack(fill="x", pady=(4, 8))

        self.btn_prev = self._make_button(
            nav_frame, "◀  Anterior",
            command=self._on_previous,
            color=COLORS["bg_panel"],
            fg=COLORS["text_primary"],
            hover=COLORS["bg_card"]
        )
        self.btn_prev.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.btn_next = self._make_button(
            nav_frame, "Siguiente  ▶",
            command=self._on_next,
            color=COLORS["bg_panel"],
            fg=COLORS["text_primary"],
            hover=COLORS["bg_card"]
        )
        self.btn_next.pack(side="left", fill="x", expand=True)

        traverse_lbl = tk.Label(
            parent, text="Recorrido de la Lista",
            font=self.font_small,
            bg=COLORS["bg_dark"], fg=COLORS["text_muted"]
        )
        traverse_lbl.pack(anchor="w", pady=(6, 2))

        traverse_card = tk.Frame(
            parent, bg=COLORS["bg_panel"],
            highlightbackground=COLORS["border"],
            highlightthickness=1
        )
        traverse_card.pack(fill="x")

        self.traverse_text = tk.Label(
            traverse_card, text="",
            font=self.font_mono,
            bg=COLORS["bg_panel"], fg=COLORS["accent"],
            anchor="w", padx=10, pady=8,
            wraplength=440, justify="left"
        )
        self.traverse_text.pack(fill="x")

    def _build_form(self, parent):
        section_lbl = tk.Label(
            parent, text="✏️  Gestión de Productos",
            font=self.font_header,
            bg=COLORS["bg_dark"], fg=COLORS["accent"]
        )
        section_lbl.pack(anchor="w", pady=(12, 6))

        form_card = tk.Frame(
            parent, bg=COLORS["bg_panel"],
            highlightbackground=COLORS["border"],
            highlightthickness=1
        )
        form_card.pack(fill="x", pady=(0, 8))

        form_inner = tk.Frame(form_card, bg=COLORS["bg_panel"])
        form_inner.pack(fill="x", padx=16, pady=14)

        self.form_vars = {}
        inputs = [
            ("Nombre",      "name",        False),
            ("Categoría",   "category",    False),
            ("Precio (COP)", "price",      False),
            ("Descripción", "description", True),
        ]

        for label_text, key, is_multi in inputs:
            lbl = tk.Label(form_inner, text=label_text,
                           font=self.font_label,
                           bg=COLORS["bg_panel"], fg=COLORS["text_secondary"])
            lbl.pack(anchor="w", pady=(4, 1))

            if is_multi:
                entry = tk.Text(
                    form_inner,
                    font=self.font_label,
                    bg=COLORS["bg_card"], fg=COLORS["text_primary"],
                    insertbackground=COLORS["text_primary"],
                    relief="flat", bd=0,
                    height=3,
                    wrap="word",
                    highlightbackground=COLORS["border"],
                    highlightthickness=1
                )
                entry.pack(fill="x", pady=(0, 4))
                self.form_vars[key] = entry
            else:
                var = tk.StringVar()
                entry = tk.Entry(
                    form_inner,
                    textvariable=var,
                    font=self.font_label,
                    bg=COLORS["bg_card"], fg=COLORS["text_primary"],
                    insertbackground=COLORS["text_primary"],
                    relief="flat", bd=0,
                    highlightbackground=COLORS["border"],
                    highlightthickness=1
                )
                entry.pack(fill="x", ipady=5, pady=(0, 4))
                self.form_vars[key] = var

    def _build_action_buttons(self, parent):
        btns_frame = tk.Frame(parent, bg=COLORS["bg_dark"])
        btns_frame.pack(fill="x")

        btn_defs = [
            ("➕  Agregar producto",   self._on_add,    COLORS["accent"],        "white"),
            ("🗑️  Eliminar producto",  self._on_remove, COLORS["accent_alt"],    "white"),
            ("🔍  Buscar producto",    self._on_search, COLORS["accent_yellow"], COLORS["bg_dark"]),
            ("📋  Mostrar catálogo",   self._on_catalog, COLORS["accent_green"], COLORS["bg_dark"]),
        ]

        for text, cmd, bg, fg in btn_defs:
            btn = self._make_button(btns_frame, text, command=cmd,
                                    color=bg, fg=fg, hover=bg,
                                    padx=10, pady=9)
            btn.pack(fill="x", pady=3)

    def _build_status_bar(self):
        bar = tk.Frame(self.root, bg=COLORS["shadow"], height=28)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)

        self.status_var = tk.StringVar(value="Sistema listo.")
        status_lbl = tk.Label(
            bar, textvariable=self.status_var,
            font=self.font_small,
            bg=COLORS["shadow"], fg=COLORS["text_muted"],
            anchor="w", padx=12
        )
        status_lbl.pack(side="left", fill="y")

        info = tk.Label(
            bar,
            text="Estructura: Lista Doblemente Enlazada  |  Semana 10",
            font=self.font_small,
            bg=COLORS["shadow"], fg=COLORS["text_muted"],
            padx=12
        )
        info.pack(side="right", fill="y")

    def _make_button(self, parent, text, command,
                     color, fg, hover,
                     padx=8, pady=7):
        btn = tk.Label(
            parent, text=text,
            font=self.font_btn,
            bg=color, fg=fg,
            cursor="hand2",
            padx=padx, pady=pady,
            relief="flat"
        )
        btn.bind("<Button-1>",    lambda e: command())
        btn.bind("<Enter>",       lambda e: btn.config(bg=hover if hover != color else self._darken(color)))
        btn.bind("<Leave>",       lambda e: btn.config(bg=color))
        return btn

    @staticmethod
    def _darken(hex_color: str) -> str:
        """Returns a slightly darker version of a hex color for hover effect."""
        try:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            factor = 0.80
            r = max(0, int(r * factor))
            g = max(0, int(g * factor))
            b = max(0, int(b * factor))
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            return hex_color

    def _refresh_display(self):
        node = self.product_list.current

        if node is None:
            self.display_vars["name"].set("(Sin productos)")
            self.display_vars["category"].set("—")
            self.display_vars["price"].set("—")
            self.display_vars["description"].set("—")
            self.position_label.config(text="Lista vacía")
            self.ptr_label.config(text="head → NULL    tail → NULL")
            self.traverse_text.config(text="(lista vacía)")
            self.counter_label.config(text="0 productos")
            return

        self.display_vars["name"].set(node.name)
        self.display_vars["category"].set(node.category)
        self.display_vars["price"].set(f"COP {node.price:,.0f}")
        self.display_vars["description"].set(node.description)

        all_products = self.product_list.get_all_products()
        total = len(all_products)
        index = next((i + 1 for i, p in enumerate(all_products)
                      if p["name"] == node.name), "?")
        self.position_label.config(text=f"Nodo {index} de {total}")

        # Pointer visualization (shown in the UI card)
        prev_name = node.previous.name if node.previous else "NULL"
        next_name = node.next.name     if node.next     else "NULL"
        ptr_info = (
            f"◀  anterior: {prev_name}\n"
            f"▶  siguiente: {next_name}"
        )
        self.ptr_label.config(text=ptr_info)

        # Traversal strip — highlight the current node
        forward = self.product_list.traverse_forward()
        annotated = []
        for name in forward:
            if name == node.name:
                annotated.append(f"[{name}]")
            else:
                annotated.append(name)
        self.traverse_text.config(text="  →  ".join(annotated))

        self.counter_label.config(text=f"{total} productos")
        self._update_nav_state(node)
        self._set_status(f"Mostrando: {node.name}")

    def _update_nav_state(self, node: ProductNode):
        """Dims navigation buttons when at the boundary of the list."""
        at_start = node.previous is None
        at_end   = node.next     is None

        prev_fg = COLORS["text_muted"] if at_start else COLORS["text_primary"]
        next_fg = COLORS["text_muted"] if at_end   else COLORS["text_primary"]

        self.btn_prev.config(fg=prev_fg)
        self.btn_next.config(fg=next_fg)

    def _set_status(self, message: str):
        self.status_var.set(f"  {message}")

    # --- Event handlers ---

    def _on_previous(self):
        """Navigate to the previous product in the list."""
        if self.product_list.is_empty:
            messagebox.showwarning("Aviso", "La galería está vacía.")
            return
        node = self.product_list.previous_product()
        self._refresh_display()
        if node and node.previous is None:
            self._set_status("Ya estás en el primer producto.")

    def _on_next(self):
        """Navigate to the next product in the list."""
        if self.product_list.is_empty:
            messagebox.showwarning("Aviso", "La galería está vacía.")
            return
        node = self.product_list.next_product()
        self._refresh_display()
        if node and node.next is None:
            self._set_status("Ya estás en el último producto.")

    def _on_add(self):
        """Reads form inputs, validates, and adds a new product to the list."""
        name     = self.form_vars["name"].get().strip()
        category = self.form_vars["category"].get().strip()
        price_str = self.form_vars["price"].get().strip()
        desc_widget = self.form_vars["description"]
        description = desc_widget.get("1.0", "end").strip()

        if not name:
            messagebox.showerror("Error de validación", "El nombre del producto es obligatorio.")
            return
        if not category:
            messagebox.showerror("Error de validación", "La categoría es obligatoria.")
            return
        if not price_str:
            messagebox.showerror("Error de validación", "El precio es obligatorio.")
            return
        try:
            price = float(price_str.replace(",", "."))
            if price < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error de validación",
                                 "El precio debe ser un número positivo.\nEjemplo: 199.99")
            return
        if not description:
            messagebox.showerror("Error de validación", "La descripción es obligatoria.")
            return

        if self.product_list.search_product(name) is not None:
            messagebox.showerror("Error", f"Ya existe un producto con el nombre:\n'{name}'")
            self.product_list.current = self.product_list.current
            return

        new_node = self.product_list.add_product(name, category, price, description)
        self.product_list.current = new_node  # Jump to the newly added product

        self.form_vars["name"].set("")
        self.form_vars["category"].set("")
        self.form_vars["price"].set("")
        desc_widget.delete("1.0", "end")

        self._refresh_display()
        messagebox.showinfo("Éxito", f"Producto '{name}' agregado correctamente.")

    def _on_remove(self):
        """Removes the product whose name is typed in the form."""
        name = self.form_vars["name"].get().strip()
        if not name:
            messagebox.showerror("Error", "Escribe el nombre del producto a eliminar en el campo 'Nombre'.")
            return

        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar el producto:\n'{name}'?"
        )
        if not confirm:
            return

        removed = self.product_list.remove_product(name)
        if removed:
            self.form_vars["name"].set("")
            self._refresh_display()
            messagebox.showinfo("Éxito", f"Producto '{name}' eliminado correctamente.")
        else:
            messagebox.showerror("Producto no encontrado",
                                 f"No se encontró ningún producto con el nombre:\n'{name}'")

    def _on_search(self):
        """Searches for a product by name and moves the current pointer to it."""
        name = self.form_vars["name"].get().strip()
        if not name:
            messagebox.showerror("Error", "Escribe el nombre del producto en el campo 'Nombre'.")
            return

        node = self.product_list.search_product(name)
        if node is not None:
            self._refresh_display()
            messagebox.showinfo("Producto encontrado",
                                f"✅ Se encontró el producto:\n'{node.name}'\n\nAhora es el producto actual.")
        else:
            messagebox.showerror("Producto no encontrado",
                                 f"❌ No se encontró ningún producto con el nombre:\n'{name}'")

    def _on_catalog(self):
        """Opens a popup window showing all products in a table."""
        products = self.product_list.get_all_products()

        if not products:
            messagebox.showinfo("Catálogo vacío", "No hay productos en la galería.")
            return

        popup = tk.Toplevel(self.root)
        popup.title("Catálogo Completo de Productos")
        popup.geometry("780x450")
        popup.configure(bg=COLORS["bg_dark"])
        popup.grab_set()

        title = tk.Label(
            popup, text="📋  Catálogo de Productos",
            font=self.font_header,
            bg=COLORS["bg_dark"], fg=COLORS["accent"]
        )
        title.pack(pady=(14, 8), padx=16, anchor="w")

        fw = self.product_list.traverse_forward()
        bw = self.product_list.traverse_backward()

        trav_frame = tk.Frame(popup, bg=COLORS["bg_panel"],
                              highlightbackground=COLORS["border"],
                              highlightthickness=1)
        trav_frame.pack(fill="x", padx=16, pady=(0, 8))

        tk.Label(trav_frame, text=f"Recorrido ▶ adelante: {' → '.join(fw)}",
                 font=self.font_mono, bg=COLORS["bg_panel"], fg=COLORS["accent_green"],
                 anchor="w", padx=10, pady=5).pack(fill="x")
        tk.Label(trav_frame, text=f"Recorrido ◀ atrás:   {' → '.join(bw)}",
                 font=self.font_mono, bg=COLORS["bg_panel"], fg=COLORS["accent_yellow"],
                 anchor="w", padx=10, pady=5).pack(fill="x")

        tree_frame = tk.Frame(popup, bg=COLORS["bg_dark"])
        tree_frame.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                        background=COLORS["bg_panel"],
                        foreground=COLORS["text_primary"],
                        fieldbackground=COLORS["bg_panel"],
                        rowheight=26,
                        font=("Segoe UI", 9))
        style.configure("Custom.Treeview.Heading",
                        background=COLORS["accent"],
                        foreground="white",
                        font=("Segoe UI", 9, "bold"),
                        relief="flat")
        style.map("Custom.Treeview",
                  background=[("selected", COLORS["accent"])])

        columns = ("nodo", "nombre", "categoria", "precio", "descripcion")
        tree = ttk.Treeview(tree_frame, columns=columns,
                            show="headings", style="Custom.Treeview")

        tree.heading("nodo",        text="Nodo #")
        tree.heading("nombre",      text="Nombre")
        tree.heading("categoria",   text="Categoría")
        tree.heading("precio",      text="Precio")
        tree.heading("descripcion", text="Descripción")

        tree.column("nodo",        width=60,  anchor="center")
        tree.column("nombre",      width=180, anchor="w")
        tree.column("categoria",   width=110, anchor="center")
        tree.column("precio",      width=90,  anchor="center")
        tree.column("descripcion", width=310, anchor="w")

        for i, p in enumerate(products, start=1):
            tree.insert("", "end", values=(
                f"#{i}",
                p["name"],
                p["category"],
                f"COP {p['price']:,.0f}",
                p["description"][:60] + ("..." if len(p["description"]) > 60 else "")
            ))

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        close_btn = tk.Label(
            popup, text="Cerrar",
            font=self.font_btn,
            bg=COLORS["accent"], fg="white",
            cursor="hand2", padx=20, pady=8
        )
        close_btn.pack(pady=(0, 14))
        close_btn.bind("<Button-1>", lambda e: popup.destroy())



def main():
    root = tk.Tk()
    app = ProductGalleryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
