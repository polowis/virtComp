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
        number_of_agents: int = options.get('number_of_agent', [10])
        continent: str = options.get('continent', self.default_continent)
        try:
            builder = AgentBuilder(continent=continent)
            builder.build_many_agents(number_of_agents[0])
        except Exception as e:
            raise CommandError(e)
