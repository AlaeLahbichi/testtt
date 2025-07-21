import re
import unicodedata
from nltk.chat.util import reflections , Chat # type: ignore
from django.http import JsonResponse
from difflib import SequenceMatcher
from django.views.decorators.http import require_http_methods

pairs = [
    [r"(bonjour|salut|coucou|hey)", ["Bonjour ! Comment puis-je vous aider aujourd'hui ?", "Salut ! Que puis-je faire pour vous ?"]],
    [r"comment ca va", ["Je suis un chatbot, donc toujours opérationnel ! Et vous, comment allez-vous ?", "Très bien, merci ! Que puis-je faire pour vous ?"]],
    [r"(.*)(age|vieux)", ["Je suis un programme informatique, donc je suis intemporel !"]],
    [r"(.*)(nom|appelles)", ["Je suis ChatBot Django, votre assistant virtuel.", "On m'appelle Botty, ravi de vous aider !"]],
    [r"(.*)(merci beaucoup|thx|mrc)",["Avec plaisir ! N'hésitez pas à poser d'autres questions"]],
    [r"(.*)(au revoir|bye|quit)", ["Au revoir ! N'hésitez pas à revenir si vous avez besoin d'aide.", "À bientôt, prenez soin de vous !"]],
    
    [r".*(changer|modifier).*(mot de passe|password)", [
        "Pour changer votre mot de passe, rendez-vous dans votre profil où vous trouverez un formulaire d'édition.",
        "Vous pouvez modifier votre mot de passe en accédant à la section profil et en utilisant le formulaire prévu à cet effet."
    ]],
    
    [r".*(ajouter|créer).*(nouveau|un).*(projet|project)", [
        "Pour ajouter un nouveau projet, cliquez simplement sur le bouton 'Nouveau' dans la barre de navigation.",
        "La création d'un projet se fait via le bouton 'Nouveau' situé dans la navbar en haut."
    ]],
    
    [r".*(gérer|administrer).*(projets|projects)", [
        "Vous pouvez gérer vos projets directement depuis la page principale ou dans le tableau de bord.",
        "La gestion des projets est accessible depuis la page d'accueil ou via le dashboard pour plus de fonctionnalités."
    ]],
    
    [r".*(gérer|administrer).*(utilisateurs|users)", [
        "La gestion des utilisateurs est réservée à l'administrateur et se trouve dans le tableau de bord.",
        "Pour gérer les utilisateurs, l'administrateur peut accéder à la section dédiée dans le dashboard."
    ]],
    
    [r".*(consulter|voir|afficher).*(graphes|graphiques|statistiques|évolution)", [
        "Les graphiques représentant l'évolution des données sont disponibles dans le tableau de bord.",
        "Pour consulter les statistiques et graphiques, rendez-vous dans le dashboard."
    ]],
    
    [r"(.*)", ["Désolé, je n'ai pas compris votre demande. Pouvez-vous reformuler ?"]]
]


def normalize(text):
    text = text.lower()
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def is_similar(user_input, pattern, threshold=0.7):
    return SequenceMatcher(None, user_input, pattern).ratio() >= threshold

chatbot = Chat(pairs, reflections)

def get_response(user_input):
    user_input_normalized = normalize(user_input)

    response = chatbot.respond(user_input_normalized)
    if response and "Désolé" not in response:
        return response

    for pattern, responses in pairs[:-1]: 
        pattern_clean = normalize(pattern.replace(".*", "").replace("(", "").replace(")", "").replace("|", " "))
        for word in pattern_clean.split():
            if is_similar(user_input_normalized, word):
                return responses[0]

    return pairs[-1][1][0]
