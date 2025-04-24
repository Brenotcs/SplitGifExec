import os
import argparse
from PIL import Image, ImageSequence

def dividir_gif_vertical(gif_path, partes=5, output_dir="gifs_divididos"):
    if partes < 1 or partes > 5:
        raise ValueError("Número de partes deve ser entre 1 e 5.")

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

    print(f"{partes} partes salvas em '{output_dir}'")

def main():
    parser = argparse.ArgumentParser(description="Divide um GIF em até 5 partes verticais.")
    parser.add_argument("gif_path", help="Caminho para o arquivo GIF")
    parser.add_argument("--partes", type=int, default=5, help="Número de partes (máx 5)")
    parser.add_argument("--saida", type=str, default="gifs_divididos", help="Pasta de saída")

    args = parser.parse_args()
    dividir_gif_vertical(args.gif_path, args.partes, args.saida)

if __name__ == "__main__":
    main()
