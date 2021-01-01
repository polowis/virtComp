from django.db import models
from app.models.core.agent import AgentCustomer
import random
from django.utils import timezone
from .agent_tracker import AgentStatsTracker


def random_score():
    return random.randint(1, 100)


class AgentWeightConfig(object):
    """The Agent Weight Factor score"""
    def __init__(self):
        self.qualification_weight = 1.8
        self.productivity_weight = 1.2
        self.communication_weight = 0.5
        self.creativity_weight = 0.8
        self.leadership_weight = 0.2
        self.learning_weight = 1.5
    
    def get_weight(self, key: str):
        """Get the weight factor of given supported key
        Raise Error if key is not supported
        """
        key: str = key.lower()
        if not key.endswith('_weight'):
            key = key + '_weight'
            return self.to_dict[key]
        return self.to_dict[key]

    def to_dict(self):
        return self.__dict__


agent_weight = AgentWeightConfig()


class AgentStatsManager(models.Manager):
    def create_stats(self, agent):
        """Create stats for given FRESH agent instance
        
        All stats are calculated at random
        """
        return self.create(agent=agent, **self.stats_generator())
    
    def stats_generator(self):
        values: dict = {
            'qualification': random_score(),
            'productivity': random_score(),
            'communication': random_score(),
            'creativity': random_score(),
            'leadership': random_score(),
            'learning': random_score(),
        }
        return values





class AgentStats(models.Model):
    """The Agent_Stats model"""
    agent = models.OneToOneField(AgentCustomer, on_delete=models.CASCADE, primary_key=True, related_name="agent")

    # the original data
    qualification = models.IntegerField(default=random_score)
    productivity = models.IntegerField(default=random_score)
    communication = models.IntegerField(default=random_score)
    creativity = models.IntegerField(default=random_score)
    leadership = models.IntegerField(default=random_score)
    learning = models.IntegerField(default=random_score)

    stress = models.IntegerField(default=0)
    emotion = models.IntegerField(default=100)

    salary = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    hour_of_work_per_day = models.IntegerField(default=0)

    is_rest = models.BooleanField(default=True)
    is_employed = models.BooleanField(default=False)

    updated_at = models.DateTimeField()

    objects = models.Manager()
    attribute = AgentStatsManager()

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        AgentStatsTracker.objects.create_tracker(self.attributes_to_dict())
        return super().save(*args, **kwargs)

    @property
    def qualification_score(self) -> float:
        return self.qualification * self.score_weight('qualification')
    
    @property
    def productivity_score(self):
        return self.productivity * self.score_weight('productivity')
    
    @property
    def communication_score(self):
        return self.communication * self.score_weight('communication')
    
    @property
    def creativity_score(self):
        return self.creativity * self.score_weight('creativity')
    
    @property
    def leadership_score(self):
        return self.leadership * self.score_weight('leadership')
    
    @property
    def learning_score(self):
        return self.learning * self.score_weight('learning')

    def score_weight(self, key):
        """Get the score weight from given key"""
        return agent_weight.get_weight(key)
    
    def attributes_to_dict(self):
        """return main attributes of agent as dictionary"""
        values = {
            'qualification': self.qualification,
            'productivity': self.productivity,
            'communication': self.communication,
            'learning': self.learning,
            'leadership': self.leadership,
            'creativity': self.creativity,
        }

        return values
    
    @property
    def perfomance_score(self):
        """Get the performance score from the agent"""
        perfomance_score_keys: list = ['qualification', 'productivity', 'communication',
                                       'learning', 'leadership', 'creativity']
        
        total_perfomance = sum([getattr(self, i + '_score') for i in perfomance_score_keys])
        return total_perfomance / 5
    
    def item_producing_time(self, item_in_sec: int):
        """The time to produce in seconds from this agent given the expected time"""
        return item_in_sec - self.perfomance_score / 60 * item_in_sec
