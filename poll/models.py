from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Poll(models.Model):
    owner=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Poll"
        verbose_name_plural = "Polls"

    def __str__(self):
        return self.text
    
    def user_can_vote(self,user):
        """
        Returns True if user can vote, else returns False
        """
        user_votes=user.vote_set.all()
        qs=user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True
    
    def num_votes(self):
        """
        Returns the number of votes on a poll
        """
        return self.vote_set.count()

        
    
class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200) 

    def __str__(self):
        return self.choice_text
    def num_votes(self):
        """
        Returns the number of votes on a particular choice
        """
        return self.vote_set.count()


class Vote(models.Model):
    poll=models.ForeignKey(Poll,on_delete=models.CASCADE)
    choice=models.ForeignKey(Choice,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)