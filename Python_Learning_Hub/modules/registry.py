from modules import module1, module2, module3, module4, module5, module6, module7

ALL_MODULES = [
    module1.MODULE,
    module2.MODULE,
    module3.MODULE,
    module4.MODULE,
    module5.MODULE,
    module6.MODULE,
    module7.MODULE,
]

MODULES_BY_ID = {m["id"]: m for m in ALL_MODULES}


def get_module(module_id):
    return MODULES_BY_ID.get(module_id)


# ==========================================
# FINAL ASSESSMENT
# ==========================================
# A comprehensive, cumulative quiz covering all 7 modules — separate from each
# module's own quiz. Passing this (in addition to completing every module) is
# what unlocks the Final Python Certificate. Uses module_id=0 as the sentinel
# ID for saving/reading this quiz's scores in the quiz_scores table, since
# real modules are numbered 1-7.

FINAL_ASSESSMENT_MODULE_ID = 0
QUESTIONS_PER_MODULE_IN_FINAL = 3


def get_final_assessment_quiz():
    """Builds a cumulative quiz by sampling questions from every module,
    so it stays in sync automatically if module quizzes are ever edited."""
    questions = []
    for module in ALL_MODULES:
        sample = module["quiz"][:QUESTIONS_PER_MODULE_IN_FINAL]
        for q in sample:
            questions.append({**q, "source_module": module["id"]})
    return questions

