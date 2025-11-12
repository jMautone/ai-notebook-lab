"""
Herramientas para generación de datos de muestra.
"""

import random
import string
from typing import Any


class DataGenerationTools:
    """Herramientas para generar datos de muestra para testing."""
    
    @staticmethod
    def generate_sample_data(data_type: str, count: int) -> dict[str, Any]:
        """
        Genera datos de muestra para testing.
        
        Args:
            data_type: Tipo de datos ('names', 'emails', 'urls', 'numbers')
            count: Cantidad de elementos a generar
            
        Returns:
            Diccionario con los datos generados
        """
        data_type = data_type.lower()
        count = max(1, min(count, 1000))  # Limitar a 1000 items
        
        if data_type == "names":
            names = ["Juan", "María", "Carlos", "Ana", "Diego", "Laura", 
                     "Pedro", "Sofia", "Miguel", "Elena", "Roberto", "Carmen",
                     "Francisco", "Isabel", "Jorge", "Rosa"]
            items = [random.choice(names) for _ in range(count)]
        
        elif data_type == "emails":
            domains = ["gmail.com", "yahoo.com", "outlook.com", "example.com",
                      "test.com", "sample.org", "demo.net"]
            items = [
                f"user{i}{random.choice(string.ascii_lowercase)}@{random.choice(domains)}"
                for i in range(count)
            ]
        
        elif data_type == "urls":
            protocols = ["http://", "https://"]
            domains = ["example.com", "test.com", "demo.org", "sample.net", 
                      "website.com", "app.io"]
            paths = ["page", "api", "data", "resource", "service", "home"]
            items = [
                f"{random.choice(protocols)}www.{random.choice(domains)}/{random.choice(paths)}"
                for _ in range(count)
            ]
        
        elif data_type == "numbers":
            items = [random.randint(1, 1000) for _ in range(count)]
        
        else:
            return {
                "success": False,
                "error": f"Tipo de dato no soportado: {data_type}. "
                        "Use: names, emails, urls, numbers"
            }
        
        return {
            "success": True,
            "data_type": data_type,
            "items": items,
            "count": len(items)
        }
    
    @staticmethod
    def generate_random_string(length: int = 10, charset: str = "ascii") -> dict[str, Any]:
        """
        Genera una cadena aleatoria.
        
        Args:
            length: Longitud de la cadena
            charset: Tipo de caracteres ('ascii', 'digits', 'hex', 'alphanumeric')
            
        Returns:
            Diccionario con la cadena generada
        """
        length = max(1, min(length, 1000))
        
        if charset == "digits":
            chars = string.digits
        elif charset == "hex":
            chars = string.hexdigits
        elif charset == "alphanumeric":
            chars = string.ascii_letters + string.digits
        else:  # ascii
            chars = string.ascii_letters
        
        result = ''.join(random.choice(chars) for _ in range(length))
        
        return {
            "string": result,
            "length": length,
            "charset": charset
        }
    
    @staticmethod
    def generate_random_passwords(count: int = 5, length: int = 12) -> dict[str, Any]:
        """
        Genera contraseñas aleatorias.
        
        Args:
            count: Cantidad de contraseñas
            length: Longitud de cada contraseña
            
        Returns:
            Diccionario con las contraseñas generadas
        """
        count = max(1, min(count, 100))
        length = max(8, min(length, 128))
        
        chars = string.ascii_letters + string.digits + string.punctuation
        passwords = [
            ''.join(random.choice(chars) for _ in range(length))
            for _ in range(count)
        ]
        
        return {
            "passwords": passwords,
            "count": count,
            "length": length
        }
