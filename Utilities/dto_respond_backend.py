class Respond:
    """This is a data transfer object for the response of the pipeline"""

    def __init__(
        self,
        fareBasis: list,
        passengerTypes: list,
        modelRespond: list,
        average: float,
        freeText: list,
    ) -> None:
        self.fareBasis = fareBasis
        self.passengerTypes = passengerTypes
        self.modelRespond = modelRespond
        self.average = average
        self.freeText = freeText

