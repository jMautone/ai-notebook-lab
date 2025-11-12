"""
Herramientas de procesamiento de texto.
"""

from typing import Any


class TextTools:
    """Herramientas para procesamiento y análisis de texto."""
    
    @staticmethod
    def analyze_text(text: str) -> dict[str, Any]:
        """
        Analiza un texto y devuelve estadísticas.
        
        Args:
            text: Texto a analizar
            
        Returns:
            Diccionario con estadísticas del texto
        """
        lines = text.split('\n')
        words = text.split()
        
        avg_word_length = (
            sum(len(word) for word in words) / len(words)
            if words else 0
        )
        
        return {
            "character_count": len(text),
            "word_count": len(words),
            "line_count": len(lines),
            "average_word_length": round(avg_word_length, 2)
        }
    
    @staticmethod
    def convert_text(text: str, format: str) -> dict[str, Any]:
        """
        Convierte texto entre diferentes formatos.
        
        Args:
            text: Texto a convertir
            format: Formato destino ('uppercase', 'lowercase', 'title', 'reverse')
            
        Returns:
            Diccionario con el texto convertido
        """
        format = format.lower()
        
        if format == "uppercase":
            converted = text.upper()
        elif format == "lowercase":
            converted = text.lower()
        elif format == "title":
            converted = text.title()
        elif format == "reverse":
            converted = text[::-1]
        else:
            raise ValueError(
                f"Formato no soportado: {format}. "
                "Use: uppercase, lowercase, title, reverse"
            )
        
        return {
            "original": text,
            "converted": converted,
            "format_used": format
        }
    
    @staticmethod
    def count_character(text: str, character: str) -> dict[str, Any]:
        """
        Cuenta las ocurrencias de un carácter en un texto.
        
        Args:
            text: Texto a analizar
            character: Carácter a contar
            
        Returns:
            Diccionario con el conteo
        """
        count = text.lower().count(character.lower())
        
        return {
            "text": text,
            "character": character,
            "count": count,
            "percentage": round(
                (count / len(text) * 100) if text else 0,
                2
            )
        }
    
    @staticmethod
    def find_longest_word(text: str) -> dict[str, Any]:
        """
        Encuentra la palabra más larga en un texto.
        
        Args:
            text: Texto a analizar
            
        Returns:
            Diccionario con la palabra más larga
        """
        words = text.split()
        
        if not words:
            return {"error": "No hay palabras en el texto"}
        
        longest = max(words, key=len)
        
        return {
            "text": text,
            "longest_word": longest,
            "length": len(longest),
            "word_count": len(words)
        }
    
    @staticmethod
    def reverse_words(text: str) -> dict[str, Any]:
        """
        Invierte el orden de las palabras en un texto.
        
        Args:
            text: Texto a procesar
            
        Returns:
            Diccionario con el texto procesado
        """
        words = text.split()
        reversed_text = ' '.join(reversed(words))
        
        return {
            "original": text,
            "reversed": reversed_text
        }
