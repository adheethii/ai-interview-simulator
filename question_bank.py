"""
Role-specific question topics for the interview simulator
"""

QUESTION_TOPICS = {
    "ML Engineer": {
        "Easy": [
            "supervised vs unsupervised learning",
            "overfitting and underfitting",
            "train test split",
            "feature scaling",
            "confusion matrix",
            "accuracy vs precision vs recall",
            "what is cross validation",
            "what is a decision tree",
        ],
        "Medium": [
            "bagging vs boosting",
            "random forest algorithm",
            "gradient descent variants",
            "regularization L1 vs L2",
            "ROC AUC curve",
            "handling imbalanced datasets",
            "feature engineering techniques",
            "hyperparameter tuning methods",
            "bias variance tradeoff",
        ],
        "Hard": [
            "design a fraud detection system",
            "XGBoost internal workings",
            "model deployment at scale",
            "feature store design",
            "model monitoring and drift detection",
            "ensemble methods deep dive",
            "neural network optimization",
        ]
    },
    "Data Scientist": {
        "Easy": [
            "what is EDA",
            "types of data",
            "mean median mode",
            "what is correlation",
            "normal distribution",
            "what is hypothesis testing",
            "p-value explained",
        ],
        "Medium": [
            "A/B testing design",
            "statistical significance",
            "time series forecasting",
            "dimensionality reduction PCA",
            "clustering algorithms",
            "SQL window functions",
            "data cleaning strategies",
            "outlier detection methods",
        ],
        "Hard": [
            "design a recommendation system",
            "causal inference",
            "survival analysis",
            "Bayesian statistics",
            "design an experiment for a new feature",
            "multi-armed bandit problem",
        ]
    },
    "AI Engineer": {
        "Easy": [
            "what is an LLM",
            "what is prompt engineering",
            "what is RAG",
            "zero shot vs few shot",
            "what is a vector embedding",
            "what is FAISS",
            "what is LangChain",
        ],
        "Medium": [
            "RAG vs fine tuning tradeoffs",
            "chain of thought prompting",
            "LangChain agents and tools",
            "vector database comparison",
            "chunking strategies for RAG",
            "hallucination prevention",
            "prompt injection attacks",
            "ReAct prompting pattern",
        ],
        "Hard": [
            "design an enterprise RAG system",
            "multi-agent workflow design",
            "LLM evaluation strategies",
            "fine tuning vs RLHF",
            "production LLM deployment",
            "LangGraph multi-agent architecture",
            "RAG evaluation metrics",
        ]
    },
    "Data Analyst": {
        "Easy": [
            "SQL SELECT basics",
            "what is a dashboard",
            "Excel vs SQL",
            "types of charts",
            "what is KPI",
            "data cleaning in Excel",
        ],
        "Medium": [
            "SQL JOINs explained",
            "Power BI DAX basics",
            "data storytelling",
            "cohort analysis",
            "funnel analysis",
            "SQL window functions",
            "data modeling star schema",
        ],
        "Hard": [
            "design a business intelligence system",
            "advanced DAX patterns",
            "real-time analytics architecture",
            "data governance",
            "designing KPI frameworks",
        ]
    }
}

DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]
ROLES = list(QUESTION_TOPICS.keys())
