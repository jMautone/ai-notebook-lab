"""
Métricas Personalizadas para Evaluación de Respuestas de IA
=============================================================

Este módulo contiene las implementaciones de las 3 métricas personalizadas
del Ejercicio 3 del Lab 8:

- Métrica A: Formalidad del Tono
- Métrica B: Completitud de Respuesta  
- Métrica C: Claridad y Concisión

Cada métrica hereda de DiscreteMetric y retorna un score 0-1.
"""

import re
import string
from ragas.metrics import DiscreteMetric


class FormalidadMetric(DiscreteMetric):
    """
    Métrica A: Formalidad del Tono
    
    Evalúa si la respuesta mantiene un tono formal y profesional.
    Penaliza lenguaje coloquial, emojis, jerga informal y contracciones.
    
    Score: 0-1 (1 = perfectamente formal, 0 = muy informal)
    
    Criterios de evaluación:
    - Presencia de emojis (penalización fuerte: -0.3)
    - Patrones de lenguaje informal (-0.05 por patrón)
    - Contracciones informales (-0.1 por contracción)
    - Exceso de signos de exclamación (-0.1 si >2)
    - Uso incorrecto de mayúsculas (-0.05 por oración)
    - Palabras muy cortas en promedio (-0.1 si avg < 4 letras)
    
    Ejemplo de uso:
        metric = FormalidadMetric()
        score = await metric._ascore({"response": "La respuesta formal..."})
    """
    
    name = "formalidad_tono"
    
    # Patrones informales a detectar
    INFORMAL_PATTERNS = [
        r'\bemoji\b', r'👍', r'😀', r'💪', r'🎯', r'✨', r'🔥',  # Emojis
        r'\bok\b', r'\bokay\b', r'\bgenial\b', r'\bsuper\b', r'\btotal\b',  # Coloquial
        r'\bre\b', r'\bmuy\s+muy\b', r'\bun\s+montón\b',  # Intensificadores informales
        r'¿\w+\?{2,}', r'!{2,}',  # Múltiples signos de puntuación
        r'\bcreo\s+que\b', r'\bpienso\s+que\b',  # Primera persona informal
        r'\bvamos\b', r'\bhey\b', r'\bbueno\b', r'\bpues\b',  # Muletillas
    ]
    
    async def _ascore(self, row: dict, **kwargs) -> float:
        """
        Calcula el score de formalidad para una respuesta.
        
        Args:
            row: Diccionario con clave 'response' conteniendo el texto a evaluar
            **kwargs: Argumentos adicionales (no utilizados)
            
        Returns:
            float: Score entre 0.0 (muy informal) y 1.0 (perfectamente formal)
        """
        response = row.get("response", "")
        
        if not response:
            return 0.0
        
        penalties = 0.0
        
        # 1. Detectar emojis (penalización fuerte)
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticonos
            u"\U0001F300-\U0001F5FF"  # símbolos y pictogramas
            u"\U0001F680-\U0001F6FF"  # transporte y símbolos de mapa
            u"\U0001F1E0-\U0001F1FF"  # banderas
        "]+", flags=re.UNICODE)
        
        if emoji_pattern.search(response):
            penalties += 0.3
        
        # 2. Detectar patrones informales
        for pattern in self.INFORMAL_PATTERNS:
            if re.search(pattern, response, re.IGNORECASE):
                penalties += 0.05
        
        # 3. Detectar contracciones informales en español
        contractions = [r'pa\s', r'\bpa\b', r"q\s", r'\bq\b', r'\bxq\b', r'\bx\b']
        for contraction in contractions:
            if re.search(contraction, response, re.IGNORECASE):
                penalties += 0.1
        
        # 4. Penalizar exceso de signos de exclamación
        exclamation_count = response.count('!')
        if exclamation_count > 2:
            penalties += 0.1
        
        # 5. Verificar uso de mayúsculas al inicio de oraciones
        sentences = re.split(r'[.!?]+', response)
        lowercase_starts = sum(1 for s in sentences if s.strip() and s.strip()[0].islower())
        if lowercase_starts > 0:
            penalties += 0.05 * lowercase_starts
        
        # 6. Detectar lenguaje muy simple (palabras muy cortas en promedio)
        words = response.split()
        if words:
            avg_word_length = sum(len(w.strip(string.punctuation)) for w in words) / len(words)
            if avg_word_length < 4:
                penalties += 0.1
        
        # Calcular score final
        score = max(0.0, 1.0 - penalties)
        return score


class CompletitudMetric(DiscreteMetric):
    """
    Métrica B: Completitud de Respuesta
    
    Evalúa si la respuesta cubre todos los aspectos preguntados.
    Analiza si responde todas las sub-preguntas implícitas.
    
    Score: 0-1 (1 = completamente completa, 0 = incompleta)
    
    Criterios de evaluación:
    - Cobertura de conceptos clave de la pregunta
    - Longitud de respuesta vs complejidad de pregunta
    - Número de oraciones significativas
    - Cobertura de conceptos de la respuesta de referencia
    
    Ejemplo de uso:
        metric = CompletitudMetric()
        score = await metric._ascore({
            "user_input": "¿Qué es...?",
            "response": "Es un proceso...",
            "reference": "Es un proceso que..."
        })
    """
    
    name = "completitud_respuesta"
    
    async def _ascore(self, row: dict, **kwargs) -> float:
        """
        Calcula el score de completitud para una respuesta.
        
        Args:
            row: Diccionario con claves:
                - 'user_input': La pregunta original
                - 'response': La respuesta generada
                - 'reference': La respuesta de referencia (opcional)
            **kwargs: Argumentos adicionales (no utilizados)
            
        Returns:
            float: Score entre 0.0 (incompleta) y 1.0 (completamente completa)
        """
        question = row.get("user_input", "")
        response = row.get("response", "")
        reference = row.get("reference", "")
        
        if not response or not question:
            return 0.0
        
        score = 1.0
        penalties = 0.0
        
        # 1. Detectar preguntas múltiples (usando conectores)
        multi_question_markers = [' y ', '¿', ' o ', ', ']
        sub_questions = 1
        for marker in multi_question_markers:
            sub_questions += question.count(marker)
        
        # 2. Contar conceptos clave en la pregunta
        question_words = re.findall(r'\b\w{4,}\b', question.lower())
        # Filtrar palabras comunes
        stopwords = {'cuál', 'cuáles', 'qué', 'cómo', 'dónde', 'cuándo', 'quién', 'para', 'sobre', 'cual', 'cuales', 'como', 'donde', 'cuando', 'quien'}
        key_concepts = [w for w in question_words if w not in stopwords]
        
        # 3. Verificar cobertura de conceptos clave
        concepts_covered = sum(1 for concept in key_concepts if concept in response.lower())
        if key_concepts:
            coverage_ratio = concepts_covered / len(key_concepts)
            if coverage_ratio < 0.5:
                penalties += 0.3
            elif coverage_ratio < 0.7:
                penalties += 0.15
        
        # 4. Analizar longitud de respuesta vs complejidad de pregunta
        response_words = len(response.split())
        question_words_count = len(question.split())
        
        expected_min_words = question_words_count * 5  # Mínimo esperado
        
        if response_words < expected_min_words:
            penalties += 0.2
        elif response_words < expected_min_words * 1.5:
            penalties += 0.1
        
        # 5. Verificar si hay desarrollo de ideas (múltiples oraciones)
        sentences = re.split(r'[.!?]+', response)
        meaningful_sentences = [s for s in sentences if len(s.split()) > 3]
        
        if len(meaningful_sentences) < 2:
            penalties += 0.2
        elif len(meaningful_sentences) < 3:
            penalties += 0.1
        
        # 6. Comparar con referencia si está disponible
        if reference:
            ref_concepts = re.findall(r'\b\w{5,}\b', reference.lower())
            ref_concepts_unique = set(ref_concepts) - stopwords
            response_lower = response.lower()
            
            ref_coverage = sum(1 for concept in ref_concepts_unique if concept in response_lower)
            if ref_concepts_unique:
                ref_ratio = ref_coverage / len(ref_concepts_unique)
                if ref_ratio < 0.4:
                    penalties += 0.2
                elif ref_ratio < 0.6:
                    penalties += 0.1
        
        score = max(0.0, 1.0 - penalties)
        return score


class ClaridadMetric(DiscreteMetric):
    """
    Métrica C: Claridad y Concisión
    
    Mide si la respuesta es clara, directa y sin redundancias.
    Evalúa complejidad de lectura y estructura gramatical.
    
    Score: 0-1 (1 = perfectamente clara y concisa, 0 = confusa o redundante)
    
    Criterios de evaluación:
    - Diversidad léxica (evitar repeticiones)
    - Longitud de respuesta (penalizar exceso)
    - Complejidad de palabras (promedio de longitud)
    - Longitud de oraciones (ni muy largas ni muy cortas)
    - Repetición de frases (bigramas)
    - Uso de conectores (estructura clara)
    - Uso de paréntesis (puede confundir)
    
    Ejemplo de uso:
        metric = ClaridadMetric()
        score = await metric._ascore({"response": "La respuesta clara..."})
    """
    
    name = "claridad_concision"
    
    async def _ascore(self, row: dict, **kwargs) -> float:
        """
        Calcula el score de claridad y concisión para una respuesta.
        
        Args:
            row: Diccionario con clave 'response' conteniendo el texto a evaluar
            **kwargs: Argumentos adicionales (no utilizados)
            
        Returns:
            float: Score entre 0.0 (confusa/redundante) y 1.0 (clara/concisa)
        """
        response = row.get("response", "")
        
        if not response:
            return 0.0
        
        penalties = 0.0
        
        # 1. Analizar redundancia (diversidad léxica)
        words = [w.lower().strip(string.punctuation) for w in response.split() if w.strip()]
        if len(words) > 0:
            unique_words = set(words)
            lexical_diversity = len(unique_words) / len(words)
            
            # Penalizar baja diversidad léxica (muchas repeticiones)
            if lexical_diversity < 0.5:
                penalties += 0.3
            elif lexical_diversity < 0.65:
                penalties += 0.15
        
        # 2. Penalizar respuestas excesivamente largas
        if len(response) > 600:
            penalties += 0.2
        elif len(response) > 450:
            penalties += 0.1
        
        # 3. Analizar complejidad de palabras
        if words:
            avg_word_length = sum(len(w) for w in words) / len(words)
            # Penalizar palabras promedio muy largas (difícil de leer)
            if avg_word_length > 7:
                penalties += 0.2
            elif avg_word_length > 6:
                penalties += 0.1
        
        # 4. Analizar longitud de oraciones
        sentences = [s.strip() for s in re.split(r'[.!?]+', response) if s.strip()]
        if sentences:
            sentence_lengths = [len(s.split()) for s in sentences]
            avg_sentence_length = sum(sentence_lengths) / len(sentences)
            
            # Penalizar oraciones muy largas (difíciles de seguir)
            if avg_sentence_length > 30:
                penalties += 0.2
            elif avg_sentence_length > 22:
                penalties += 0.1
            
            # Penalizar oraciones muy cortas (puede ser demasiado telegráfico)
            if avg_sentence_length < 8:
                penalties += 0.1
        
        # 5. Detectar repeticiones de frases
        bigrams = [' '.join(words[i:i+2]) for i in range(len(words)-1)]
        if bigrams:
            unique_bigrams = len(set(bigrams))
            bigram_diversity = unique_bigrams / len(bigrams)
            if bigram_diversity < 0.8:
                penalties += 0.15
        
        # 6. Detectar conectores y fluidez
        connectors = ['además', 'sin embargo', 'por lo tanto', 'asimismo', 'mientras', 
                     'aunque', 'porque', 'ya que', 'debido a', 'en consecuencia']
        connector_count = sum(1 for conn in connectors if conn in response.lower())
        
        # Buena señal si hay algunos conectores (estructura clara)
        if connector_count >= 1 and connector_count <= 3:
            penalties -= 0.05  # Bonus por buena estructura
        elif connector_count > 5:
            penalties += 0.1  # Penalizar exceso de conectores
        
        # 7. Penalizar uso excesivo de paréntesis (puede confundir)
        parenthesis_count = response.count('(') + response.count(')')
        if parenthesis_count > 4:
            penalties += 0.1
        
        score = max(0.0, min(1.0, 1.0 - penalties))
        return score
