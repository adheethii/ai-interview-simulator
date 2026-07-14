"""
Core interview logic — question generation and answer evaluation
"""

import json
import re
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from prompts import QUESTION_GENERATOR_PROMPT, ANSWER_EVALUATOR_PROMPT, FINAL_REPORT_PROMPT


def get_llm(model="llama3.2:1b", temperature=0.7):
    return OllamaLLM(model=model, temperature=temperature)


def generate_question(role, difficulty, covered_topics, question_num, total_questions):
    """Generate the next interview question"""
    llm = get_llm(temperature=0.8)
    prompt = PromptTemplate(
        input_variables=["role", "difficulty", "covered_topics", "question_num", "total_questions"],
        template=QUESTION_GENERATOR_PROMPT
    )
    chain = prompt | llm
    question = chain.invoke({
        "role": role,
        "difficulty": difficulty,
        "covered_topics": ", ".join(covered_topics) if covered_topics else "None yet",
        "question_num": question_num,
        "total_questions": total_questions
    })
    return question.strip()


def evaluate_answer(role, question, answer):
    """Evaluate the candidate's answer and return score + feedback"""
    llm = get_llm(temperature=0.3)  # low temp for consistent evaluation
    prompt = PromptTemplate(
        input_variables=["role", "question", "answer"],
        template=ANSWER_EVALUATOR_PROMPT
    )
    chain = prompt | llm
    response = chain.invoke({
        "role": role,
        "question": question,
        "answer": answer
    })

    # Parse JSON response
    try:
        # Clean response — remove any text before/after JSON
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return result
    except (json.JSONDecodeError, AttributeError):
        pass

    # Fallback if JSON parsing fails
    return {
        "score": 5,
        "verdict": "Average",
        "strengths": ["Answer provided"],
        "improvements": ["Try to be more specific"],
        "ideal_answer_hint": "Focus on key concepts with examples"
    }


def generate_final_report(role, difficulty, questions, answers, scores):
    """Generate final performance report"""
    llm = get_llm(temperature=0.5)
    prompt = PromptTemplate(
        input_variables=["role", "difficulty", "total_questions", "avg_score", "qa_summary"],
        template=FINAL_REPORT_PROMPT
    )
    chain = prompt | llm

    avg_score = sum(scores) / len(scores) if scores else 0
    qa_summary = "\n".join([
        f"Q{i+1}: {q[:80]}... → Score: {s}/10"
        for i, (q, s) in enumerate(zip(questions, scores))
    ])

    response = chain.invoke({
        "role": role,
        "difficulty": difficulty,
        "total_questions": len(questions),
        "avg_score": round(avg_score, 1),
        "qa_summary": qa_summary
    })

    try:
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except (json.JSONDecodeError, AttributeError):
        pass

    return {
        "overall_grade": "B",
        "performance_summary": f"Completed {len(questions)} questions with an average score of {round(avg_score, 1)}/10.",
        "top_strengths": ["Completed the interview", "Provided answers to all questions"],
        "areas_to_improve": ["Review core concepts", "Practice with more examples"],
        "study_recommendations": ["Review ML fundamentals", "Practice explaining concepts clearly"],
        "interview_readiness": "Almost Ready",
        "encouragement": "Keep practising — you're on the right track!"
    }
