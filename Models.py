
# A category is an axis the subject is being evaluated on
# Actual scoring will always be done based on percentage 
class Category:
    name: str 
    min: int 
    max: int
    
    def __init__(self, name, min, max):
        self.name = name
        self.min = min 
        self.max = max

    def get_score(self, value):
        return (value - self.min) / (self.max - self.min)
    
# A rubric defines how much each category is weighted in the final evaluation 
class Rubric:
    name = str
    mapping: dict[Category: int] = {}
    total_mass: int 

    def __init__(self, name, categories: list[Category] | dict[Category: int]):
        self.name = name
        if isinstance(categories, list):
            self.mapping = {category: 1 for category in categories}
        else:
            self.mapping = categories
        self.total_mass = sum(self.mapping.values())

    def set_weight(self, category: Category, weight: int):
        self.mapping[category] = weight
        self.total_mass = sum(self.mapping.values())
    
# A subject is an object that is being evaluated 
class Subject:
    name = str
    scores: dict[Category: int]

    def __init__(self, name, categories: list[Category]):
        self.name = name
        self.scores = {category: None for category in categories}
    
    def set_score(self, category: Category, value: int):
        self.scores[category] = category.get_score(value)
    
    def get_overall_score(self, rubric: Rubric):
        return sum([self.scores[category] * (rubric.mapping[category] / rubric.total_mass) for category in self.scores.keys()])
    
# A tierlist is a evaluation
class Tierlist:
    subjects: list[Subject]
    categories: list[Category]
    rubric: Rubric

    def __init__(self, subjects: list[Subject] | list[str], rubric: Rubric | str, categories: list[Category]):
        if isinstance(subjects[0], Subject):
            self.subjects = subjects
        else:
            self.subjects = [Subject(name, categories) for name in subjects]
        
        if isinstance(rubric, Rubric):
            self.rubric = rubric
        else:
            self.rubric = Rubric(rubric, categories)
        
        self.categories = categories

    def get_ordered_list(self):
        return sorted(self.subjects, key=lambda subject: subject.get_overall_score(self.rubric), reverse=True)

