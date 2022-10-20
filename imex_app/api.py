from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from .models import Review, Agent, AgentType
from tastypie import fields
from tastypie.authorization import Authorization

# class AgentTypeResource(ModelResource):
#     class Meta:
#         queryset = AgentType.objects.all()
#         resource_name = 'agent_type'
#         filtering = {'slug': ALL}

# class AgentResource(ModelResource):
#     agent_type = fields.ForeignKey(AgentTypeResource, 'agent_type', full=True)
#     class Meta:
#         queryset = Agent.objects.all()
#         resource_name = 'agent'
#         filtering = {'agent_type': ALL_WITH_RELATIONS, 'name': ALL, 'telephone_number': ALL}

# class ReviewResource(ModelResource):
#     agent = fields.ForeignKey(AgentResource(), 'agent', full=True)
#     class Meta:
#         queryset = Review.objects.all()
#         resource_name = 'review'
#         allow_methods = ['GET', 'POST']
#         authorization = Authorization()
#         filtering = {'agent': ALL_WITH_RELATIONS, 'name': ALL, 'subject': ALL, 'content':ALL}

# class ReviewResource(ModelResource):
#     agent = fields.ForeignKey(AgentResource, 'agent', full=True)
#     class Meta:
#         queryset = Review.objects.all()
#         resource_name = 'review'
#         allow_methods = ['GET', 'POST']
#         authorization = Authorization()
#         filtering = {'agent': ALL_WITH_RELATIONS, 'name': ALL, 'subject': ALL, 'content':ALL}

class AgentResource(ModelResource):
    class Meta:
        queryset = Agent.objects.all()
        resource_name = 'agent'
        filtering = {'id': ALL, 'name': ALL, 'telephone_number': ALL}

class ReviewResource(ModelResource):
    agent = fields.ForeignKey(AgentResource, 'agent', full=True)
    class Meta:
        queryset = Review.objects.all()
        resource_name = 'review'
#        allow_methods = ['GET', 'POST']
#        authorization = Authorization()
        filtering = {'agent': ALL_WITH_RELATIONS, 'name': ALL, 'rating':ALL, 'content':ALL}