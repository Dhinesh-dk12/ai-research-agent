from typing import List

from research.evidence import Evidence


class EvidenceCollector:

    def __init__(self):

        self.evidences: List[Evidence] = []

    def add_evidence(
        self,
        evidence: Evidence
    ):

        self.evidences.append(
            evidence
        )

    def get_all(self):

        return self.evidences

    def clear(self):

        self.evidences.clear()