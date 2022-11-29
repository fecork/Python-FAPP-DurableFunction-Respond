class Respond:
    """This is a data transfer object for the response of the pipeline"""

    def __init__(
        self,
        question: str,
        answer: str,
        category: int,
        quote: str,
        freeText: str,
        numberQuestion: int,
        boolean: bool,
        meanProbability: float,
        value: float,
        denomination: str,
    ) -> None:
        self.question = question
        self.answer = answer
        self.category = category
        self.quote = quote
        self.freeText = freeText
        self.numberQuestion = numberQuestion
        self.boolean = boolean
        self.meanProbability = meanProbability
        self.value = value
        self.denomination = denomination
