from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from .models import Agent, Review
from tastypie import fields

#class AgentResource(ModelResource):
#    class Meta:
#        queryset = Agent.objects.all()
#        resource_name = 'agent'
#        filtering = {'id': ALL, 'name': ALL, 'telephone_number': ALL}

#class ReviewResource(ModelResource):
#    agent = fields.ForeignKey(AgentResource, 'agent', full=True)
#    class Meta:
#        queryset = Review.objects.all()
#        resource_name = 'review'
#        allow_methods = ['GET', 'POST']
#        authorization = Authorization()
#        filtering = {'agent': ALL_WITH_RELATIONS, 'name': ALL, 'rating':ALL, 'content':ALL}


