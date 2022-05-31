from django.db import models

# Create your models here.
class TrainData(models.Model):
    intent = models.CharField(max_length=128)
    ner = models.CharField(max_length=128)
    query = models.TextField(blank=True)
    answer = models.TextField(blank=True)
    answer_add = models.CharField(max_length=32)
    stage = models.IntegerField(default=0)
    stage_change = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.query} : {self.intent} {self.ner} : {self.answer}'

class UserChatData(models.Model):
    query = models.TextField(blank=True)
    ai_intent = models.CharField(max_length=128)
    ai_ner = models.CharField(max_length=128)
    ad_intent = models.CharField(max_length=128)
    ad_ner = models.CharField(max_length=128)
    trian_num = models.IntegerField(default=0)
    on_train = models.BooleanField(default=True)
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.query} : {self.ai_intent} {self.ai_ner}'