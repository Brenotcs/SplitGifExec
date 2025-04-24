import os
from tkinter import Tk, filedialog, Button, Label, Spinbox, messagebox
from PIL import Image, ImageSequence

def dividir_gif_vertical(gif_path, partes=5):
    if partes < 1 or partes > 5:
        raise ValueError("Número de partes deve ser entre 1 e 5.")

    output_dir = os.path.join(os.path.dirname(gif_path), "gifs_divididos")
    os.makedirs(output_dir, exist_ok=True)

    gif = Image.open(gif_path)
    largura_total, altura = gif.size
    largura_parte = largura_total // partes

    partes_gifs = [[] for _ in range(partes)]

    for frame in ImageSequence.Iterator(gif):
        for i in range(partes):
            esquerda = i * largura_parte
            direita = esquerda + largura_parte
            parte = frame.crop((esquerda, 0, direita, altura))
            partes_gifs[i].append(parte.convert("RGBA"))

    for i, frames in enumerate(partes_gifs):
        nome_saida = os.path.join(output_dir, f"parte_{i+1}.gif")
        frames[0].save(
            nome_saida,
            save_all=True,
            append_images=frames[1:],
            duration=gif.info.get("duration", 100),
            loop=0,
            disposal=2
        )

    messagebox.showinfo("Sucesso", f"GIF dividido em {partes} partes.\nSalvo em:\n{output_dir}")

def escolher_gif():
    caminho = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if caminho:
        partes = int(spinbox.get())
        try:
            dividir_gif_vertical(caminho, partes)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

# GUI
app = Tk()
app.title("Dividir GIF Verticalmente")
app.geometry("300x150")

Label(app, text="Número de partes (1-5):").pack(pady=10)
spinbox = Spinbox(app, from_=1, to=5)
spinbox.pack()

Button(app, text="Escolher GIF e Dividir", command=escolher_gif).pack(pady=20)

app.mainloop()
