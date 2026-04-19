from django.db import models
from src.app.common.models import Basemodel



class faq(Basemodel):
    question = models.CharField(max_length=200, blank=True, null=True)
    answer = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.question or "No Question"