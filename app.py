from flask import Flask, request, make_response
from ultralytics import YOLO
import numpy as np
import cv2
import base64
import json
import os

app = Flask(__name__)

foods = [
'rice',
'eels-on-rice',
'pilaf',
'chicken-n-egg-on-rice',
'pork-cutlet-on-rice',
'beef-curry',
'sushi',
'chicken-rice',
'fried-rice',
'tempura-bowl',
'bibimbap',
'toast',
'croissant',
'roll-bread',
'raisin-bread',
'chip-butty',
'hamburger',
'pizza',
'sandwiches',
'udon-noodle',
'tempura-udon',
'soba-noodle',
'ramen-noodle',
'beef-noodle',
'tensin-noodle',
'fried-noodle',
'spaghetti',
'Japanese-style-pancake',
'takoyaki',
'gratin',
'sauteed-vegetables',
'croquette',
'grilled-eggplant',
'sauteed-spinach',
'vegetable-tempura',
'miso-soup',
'potage',
'sausage',
'oden',
'omelet',
'ganmodoki',
'jiaozi',
'stew',
'teriyaki-grilled-fish',
'fried-fish',
'grilled-salmon',
'salmon-meuniere',
'sashimi',
'grilled-pacific-saury-',
'sukiyaki',
'sweet-and-sour-pork',
'lightly-roasted-fish',
'steamed-egg-hotchpotch',
'tempura',
'fried-chicken',
'sirloin-cutlet',
'nanbanzuke',
'boiled-fish',
'seasoned-beef-with-potatoes',
'hambarg-steak',
'beef-steak',
'dried-fish',
'ginger-pork-saute',
'spicy-chili-flavored-tofu',
'yakitori',
'cabbage-roll',
'rolled-omelet',
'egg-sunny-side-up',
'fermented-soybeans',
'cold-tofu',
'egg-roll',
'chilled-noodle',
'stir-fried-beef-and-peppers',
'simmered-pork',
'boiled-chicken-and-vegetables',
'sashimi-bowl',
'sushi-bowl',
'fish-shaped-pancake-with-bean-jam',
'shrimp-with-chill-source',
'roast-chicken',
'steamed-meat-dumpling',
'omelet-with-fried-rice',
'cutlet-curry',
'spaghetti-meat-sauce',
'fried-shrimp',
'potato-salad',
'green-salad',
'macaroni-salad',
'Japanese-tofu-and-vegetable-chowder',
'pork-miso-soup',
'chinese-soup',
'beef-bowl',
'kinpira-style-sauteed-burdock',
'rice-ball',
'pizza-toast',
'dipping-noodles',
'hot-dog',
'french-fries',
'mixed-rice',
'goya-chanpuru',
]

foods_br = [
'arroz',
'enguias sobre arroz',
'pilaf',
'frango com ovo sobre arroz',
'tonkatsu sobre arroz',
'curry de carne bovina',
'sushi',
'arroz com frango',
'arroz frito',
'tempurá sobre arroz',
'bibimbap',
'torrada',
'croissant',
'pãozinho',
'pão com uvas-passas',
'sanduíche de batata frita',
'hambúrguer',
'pizza',
'sanduíches',
'macarrão udon',
'udon com tempurá',
'macarrão soba',
'macarrão ramen',
'macarrão com carne',
'macarrão com tempurá',
'yakisoba',
'espaguete',
'panqueca japonesa',
'takoyaki',
'gratinado',
'legumes salteados',
'croquete',
'berinjela grelhada',
'espinafre salteado',
'tempurá de legumes',
'sopa de missô',
'creme de legumes',
'linguiça',
'oden',
'omelete',
'bolinho de tofu frito',
'guioza',
'ensopado',
'peixe grelhado com teriyaki',
'peixe frito',
'salmão grelhado',
'salmão ao molho meunière',
'sashimi',
'sanma grelhado',
'sukiyaki',
'porco agridoce',
'peixe levemente grelhado',
'pudim de ovo no vapor',
'tempurá',
'frango frito',
'filé empanado',
'peixe marinado ao estilo nanban',
'peixe cozido',
'carne com batatas temperadas',
'hambúrguer japonês',
'bife de carne',
'peixe seco',
'porco salteado com gengibre',
'tofu apimentado',
'espetinho de frango',
'charuto de repolho',
'omelete enrolada',
'ovo frito com gema mole',
'soja fermentada',
'tofu frio',
'rocambole de ovo',
'macarrão frio',
'carne com pimentão salteada',
'porco cozido lentamente',
'frango cozido com legumes',
'tigela de sashimi',
'tigela de sushi',
'panqueca em forma de peixe com feijão',
'camarão ao molho picante',
'frango assado',
'bolinho de carne no vapor',
'omelete com arroz frito',
'curry com filé empanado',
'espaguete à bolonhesa',
'camarão frito',
'salada de batata',
'salada verde',
'salada de macarrão',
'ensopado japonês de tofu com legumes',
'sopa de missô com carne de porco',
'sopa chinesa',
'tigela de carne',
'bardana salteada ao estilo kinpira',
'bolinho de arroz',
'torrada com cobertura de pizza',
'macarrão para mergulhar',
'cachorro-quente',
'batatas fritas',
'arroz misturado',
'refogado de goya com ovo e tofu'
]

@app.route('/api/detect', methods=['POST'])
def detect_food():
    print(f"Request data: {request.data}")
    img_bytes = base64.b64decode(request.data)
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    print("Image received for processing.")

    model = YOLO('assets/best.pt')
    results = model.predict(img, save=False, conf=0.5)
    food_detected = results[0].verbose().split()[1].replace(',', '')

    food_result = foods_br[foods.index(food_detected) - 1]
    print(f"Detected food: {food_result}")

    return make_response(json.dumps({'detected': food_result}, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'})

@app.route('/health-check', methods=['GET'])
def health_check():
    return make_response(json.dumps({'status': 'ok'}), 200, {'Content-Type': 'application/json; charset=utf-8'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 8000))