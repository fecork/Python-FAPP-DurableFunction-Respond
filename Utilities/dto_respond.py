class Respond:
    """This is a data transfer object for the response of the pipeline"""

    def __init__(
        self,
        question: str,
        answer: str,
        category: int,
        quote: str,
        numberQuestion: int,
        boolean: bool,
        meanProbability: float,
    ) -> None:
        self.question = question
        self.answer = answer
        self.category = category
        self.quote = quote
        self.numberQuestion = numberQuestion
        self.boolean = boolean
        self.meanProbability = meanProbability
