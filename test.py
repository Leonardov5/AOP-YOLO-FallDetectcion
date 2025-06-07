from ultralytics import YOLO

if __name__ == '__main__':
    # Carregar o modelo treinado
    model = YOLO("models/fallDetection.pt")  # Substitua pelo caminho do modelo salvo
    #model = YOLO("yolo11n.pt")  # Substitua pelo caminho do modelo salvo

    # Realizar previsões em uma nova imagem
    #results = model(0, show=True)
    results = model("material/video3.mp4", show=True)  # Substitua pelo caminho da nova imagem
    #results[0].show()  # Exibir os resultados

    # Opcional: Salvar os resultados em um arquivo
    #results.save("")  # Substitua pelo caminho da pasta de saída