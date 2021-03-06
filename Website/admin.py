from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User

from Website.models import Champion, Item, Match, Participant, Profile, Summoner, Team, Post, PostInteraction, \
    SummonerSpell, ParticipantFrame, MatchEvent, RegistrationInterest, AccessCode, Notification, RankedTier


class RankedTierAdmin(admin.ModelAdmin):
    model = RankedTier

    list_display = (
        'key',
        'name',
    )


class PostAdmin(admin.ModelAdmin):
    model = Post

    list_display = (
        'user_source',
        'post_type',
        'date_modified',
        'date_created',
    )

    search_fields = (
        'user_source__username',
    )


class PostInteractionAdmin(admin.ModelAdmin):
    model = PostInteraction

    list_display = (
        'user',
        'post',
        'post_interaction_type',
        'date_modified',
        'date_created',
    )

    search_fields = (
        'user__username',
        'post'
    )


class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'last_login',
        'date_joined',
    )


class SummonerSpellAdmin(admin.ModelAdmin):
    model = SummonerSpell


class NotificationAdmin(admin.ModelAdmin):
    model = Notification

    list_display = (
        'title',
        'user',
        'category',
        'date_modified',
        'date_created'
    )


class SummonerAdmin(admin.ModelAdmin):
    model = Summoner

    list_display = (
        'summoner_name',
        'user_profile',
        'server',
        'summoner_level',
        'ranked_solo_tier',
        'ranked_flex_tt_tier',
        'ranked_flex_sr_tier',
        'date_created',
        'date_updated'
    )

    list_select_related = (
        'user_profile',
        'ranked_solo_tier',
        'ranked_flex_tt_tier',
        'ranked_flex_sr_tier',
    )

    search_fields = (
        'summoner_name',
        'summoner_id',
        'user_profile__user__username',
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        readonly_fields.remove('user_profile')
        return readonly_fields


class MatchAdmin(admin.ModelAdmin):
    model = Match

    list_display = (
        'game_id',
        'queue_id',
        'season_id',
        'platform_id',
        'timestamp',
        'date_created'
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        return readonly_fields


class TeamAdmin(admin.ModelAdmin):
    model = Team

    list_display = (
        'team_id',
        'match',
        'date_created',
    )

    list_select_related = (
        'match',
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        return readonly_fields


class ParticipantAdmin(admin.ModelAdmin):
    model = Participant

    list_display = (
        'summoner',
        'champion',
        'date_created',
    )

    list_select_related = (
        'summoner',
        'champion',
        'match',
    )

    search_fields = (
        'match__game_id',
        'summoner__summoner_name'
    )

    list_per_page = 50

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        return readonly_fields

    def get_fields(self, request, obj=None):
        fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        return sorted(fields)


class ProfileAdmin(admin.ModelAdmin):
    model = Profile

    list_display = (
        'user',
        'email',
        'email_confirmed',
        'date_created',
        'date_modified'
    )

    list_select_related = (
        'user',
    )

    readonly_fields = (
        'date_created',
        'date_modified'
    )

    search_fields = (
        'user',
    )

    @staticmethod
    def email(self):
        return self.user.email


class ChampionAdmin(admin.ModelAdmin):
    model = Champion
    ordering = ('name',)

    list_display = (
        'name',
        'key',
        'version'
    )

    search_fields = (
        'name',
    )


class ItemAdmin(admin.ModelAdmin):
    model = Item

    list_display = (
        'item_id',
        'name',
        'version'
    )


class ParticipantFrameAdmin(admin.ModelAdmin):
    model = ParticipantFrame

    list_display = (
        'match',
        'participant_id',
        'timestamp',
        'date_created'
    )

    list_select_related = (
        'match',
    )

    search_fields = (
        'match__game_id',
    )


class MatchEventAdmin(admin.ModelAdmin):
    model = MatchEvent

    list_display = (
        'match',
        'type',
        'timestamp',
        'date_created'
    )

    list_select_related = (
        'match',
    )

    search_fields = (
        'match__game_id',
    )


class RegistrationInterestAdmin(admin.ModelAdmin):
    model = RegistrationInterest

    list_display = (
        'name',
        'user',
        'accepted',
        'date_created'
    )

    list_select_related = (
        'user',
    )

    search_fields = (
        'email',
    )


class AccessCodeAdmin(admin.ModelAdmin):
    model = AccessCode

    list_display = (
        'key',
        'used',
        'user',
        'date_used',
        'date_created',
        'archived'
    )


admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Summoner, SummonerAdmin)
admin.site.register(Champion, ChampionAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(SummonerSpell, SummonerSpellAdmin)
admin.site.register(ParticipantFrame, ParticipantFrameAdmin)
admin.site.register(MatchEvent, MatchEventAdmin)
admin.site.register(RegistrationInterest, RegistrationInterestAdmin)
admin.site.register(AccessCode, AccessCodeAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostInteraction, PostInteractionAdmin)
admin.site.register(RankedTier, RankedTierAdmin)
