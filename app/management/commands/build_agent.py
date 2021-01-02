from django.core.management.base import BaseCommand, CommandError
from app.core.services.builders.agent_builder import AgentBuilder


class Command(BaseCommand):

    help = 'Create a new agent'

    default_continent = 'alantica'

    def add_arguments(self, parser):
        parser.add_argument('number_of_agent', nargs='+', type=int)
        parser.add_argument('--continent', nargs='?', type=str,
                            default=self.default_continent)
    
    def handle(self, *args, **options):
        number_of_agents: int = options.get('number_of_agents', 10)
        continent: str = options.get('continent', self.default_continent)
        try:
            for agent in range(number_of_agents):
                builder = AgentBuilder(continent=continent)
                builder.build()
        except Exception as e:
            raise CommandError(e)
