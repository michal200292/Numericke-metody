from numpy.typing import NDArray


class Document:
    def __init__(self, title: str, question_id: int, text: str):
        self.question_title = title
        self.question_id = question_id
        self.text = text


class Vector:
    def __init__(self, title: str, question_id: int, vector: dict[str, int]):
        self.question_title = title
        self.question_id = question_id
        self.vector = vector


class TruncatedMatrix:
    def __init__(self, k: int, U_S: NDArray[float], sigma: NDArray[float], V: NDArray[float],
                 vector_lengths: NDArray[float]):
        self.k = k
        self.U_S = U_S
        self.sigma = sigma
        self.V = V
        self.vector_lengths = vector_lengths

