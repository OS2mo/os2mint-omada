# Generated by ariadne-codegen on 2024-08-22 11:26
# Source: queries.graphql

from uuid import UUID

from .base_model import BaseModel


class DeleteEngagement(BaseModel):
    engagement_delete: "DeleteEngagementEngagementDelete"


class DeleteEngagementEngagementDelete(BaseModel):
    uuid: UUID


DeleteEngagement.update_forward_refs()
DeleteEngagementEngagementDelete.update_forward_refs()
