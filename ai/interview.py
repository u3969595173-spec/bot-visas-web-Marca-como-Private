import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class InterviewSimulator:
    """AI-powered interview simulator for visa consulate"""
    
    # Common interview questions
    QUESTIONS = [
        "¿Por qué quieres estudiar en España?",
        "¿Por qué elegiste esta universidad específicamente?",
        "¿Cómo financiarás tus estudios?",
        "¿Planeas regresar a tu país al terminar tus estudios?",
        "¿Qué harás después de graduarte?",
        "¿Por qué este programa de estudios específicamente?",
        "¿Tienes familia o amigos en España?",
        "¿Cómo te mantendrás económicamente durante tu estancia?",
        "¿Dónde vivirás en España?",
        "¿Qué nivel de español tienes?",
        "¿Has estado en España antes?",
        "¿Por qué no estudias esto en tu país?",
        "¿Qué vas a aportar a la universidad?",
        "¿Cuáles son tus planes a largo plazo?",
        "¿Cómo te enteraste de esta universidad?"
    ]
    
    @staticmethod
    def get_random_question():
        """Get a random interview question"""
        import random
        return random.choice(InterviewSimulator.QUESTIONS)
    
    @staticmethod
    def evaluate_answer(question: str, user_answer: str, context: dict = None) -> dict:
        """
        Evaluate user's answer using AI
        
        Args:
            question: The question asked
            user_answer: User's response
            context: Optional context about the user's application
            
        Returns:
            dict with score, problems, and improved answer
        """
        # Build context for AI
        context_str = ""
        if context:
            context_str = f"""
Contexto del estudiante:
- País: {context.get('country_origin', 'N/A')}
- Universidad: {context.get('university', 'N/A')}
- Programa: {context.get('study_type', 'N/A')}
- Duración: {context.get('duration_months', 'N/A')} meses
"""
        
        prompt = f"""Eres un experto en entrevistas de visa de estudiante para España. 
Evalúa la siguiente respuesta en una escala del 1 al 10.

{context_str}

Pregunta del consulado: "{question}"
Respuesta del estudiante: "{user_answer}"

Por favor proporciona:
1. Puntuación (1-10)
2. Problemas específicos con la respuesta
3. Una respuesta mejorada que sería ideal

Formato de respuesta:
PUNTUACION: [número]
PROBLEMAS:
- [problema 1]
- [problema 2]
RESPUESTA_MEJORADA:
[respuesta ideal]
"""
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Eres un experto en visas de estudiante para España. Evalúas respuestas de entrevistas y proporcionas feedback constructivo."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            
            # Parse the response
            lines = content.strip().split('\n')
            score = 5
            problems = []
            improved_answer = ""
            
            current_section = None
            for line in lines:
                if line.startswith('PUNTUACION:'):
                    try:
                        score = int(line.split(':')[1].strip())
                    except:
                        score = 5
                elif line.startswith('PROBLEMAS:'):
                    current_section = 'problems'
                elif line.startswith('RESPUESTA_MEJORADA:'):
                    current_section = 'improved'
                elif current_section == 'problems' and line.strip().startswith('-'):
                    problems.append(line.strip()[1:].strip())
                elif current_section == 'improved':
                    improved_answer += line.strip() + ' '
            
            status = '🔴 DÉBIL' if score <= 3 else ('🟡 REGULAR' if score <= 6 else ('🟢 BUENA' if score <= 8 else '🟢 EXCELENTE'))
            
            return {
                'score': score,
                'status': status,
                'problems': problems if problems else ['Respuesta muy genérica, falta especificidad'],
                'improved_answer': improved_answer.strip() if improved_answer else 'Agrega detalles específicos sobre tu programa, universidad y motivaciones.',
                'formatted_feedback': InterviewSimulator._format_feedback(
                    question, user_answer, score, status, problems, improved_answer.strip()
                )
            }
            
        except Exception as e:
            print(f"Error evaluating answer: {e}")
            # Fallback to basic evaluation
            return InterviewSimulator._basic_evaluation(question, user_answer)
    
    @staticmethod
    def _basic_evaluation(question: str, user_answer: str) -> dict:
        """Basic evaluation without AI (fallback)"""
        answer_length = len(user_answer.split())
        
        if answer_length < 10:
            score = 3
            status = '🔴 MUY CORTA'
            problems = ['Respuesta demasiado corta', 'Falta de detalles']
            improved = 'Proporciona más detalles específicos sobre tu situación, motivaciones y planes.'
        elif answer_length < 30:
            score = 5
            status = '🟡 PUEDE MEJORAR'
            problems = ['Agrega más detalles específicos', 'Menciona aspectos únicos de tu caso']
            improved = 'Expande tu respuesta con ejemplos concretos y detalles sobre el programa y universidad.'
        else:
            score = 7
            status = '🟢 BIEN'
            problems = ['Revisa que sea clara y directa']
            improved = 'Asegúrate de ser específico y mencionar detalles clave.'
        
        return {
            'score': score,
            'status': status,
            'problems': problems,
            'improved_answer': improved,
            'formatted_feedback': InterviewSimulator._format_feedback(
                question, user_answer, score, status, problems, improved
            )
        }
    
    @staticmethod
    def _format_feedback(question, user_answer, score, status, problems, improved):
        """Format feedback for display"""
        feedback = f"""
🎤 **PREGUNTA:** {question}

👤 **TU RESPUESTA:**
"{user_answer}"

━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **EVALUACIÓN:** {status} ({score}/10)

⚠️ **Problemas detectados:**
"""
        for problem in problems:
            feedback += f"• {problem}\n"
        
        feedback += f"""
💡 **RESPUESTA MEJORADA:**
"{improved}"

━━━━━━━━━━━━━━━━━━━━━━━━━━━

💪 Practica más veces para mejorar tu puntuación!
"""
        return feedback
