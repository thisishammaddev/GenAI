"""Curated questions and concept guides for the learning agent."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Question:
    id: str
    concept: str
    prompt: str
    options: tuple[str, str, str, str]
    answer: int
    wrong_reasons: dict[int, str]


TRACKS: dict[str, dict] = {
    "Python Basics": {
        "subtitle": "Variables, identity, loops, and functions",
        "questions": [
            Question("py1", "Equality vs identity", "What does `a == b` check?", ("Whether values are equal", "Whether both names point to the same object", "Whether types match", "Whether both objects are mutable"), 0, {1: "Confuses value equality with object identity", 2: "Assumes equality only checks types", 3: "Confuses comparison with mutability"}),
            Question("py2", "Equality vs identity", "Two separate lists contain `[1, 2]`. Which expression is reliably `True`?", ("list_a is list_b", "list_a == list_b", "id(list_a) == id(list_b)", "list_a is [1, 2]"), 1, {0: "Confuses equal contents with same object", 2: "Assumes separate objects share an identity", 3: "Assumes a new list literal is the original object"}),
            Question("py3", "Loop boundaries", "What does `list(range(2, 5))` produce?", ("[2, 3, 4, 5]", "[0, 1, 2, 3, 4]", "[2, 3, 4]", "[3, 4, 5]"), 2, {0: "Assumes the stop value is included", 1: "Assumes range always starts at zero", 3: "Assumes the start value is excluded"}),
            Question("py4", "Function return values", "What does a Python function return if it has no `return` statement?", ("0", "False", "An empty string", "None"), 3, {0: "Assumes a numeric default return", 1: "Confuses falsy values with None", 2: "Assumes a string default return"}),
            Question("py5", "Equality vs identity", "If `b = a`, what does `a is b` evaluate to?", ("True", "False", "Only true for strings", "Only true for numbers"), 0, {1: "Misses that assignment shares the same object", 2: "Assumes identity only works for strings", 3: "Assumes identity only works for numbers"}),
            Question("py6", "Loop boundaries", "What does `list(range(5, 2, -1))` produce?", ("[5, 4, 3, 2]", "[5, 4, 3]", "[4, 3, 2]", "[2, 3, 4, 5]"), 1, {0: "Includes the exclusive stop value", 2: "Excludes the start value", 3: "Ignores the negative step"}),
            Question("py7", "Function return values", "A function calls `print('Hi')` but has no `return`. What value does calling it return?", ("'Hi'", "True", "None", "An empty string"), 2, {0: "Confuses printed output with returned value", 1: "Assumes printing returns success", 3: "Assumes an empty string is returned"}),
            Question("py8", "Loop boundaries", "How many values are in `range(1, 10, 3)`?", ("2", "4", "10", "3"), 3, {0: "Stops one step too early", 1: "Includes the exclusive stop value as another step", 2: "Confuses stop with number of values"}),
        ],
    },
    "SQL Essentials": {
        "subtitle": "Filtering, joins, and aggregation",
        "questions": [
            Question("sql1", "WHERE vs HAVING", "Which clause filters groups after `GROUP BY`?", ("WHERE", "HAVING", "ORDER BY", "LIMIT"), 1, {0: "Confuses row filtering with group filtering", 2: "Confuses sorting with filtering", 3: "Confuses limiting output with filtering groups"}),
            Question("sql2", "WHERE vs HAVING", "To keep only orders with `amount > 100` before grouping, use:", ("WHERE amount > 100", "HAVING amount > 100", "ORDER BY amount > 100", "GROUP BY amount > 100"), 0, {1: "Uses HAVING for a row-level condition", 2: "Uses sorting in place of filtering", 3: "Uses grouping in place of filtering"}),
            Question("sql3", "JOIN behavior", "Which join keeps every row from the left table?", ("INNER JOIN", "RIGHT JOIN", "LEFT JOIN", "CROSS JOIN"), 2, {0: "Assumes INNER JOIN keeps unmatched left rows", 1: "Reverses left and right join behavior", 3: "Confuses a Cartesian product with a left join"}),
            Question("sql4", "COUNT and NULL", "What does `COUNT(column_name)` exclude?", ("Duplicate values", "Zero values", "Empty strings", "NULL values"), 3, {0: "Confuses COUNT with COUNT DISTINCT", 1: "Assumes zero is missing", 2: "Assumes empty strings are NULL"}),
            Question("sql5", "WHERE vs HAVING", "Which clause can filter groups where `SUM(amount) > 500`?", ("HAVING", "WHERE", "ORDER BY", "LIMIT"), 0, {1: "Tries to filter an aggregate before grouping", 2: "Confuses ordering with group filtering", 3: "Confuses row limits with group filtering"}),
            Question("sql6", "JOIN behavior", "Which join returns only rows with matches in both tables?", ("LEFT JOIN", "INNER JOIN", "CROSS JOIN", "FULL OUTER JOIN"), 1, {0: "Includes unmatched left-side rows", 2: "Creates combinations instead of matching rows", 3: "Includes unmatched rows from both sides"}),
            Question("sql7", "COUNT and NULL", "A table has three rows, including one with a NULL email. What does `COUNT(*)` return?", ("0", "2", "3", "NULL"), 2, {0: "Assumes NULL prevents counting rows", 1: "Confuses COUNT(*) with COUNT(email)", 3: "Assumes an aggregate returns NULL because a row contains NULL"}),
            Question("sql8", "JOIN behavior", "In a LEFT JOIN, what appears in right-table columns when no match exists?", ("Zero", "An empty string", "The left-table value", "NULL"), 3, {0: "Assumes a numeric default for unmatched data", 1: "Assumes an empty-string default", 2: "Assumes left values are copied to the right"}),
        ],
    },
    "Machine Learning": {
        "subtitle": "Data leakage, evaluation, and model fit",
        "questions": [
            Question("ml1", "Train-test leakage", "When should a scaler be fitted in a train/test workflow?", ("On all data before splitting", "On training data only", "On test data only", "Separately on training and test data"), 1, {0: "Lets test data influence preprocessing", 2: "Fits preprocessing without training data", 3: "Uses inconsistent scaling between splits"}),
            Question("ml2", "Train-test leakage", "A model feature contains information recorded after the predicted event. What is this?", ("Regularization", "Class imbalance", "Data leakage", "Cross-validation"), 2, {0: "Confuses leakage with regularization", 1: "Confuses leakage with uneven class counts", 3: "Confuses leakage with evaluation design"}),
            Question("ml3", "Precision vs recall", "For a rare disease screen where missing cases is costly, which metric deserves special attention?", ("Recall", "Precision", "R-squared", "Training loss"), 0, {1: "Prioritizes false positives over missed cases", 2: "Uses a regression metric for classification", 3: "Uses training loss instead of missed-case performance"}),
            Question("ml4", "Overfitting", "Training accuracy is 99%, test accuracy is 61%. Most likely issue?", ("Underfitting", "Perfect generalization", "Data normalization", "Overfitting"), 3, {0: "Confuses weak learning with poor generalization", 1: "Ignores the train-test performance gap", 2: "Assumes normalization explains the gap"}),
            Question("ml5", "Train-test leakage", "You fill missing values using the mean of the full dataset before splitting. What is the problem?", ("It always causes underfitting", "Test data influences preprocessing", "It removes the target column", "There is no problem"), 1, {0: "Confuses leakage with underfitting", 2: "Assumes imputation changes the target", 3: "Misses test information leaking into training"}),
            Question("ml6", "Precision vs recall", "A classifier finds 8 of 16 actual positive cases. What is its recall?", ("25%", "80%", "50%", "100%"), 2, {0: "Divides by the wrong number of actual positives", 1: "Confuses recall with another proportion", 3: "Ignores the eight missed cases"}),
            Question("ml7", "Overfitting", "Which result most strongly suggests overfitting?", ("High training score, much lower test score", "Low training score, similarly low test score", "Equal high training and test scores", "A smaller dataset file"), 0, {1: "Confuses underfitting with overfitting", 2: "Confuses generalization with overfitting", 3: "Uses file size instead of model performance"}),
            Question("ml8", "Precision vs recall", "A classifier predicts 10 positive cases and 8 are correct. What is its precision?", ("50%", "80%", "20%", "100%"), 1, {0: "Uses the wrong denominator for predicted positives", 2: "Counts incorrect predictions rather than correct predictions", 3: "Ignores the two false positives"}),
        ],
    },
}


PRACTICE: dict[str, Question] = {
    "Equality vs identity": Question("p_py1", "Equality vs identity", "Which operator asks whether two variables refer to the same object?", ("==", "is", "!=", "in"), 1, {0: "Still comparing values rather than identity", 2: "Checks value inequality", 3: "Checks membership"}),
    "Loop boundaries": Question("p_py2", "Loop boundaries", "What is the final number in `list(range(3, 7))`?", ("3", "5", "6", "7"), 2, {0: "Selected the start value", 1: "Stopped one value too early", 3: "Included the exclusive stop value"}),
    "Function return values": Question("p_py3", "Function return values", "What is printed by `print(type(no_return()))` if `no_return` has no return statement?", ("<class 'NoneType'>", "<class 'bool'>", "<class 'int'>", "An error"), 0, {1: "Confuses None with False", 2: "Assumes a numeric return", 3: "Assumes implicit None causes an error"}),
    "WHERE vs HAVING": Question("p_sql1", "WHERE vs HAVING", "Which clause should filter departments with `COUNT(*) > 5`?", ("WHERE", "HAVING", "LIMIT", "ORDER BY"), 1, {0: "Applies aggregate filtering before grouping", 2: "Limits rows instead of filtering groups", 3: "Sorts groups instead of filtering them"}),
    "JOIN behavior": Question("p_sql2", "JOIN behavior", "A customer has no orders. Which join still shows that customer when `customers` is the left table?", ("INNER JOIN", "CROSS JOIN", "LEFT JOIN", "RIGHT JOIN"), 2, {0: "Drops unmatched customers", 1: "Creates combinations, not unmatched left rows", 3: "Preserves the other side"}),
    "COUNT and NULL": Question("p_sql3", "COUNT and NULL", "A column has values `5, NULL, 0`. What does `COUNT(column)` return?", ("1", "2", "3", "0"), 1, {0: "Incorrectly excludes zero", 2: "Incorrectly includes NULL", 3: "Excludes all valid values"}),
    "Train-test leakage": Question("p_ml1", "Train-test leakage", "You fit a text vocabulary on all samples before splitting. What is the risk?", ("Lower precision", "Overfitting is impossible", "Test-set information leaks into training", "No risk"), 2, {0: "Mistakes a possible effect for the main risk", 1: "Assumes preprocessing prevents overfitting", 3: "Misses information from the test set"}),
    "Precision vs recall": Question("p_ml2", "Precision vs recall", "Which metric measures how many actual positive cases were found?", ("Accuracy", "Recall", "Precision", "Specificity"), 1, {0: "Uses overall correctness", 2: "Measures correctness among predicted positives", 3: "Measures actual negatives found"}),
    "Overfitting": Question("p_ml3", "Overfitting", "Which change can help when a model memorizes training data?", ("Increase complexity", "Evaluate on training data only", "Remove the test set", "Use regularization"), 3, {0: "May increase memorization", 1: "Hides generalization problems", 2: "Removes independent evaluation"}),
}


GUIDES = {
    "Equality vs identity": "== compares values. is checks whether two references point to the same object. Separate lists can be equal without being identical.",
    "Loop boundaries": "range(start, stop) includes start and excludes stop. range(2, 5) yields 2, 3, 4.",
    "Function return values": "A Python function without an explicit return statement returns None. None is not the same object as False or 0.",
    "WHERE vs HAVING": "WHERE filters individual rows before grouping. HAVING filters groups after aggregation.",
    "JOIN behavior": "LEFT JOIN keeps every row from the left table and fills unmatched right-side columns with NULL.",
    "COUNT and NULL": "COUNT(column) counts non-NULL entries, including zero and empty strings. COUNT(*) counts rows.",
    "Train-test leakage": "Fit preprocessing only on training data, then apply the fitted transform to the test set. Features must be available at prediction time.",
    "Precision vs recall": "Recall = true positives / all actual positives. Precision = true positives / all predicted positives.",
    "Overfitting": "Overfitting means a model learns training-specific patterns and performs much worse on unseen data. Regularization can help.",
}
