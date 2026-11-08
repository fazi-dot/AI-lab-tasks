# Task 1
def rule_check(score, complete, gpa, income):
    failed = []
    
    if complete == False:
        failed.append("incomplete_docs")
    if score < 70:
        failed.append("score_below_70")
    if gpa < 2.5:
        failed.append("gpa_below_2.5")
    if income > 50000:
        failed.append("income_above_50000")
        
    if len(failed) > 0:
        return "Hold", failed
    else:
        return "Review", ["all_passed"]


tests = [
    ("T1_pass", 82, True, 3.4, 35000, "Review"),
    ("T2_fail_gpa", 80, True, 2.1, 30000, "Hold"),
    ("T3_fail_income", 85, True, 3.2, 72000, "Hold"),
    ("T4_boundary", 70, True, 2.5, 50000, "Review")
]

passed = 0
for name, s, comp, g, inc, exp in tests:
    actual, reason = rule_check(s, comp, g, inc)
    if actual == exp:
        passed = passed + 1
    print(name, "| Expected:", exp, "| Actual:", actual, "| Reason:", reason)

print("\nPassed:", passed, "out of", len(tests))

print("Edge case (high score, incomplete docs):")
print(rule_check(91, False, 3.8, 20000))

 # Task 2
def symbolic(score, complete):
    if complete == True and score >= 70:
        return "Review"
    else:
        return "Hold"

def threshold(probability):
    if probability >= 0.70:
        return "Review"
    else:
        return "Hold"


cases = [
    ("complete_high", 82, True, 0.81),
    ("complete_low", 68, True, 0.74),
    ("incomplete_high", 91, False, 0.88),
    ("boundary", 70, True, 0.70)
]

print("Case | Symbolic | Threshold | Disagreement")
for name, s, comp, prob in cases:
    res1 = symbolic(s, comp)
    res2 = threshold(prob)
    disagree = (res1 != res2)
    print(name, "|", res1, "|", res2, "|", disagree)


print("\nBoundary checks:")
variants = [
    ("score_69_prob_0.70", 69, True, 0.70),
    ("score_70_prob_0.69", 70, True, 0.69)
]

for name, s, comp, prob in variants:
    res1 = symbolic(s, comp)
    res2 = threshold(prob)
    disagree = (res1 != res2)
    print(name, "|", res1, "|", res2, "|", disagree)