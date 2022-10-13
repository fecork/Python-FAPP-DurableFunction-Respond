class Respond:
    """This is a data transfer object for the response of the pipeline"""

    def __init__(
        self,
        Question: str,
        Answer: str,
        Category: int,
        Quote: str,
        FreeText: str,
        NumberQuestion: int,
        Boolean: bool,
        MeanProbability: float,
        Value: float,
        Denomination: str,
    ) -> None:
        self.Question = Question
        self.Answer = Answer
        self.Category = Category
        self.Quote = Quote
        self.FreeText = FreeText
        self.NumberQuestion = NumberQuestion
        self.Boolean = Boolean
        self.MeanProbability = MeanProbability
        self.Value = Value
        self.Denomination = Denomination
