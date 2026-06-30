import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

selected_images = []


def select_images():
    global selected_images

    files = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")
        ]
    )

    if not files:
        return

    selected_images = list(files)

    listbox.delete(0, tk.END)

    for file in selected_images:
        listbox.insert(tk.END, os.path.basename(file))

    preview_image(selected_images[0])


def preview_image(path):
    try:
        img = Image.open(path)
        img.thumbnail((250, 250))

        photo = ImageTk.PhotoImage(img)

        preview_label.config(image=photo)
        preview_label.image = photo

    except Exception:
        messagebox.showerror("Error", "Cannot preview image.")


def create_gif():
    if len(selected_images) == 0:
        messagebox.showwarning(
            "Warning",
            "Please select images."
        )
        return

    try:
        duration = int(duration_entry.get())

        images = []

        first = Image.open(selected_images[0]).convert("RGB")
        size = first.size

        images.append(first)

        for file in selected_images[1:]:
            img = Image.open(file).convert("RGB")
            img = img.resize(size)
            images.append(img)

        save_path = filedialog.asksaveasfilename(
            defaultextension=".gif",
            filetypes=[("GIF File", "*.gif")]
        )

        if not save_path:
            return

        images[0].save(
            save_path,
            save_all=True,
            append_images=images[1:],
            duration=duration,
            loop=0
        )

        messagebox.showinfo(
            "Success",
            f"GIF saved successfully!\n\n{save_path}"
        )

    except ValueError:
        messagebox.showerror(
            "Error",
            "Duration must be a number."
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


def clear_selection():
    global selected_images

    selected_images = []

    listbox.delete(0, tk.END)

    preview_label.config(image="")
    preview_label.image = None


root = tk.Tk()
root.title("Animated GIF Generator")
root.geometry("550x600")
root.resizable(False, False)

title = tk.Label(
    root,
    text="Animated GIF Generator",
    font=("Arial", 18, "bold")
)

title.pack(pady=10)

btn_select = tk.Button(
    root,
    text="Select Images",
    command=select_images,
    width=20
)

btn_select.pack(pady=5)

listbox = tk.Listbox(
    root,
    width=60,
    height=10
)

listbox.pack(pady=10)

preview_label = tk.Label(root)
preview_label.pack()

duration_label = tk.Label(
    root,
    text="Frame Duration (milliseconds)"
)

duration_label.pack(pady=5)

duration_entry = tk.Entry(root)
duration_entry.insert(0, "500")
duration_entry.pack()

btn_create = tk.Button(
    root,
    text="Create GIF",
    command=create_gif,
    bg="green",
    fg="white",
    width=20
)

btn_create.pack(pady=10)

btn_clear = tk.Button(
    root,
    text="Clear",
    command=clear_selection,
    width=20
)

btn_clear.pack()

root.mainloop()