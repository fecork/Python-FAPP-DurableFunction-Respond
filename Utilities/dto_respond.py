class Respond:
    """This is a data transfer object for the response of the pipeline"""

    def __init__(
        self,
        numberQuestion: int,
        question: str,
        answer: str,
        category: int,
        quote: str,
        freeText: str,
        boolean: bool,
        meanProbability: float,
        value: float,
        denomination: str,
    ) -> None:
        self.numberQuestion = numberQuestion
        self.question = question
        self.answer = answer
        self.category = category
        self.quote = quote
        self.freeText = freeText
        self.boolean = boolean
        self.meanProbability = meanProbability
        self.value = value
        self.denomination = denomination
