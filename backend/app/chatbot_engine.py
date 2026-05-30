import re
from typing import List, Dict, Optional

class ChatbotEngine:
    def __init__(self, bot_name: str, personality: str, products: List[Dict] = None):
        self.name = bot_name
        self.personality = personality
        self.products = products or []
        self.conversation_context = []
    
    def detect_intent(self, message: str) -> str:
        msg = message.lower()
        
        if any(w in msg for w in ["hola", "buenos", "saludos", "hey", "buenas"]):
            return "greeting"
        
        if any(w in msg for w in ["lista", "autos", "productos", "catálogo", "catalogo", "disponibles", "tienes", "muestrame", "ver"]):
            return "list_products"
        
        if re.search(r"(opci[oó]n|numero|n[uú]mero|la)\s*(\d+)", msg):
            return "product_detail"
        
        if any(w in msg for w in ["precio", "cuesta", "vale", "valor", "cuánto", "cuanto"]):
            return "price_inquiry"
        
        if any(w in msg for w in ["gracias", "adiós", "adios", "chao", "bye"]):
            return "goodbye"
        
        if any(w in msg for w in ["ayuda", "help", "ayudame", "info"]):
            return "help"
        
        return "general"
    
    def get_product_list(self) -> str:
        if not self.products:
            return "Lo siento, no tengo productos disponibles en este momento."
        
        response = "¡Claro! Estos son nuestros productos disponibles:\n\n"
        for i, p in enumerate(self.products, 1):
            response += f"**{i}. {p['name']}**\n"
            response += f"   💰 Precio: ${p.get('price', 0):,}\n"
            if p.get('description'):
                response += f"   📝 {p['description']}\n"
            response += "\n"
        
        self.conversation_context.append({
            "type": "product_list",
            "products": self.products
        })
        
        response += "¿Te interesa alguno en particular? Puedes decirme el número."
        return response
    
    def get_product_by_option(self, message: str) -> str:
        match = re.search(r"(opci[oó]n|numero|n[uú]mero|la)\s*(\d+)", message.lower())
        if not match:
            return "¿A qué producto te refieres? Puedes decirme el número de la lista."
        
        option_num = int(match.group(2))
        
        if self.conversation_context and self.conversation_context[-1]["type"] == "product_list":
            products = self.conversation_context[-1]["products"]
            if 1 <= option_num <= len(products):
                p = products[option_num - 1]
                response = f"**{p['name']}**\n\n"
                response += f"💰 Precio: ${p.get('price', 0):,}\n"
                if p.get('description'):
                    response += f"📝 {p['description']}\n"
                response += "\n¿Te gustaría más información sobre este producto?"
                return response
            else:
                return f"Solo tengo {len(products)} productos. Elige un número del 1 al {len(products)}."
        else:
            return "Primero necesitas pedirme la lista de productos. Di 'lista de autos' o 'productos disponibles'."
    
    def generate_response(self, message: str, history: List[Dict] = None) -> str:
        intent = self.detect_intent(message)
        
        if history:
            for h in history:
                if h.get("role") == "assistant" and "productos disponibles" in h.get("content", "").lower():
                    self.conversation_context.append({
                        "type": "product_list",
                        "products": self.products
                    })
        
        if intent == "greeting":
            return f"¡Hola! Soy {self.name}. {self.personality} ¿En qué puedo ayudarte hoy?"
        
        elif intent == "list_products":
            return self.get_product_list()
        
        elif intent == "product_detail":
            return self.get_product_by_option(message)
        
        elif intent == "price_inquiry":
            return "Para darte el precio exacto, dime ¿qué producto te interesa? Puedes ver la lista diciendo 'lista de autos'."
        
        elif intent == "help":
            return "Puedo ayudarte con:\n- Lista de productos\n- Precios\n- Información de cada producto\n\n¿Qué necesitas?"
        
        elif intent == "goodbye":
            return "¡Gracias por tu visita! Estoy aquí cuando me necesites. ¡Hasta luego!"
        
        else:
            return f"¿En qué más puedo ayudarte? Puedo mostrarte nuestra lista de productos o darte información específica."
