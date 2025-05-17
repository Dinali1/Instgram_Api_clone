from django.db import models
from django.contrib.auth.models import User

# Create your here.

# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.db.models import Model, OneToOneField, BooleanField, CharField, EmailField, TextField, ImageField, \
#     ManyToManyField, CASCADE, ForeignKey, FileField, DateTimeField, PositiveIntegerField, GenericIPAddressField, \
#     DecimalField, SET_NULL, URLField
#
#
# class User(AbstractUser):
#     email = EmailField(unique=True)
#     bio = TextField(blank=True)
#     profile_picture = ImageField(upload_to='profiles/', null=True, blank=True)
#     followers = ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
#     is_private = BooleanField(default=False)
#     instagram_id = CharField(max_length=7)
#
#     def __str__(self):
#         return self.username
# class UserSettings(Model):
#     user = OneToOneField(User, on_delete=CASCADE, related_name='settings')
#     dark_mode = BooleanField(default=False)
#     push_notifications = BooleanField(default=True)
#     language = CharField(max_length=20, default='en')
#     account_hidden = BooleanField(default=False)
#
#     def __str__(self):
#         return f"Settings for {self.user.username}"
#
#
# class Post(Model):
#     MEDIA_TYPE_CHOICES = [('image', 'Image'), ('video', 'Video'),]
#     user = ForeignKey('apps.User', on_delete=CASCADE, related_name='posts')
#     media = FileField(upload_to='posts/')
#     media_type = CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
#     caption = TextField(blank=True)
#     created_at = DateTimeField(auto_now_add=True)
#     liked_by = ManyToManyField('apps.User', related_name='liked_posts', blank=True)
#     is_archived = BooleanField(default=False)
#
#     def __str__(self):
#         return f'{self.user.username} Post'
#
#
# class PostComment(Model):
#     user = ForeignKey('apps.User', on_delete=CASCADE)
#     post = ForeignKey('apps.Post', on_delete=CASCADE, related_name='comments')
#     text = TextField()
#     created_at = DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.user.username} on Post {self.post.id}'
#
# class Story(Model):
#     MEDIA_TYPE_CHOICES = [('image', 'Image'), ('video', 'Video'),]
#     user = ForeignKey('apps.User', on_delete=CASCADE)
#     media = FileField(upload_to='stories/')
#     media_type = CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
#     created_at = DateTimeField(auto_now_add=True)
#     viewers = ManyToManyField(User, related_name='viewed_stories', blank=True)
#
#     def __str__(self):
#         return f'{self.user.username} Story'
#
# class Message(Model):
#     MEDIA_TYPE_CHOICES = [('text', 'Text'), ('image', 'Image'),('video', 'Video'),]
#     sender = ForeignKey('apps.User', on_delete=CASCADE, related_name='sent_messages')
#     receiver = ForeignKey('apps.User', on_delete=CASCADE, related_name='received_messages')
#     media_type = CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
#     content = TextField(blank=True)
#     media = FileField(upload_to='messages/', blank=True, null=True)
#     created_at = DateTimeField(auto_now_add=True)
#     is_read = BooleanField(default=False)
#
#     def __str__(self):
#         return f'Message from {self.sender} to {self.receiver}'
#
# class Notification(Model):
#     NOTIF_TYPE = (('like', 'Like'),('comment', 'Comment'),('follow', 'Follow'),('message', 'Message'),('tag', 'Tag'),)
#     sender = ForeignKey(User, on_delete=CASCADE, related_name='sent_notifications')
#     receiver = ForeignKey(User, on_delete=CASCADE, related_name='notifications')
#     notif_type = CharField(max_length=10, choices=NOTIF_TYPE)
#     post = ForeignKey(Post, on_delete=CASCADE, null=True, blank=True)
#     comment = ForeignKey(PostComment, on_delete=CASCADE, null=True, blank=True)
#     is_read = BooleanField(default=False)
#     created_at = DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.notif_type} from {self.sender} to {self.receiver}'
#
# class Reel(Model):
#     user = ForeignKey('apps.User', on_delete=CASCADE, related_name='reels')
#     video = FileField(upload_to='reels/')
#     caption = TextField(blank=True)
#     created_at = DateTimeField(auto_now_add=True)
#     liked_by = ManyToManyField(User, related_name='liked_reels', blank=True)
#     views = PositiveIntegerField(default=0)
#
#     def __str__(self):
#         return f'{self.user.username} Reel'
#
# class SavedPost(Model):
#     user = ForeignKey('apps.User', on_delete=CASCADE, related_name='saved_posts')
#     post = ForeignKey('apps.Post', on_delete=CASCADE, related_name='saved_by')
#     saved_at = DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ('user', 'post')
#
#     def __str__(self):
#         return f'{self.user.username} saved Post {self.post.id}'
#
#
# class TaggedUser(Model):
#     post = ForeignKey('apps.Post', on_delete=CASCADE, related_name='tagged_users')
#     user = ForeignKey('apps.User', on_delete=CASCADE)
#
#     def __str__(self):
#         return f'{self.user.username} tagged in Post {self.post.id}'
#
# class Hashtag(Model):
#     name = CharField(max_length=100, unique=True)
#
#     def __str__(self):
#         return f'#{self.name}'
#
# class PostHashtag(Model):
#     post = ForeignKey('apps.Post', on_delete=CASCADE, related_name='hashtags')
#     hashtag = ForeignKey('apps.Hashtag', on_delete=CASCADE)
#
#     def __str__(self):
#         return f'{self.post.id} tagged with #{self.hashtag.name}'
#
#
# class Highlight(Model):
#     user = ForeignKey('apps.User', on_delete=CASCADE, related_name='highlights')
#     title = CharField(max_length=100)
#     cover_image = ImageField(upload_to='highlight_covers/', null=True, blank=True)
#     stories = ManyToManyField(Story, related_name='included_in_highlights')
#     created_at = DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.user.username} Highlight: {self.title}'
#
#
# class LiveStream(Model):
#     user = ForeignKey('apps.User', on_delete=CASCADE, related_name='live_streams')
#     stream_title = CharField(max_length=255)
#     stream_key = CharField(max_length=100, unique=True)
#     is_live = BooleanField(default=False)
#     viewers = ManyToManyField(User, related_name='watching_lives', blank=True)
#     started_at = DateTimeField(null=True, blank=True)
#     ended_at = DateTimeField(null=True, blank=True)
#
#     def __str__(self):
#         return f'{self.user.username} Live Stream'
#
#
# class BlockedUser(Model):
#     blocker = ForeignKey('apps.User', on_delete=CASCADE, related_name='blocked_users')
#     blocked = ForeignKey('apps.User', on_delete=CASCADE, related_name='blocked_by')
#     created_at = DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ('blocker', 'blocked')
#
#     def __str__(self):
#         return f'{self.blocker} blocked {self.blocked}'
#
# class Report(Model):
#     REPORT_TYPE_CHOICES = [('user', 'User'),('post', 'Post'),('reel', 'Reel'),('story', 'Story'),('comment', 'Comment'),]
#     reporter = ForeignKey('apps.User', on_delete=CASCADE, related_name='reports_made')
#     report_type = CharField(max_length=10, choices=REPORT_TYPE_CHOICES)
#     reported_user = ForeignKey('apps.User', on_delete=CASCADE, related_name='reports_received', null=True, blank=True)
#     reported_post = ForeignKey('apps.Post', on_delete=CASCADE, null=True, blank=True)
#     reported_reel = ForeignKey('apps.Reel', on_delete=CASCADE, null=True, blank=True)
#     reported_story = ForeignKey('apps.Story', on_delete=CASCADE, null=True, blank=True)
#     reported_comment = ForeignKey('apps.PostComment', on_delete=CASCADE, null=True, blank=True)
#     reason = TextField()
#     created_at = DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.reporter.username} reported {self.report_type}'
#
#
#
# class ActivityLog(Model):
#     user = ForeignKey('apps.User', on_delete=CASCADE, related_name='activities')
#     action = CharField(max_length=255)
#     ip_address = GenericIPAddressField(null=True, blank=True)
#     user_agent = TextField(blank=True)
#     timestamp = DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.user.username}: {self.action}'
#
# class Device(Model):
#     user = ForeignKey('apps.User', on_delete=CASCADE, related_name='devices')
#     device_name = CharField(max_length=100)
#     device_os = CharField(max_length=100, blank=True)
#     last_login = DateTimeField(auto_now=True)
#     is_active = BooleanField(default=True)
#
#     def __str__(self):
#         return f'{self.device_name} for {self.user.username}'
#
# class Poll(Model):
#     post = OneToOneField('apps.Post', on_delete=CASCADE, related_name='poll')
#     question = CharField(max_length=255)
#     created_at = DateTimeField(auto_now_add=True)
#
# class PollOption(Model):
#     poll = ForeignKey('apps.Poll', on_delete=CASCADE, related_name='options')
#     option_text = CharField(max_length=100)
#
# class PollVote(Model):
#     user = ForeignKey('apps.User', on_delete=CASCADE)
#     option = ForeignKey('apps.PollOption', on_delete=CASCADE, related_name='votes')
#
#     class Meta:
#         unique_together = ('user', 'option')
#
#
# class GroupChat(Model):
#     name = CharField(max_length=100)
#     members = ManyToManyField('apps.User', related_name='group_chats')
#     created_at = DateTimeField(auto_now_add=True)
#
# class GroupMessage(Model):
#     group = ForeignKey('apps.GroupChat', on_delete=CASCADE, related_name='messages')
#     sender = ForeignKey('apps.User', on_delete=CASCADE)
#     content = TextField()
#     media = FileField(upload_to='group_messages/', blank=True, null=True)
#     sent_at = DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.sender.username} in {self.group.name}'
# class LocationTag(Model):
#     post = ForeignKey('apps.Post', on_delete=CASCADE, related_name='locations')
#     name = CharField(max_length=255)
#     latitude = DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
#     longitude = DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
#
#     def __str__(self):
#         return self.name
#
# class Archive(Model):
#     user = ForeignKey('apps.User', on_delete=CASCADE, related_name='archives')
#     post = ForeignKey('apps.Post', on_delete=CASCADE)
#     archived_at = DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ('user', 'post')
#
#     def __str__(self):
#         return f'{self.user.username} archived Post {self.post.id}'
#
# class Subscription(models.Model):
#     user = ForeignKey('apps.User', on_delete=CASCADE, related_name='subscriptions')
#     creator = ForeignKey('apps.User', on_delete=CASCADE, related_name='creators_subscribed')
#     start_date = DateTimeField(auto_now_add=True)
#     end_date = DateTimeField()
#     active = BooleanField(default=True)
#
#     def __str__(self):
#         return f'{self.user.username} subscribed to {self.creator.username}'
#
# class PostAnalytics(models.Model):
#     post = OneToOneField('apps.Post', on_delete=CASCADE, related_name='analytics')
#     reach = PositiveIntegerField(default=0)
#     likes = PositiveIntegerField(default=0)
#     comments = PositiveIntegerField(default=0)
#     saves = PositiveIntegerField(default=0)
#     shares = PositiveIntegerField(default=0)
#
#     def __str__(self):
#         return f'Analytics for Post {self.post.id}'
#
#
# class Reaction(models.Model):
#     REACTION_CHOICES = [
#         ('like', 'Like'),
#         ('love', 'Love'),
#         ('haha', 'Haha'),
#         ('wow', 'Wow'),
#         ('sad', 'Sad'),
#         ('angry', 'Angry'),
#     ]
#
#     user = ForeignKey('apps.User', on_delete=CASCADE, related_name='reactions')
#     post = ForeignKey('apps.Post', on_delete=CASCADE, related_name='reactions')
#     reaction_type = CharField(max_length=10, choices=REACTION_CHOICES)
#     created_at = DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ('user', 'post', 'reaction_type')
#
#     def __str__(self):
#         return f'{self.user.username} reacted with {self.reaction_type} to Post {self.post.id}'
#
# class Badge(models.Model):
#     name = CharField(max_length=100)
#     description = TextField()
#     image = ImageField(upload_to='badges/', null=True, blank=True)
#
#     def __str__(self):
#         return self.name
#
# class UserBadge(models.Model):
#     user = ForeignKey('apps.User', on_delete=CASCADE, related_name='badges')
#     badge = ForeignKey('apps.Badge', on_delete=CASCADE)
#     awarded_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ('user', 'badge')
#
#     def __str__(self):
#         return f'{self.user.username} awarded {self.badge.name}'
#
# class DraftPost(Model):
#     user = ForeignKey('apps.User', on_delete=CASCADE, related_name='draft_posts')
#     content = TextField()
#     image = ImageField(upload_to='draft_posts/', null=True, blank=True)
#     created_at = DateTimeField(auto_now_add=True)
#     is_published = BooleanField(default=False)
#
#     def __str__(self):
#         return f'Draft Post by {self.user.username}'
#
# class PostEditHistory(models.Model):
#     post = ForeignKey(Post, on_delete=CASCADE, related_name='edit_history')
#     edited_by = ForeignKey(User, on_delete=CASCADE)
#     previous_content = TextField()
#     previous_image = ImageField(upload_to='post_edits/', null=True, blank=True)
#     edited_at = DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.edited_by.username} edited Post {self.post.id}'
#
#
#
# class PinnedPost(models.Model):
#     user = ForeignKey(User, on_delete=CASCADE, related_name='pinned_posts')
#     post = ForeignKey(Post, on_delete=CASCADE)
#     pinned_at = DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ('user', 'post')
#
#     def __str__(self):
#         return f'{self.post.id} pinned by {self.user.username}'
#
#
# class Product(models.Model):
#     name = CharField(max_length=255)
#     description = TextField()
#     price = DecimalField(max_digits=10, decimal_places=2)
#     image = ImageField(upload_to='products/')
#
#     def __str__(self):
#         return self.name
#
#
# class ProductTag(Model):
#     post = ForeignKey(Post, on_delete=CASCADE, related_name='product_tags')
#     product = ForeignKey(Product, on_delete=CASCADE)
#
#     def __str__(self):
#         return f'{self.product.name} tagged in Post {self.post.id}'
#
#
# class Event(models.Model):
#     creator = ForeignKey(User, on_delete=CASCADE)
#     title = CharField(max_length=255)
#     description = TextField()
#     location = CharField(max_length=255, null=True, blank=True)
#     is_online = BooleanField(default=False)
#     start_time = DateTimeField()
#     end_time = DateTimeField()
#     participants = ManyToManyField(User, related_name='events_joined', blank=True)
#
#     def __str__(self):
#         return self.title
#
#
# class Notifications(Model):
#     recipient = ForeignKey(User, on_delete=CASCADE, related_name='notifications')
#     sender = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
#     message = CharField(max_length=255)
#     url = URLField(null=True, blank=True)
#     is_read = BooleanField(default=False)
#     created_at = DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'Notification to {self.recipient.username}'
#
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followed_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ('follower', 'following')
#
#     def __str__(self):
#         return f'{self.follower.username} → {self.following.username}'
#
# class Payment(Model):
#     user = ForeignKey(User, on_delete=CASCADE)
#     amount = DecimalField(max_digits=10, decimal_places=2)
#     description = CharField(max_length=255)
#     timestamp = DateTimeField(auto_now_add=True)
#     status = CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])
#
#     def __str__(self):
#         return f'{self.user.username} - {self.amount}'
#
# class Conversation(Model):
#     participants = ManyToManyField(User, related_name='conversations')
#     created_at = DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'Conversation {self.id}'
#
# class Messages(Model):
#     conversation = models.ForeignKey(Conversation, on_delete=CASCADE, related_name='messages')
#     sender = ForeignKey(User, on_delete=models.CASCADE)
#     content = TextField()
#     image = ImageField(upload_to='messages/', null=True, blank=True)
#     created_at = DateTimeField(auto_now_add=True)
#     is_read = BooleanField(default=False)
#
#     def __str__(self):
#         return f'Message from {self.sender.username}'
#
#
# class StoryAnalytics(Model):
#     story = OneToOneField('Story', on_delete=CASCADE, related_name='analytics')
#     views = PositiveIntegerField(default=0)
#     replies = PositiveIntegerField(default=0)
#     reactions = PositiveIntegerField(default=0)
#
#     def __str__(self):
#         return f'Analytics for Story {self.story.id}'
#
#
# class StoryReaction(Model):
#     story = ForeignKey('Story', on_delete=CASCADE, related_name='reactions')
#     user = ForeignKey(User, on_delete=CASCADE)
#     emoji = CharField(max_length=10)
#     reacted_at = DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ('story', 'user')
#
#     def __str__(self):
#         return f'{self.user.username} reacted to Story {self.story.id}'
#
#
# class Mention(Model):
#     post = ForeignKey(Post, on_delete=CASCADE, related_name='mentions')
#     mentioned_user = ForeignKey(User, on_delete=CASCADE)
#     created_at = DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.mentioned_user.username} mentioned in Post {self.post.id}'
#
#
# class VerificationRequest(Model):
#     user = OneToOneField(User, on_delete=CASCADE)
#     full_name = CharField(max_length=255)
#     id_document = ImageField(upload_to='verification_docs/')
#     message = TextField(blank=True, null=True)
#     status = CharField(max_length=20, choices=[
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ], default='pending')
#     submitted_at = DateTimeField(auto_now_add=True)
#     reviewed_at = DateTimeField(null=True, blank=True)
#
#     def __str__(self):
#         return f'{self.user.username} - {self.status}'
#
# class TwoFactorAuth(Model):
#     user = OneToOneField(User, on_delete=CASCADE)
#     is_enabled = BooleanField(default=False)
#     secret_key = CharField(max_length=64, blank=True, null=True)
#     backup_codes = TextField(blank=True, null=True)
#
#     def __str__(self):
#         return f'{self.user.username} - 2FA: {"On" if self.is_enabled else "Off"}'
#
# class SavedSearch(Model):
#     user = ForeignKey(User, on_delete=CASCADE)
#     keyword = CharField(max_length=255)
#     searched_at = DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.user.username} searched "{self.keyword}"'
#
#
#
#
# class AdCampaign(models.Model):
#     advertiser = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     budget = models.DecimalField(max_digits=10, decimal_places=2)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     active = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.name
#
# class SponsoredPost(models.Model):
#     campaign = models.ForeignKey(AdCampaign, on_delete=models.CASCADE)
#     post = models.ForeignKey('Post', on_delete=models.CASCADE)
#     promoted_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'Sponsored {self.post.id} in {self.campaign.name}'
#
# class UserDeviceLog(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     ip_address = models.GenericIPAddressField()
#     user_agent = models.TextField()
#     location = models.CharField(max_length=255, blank=True, null=True)
#     login_time = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.user.username} - {self.ip_address}'
#
# class ContentModeration(models.Model):
#     post = models.ForeignKey('Post', on_delete=models.CASCADE)
#     flagged = models.BooleanField(default=False)
#     reason = models.CharField(max_length=255, null=True, blank=True)
#     confidence = models.FloatField(default=0.0)
#     reviewed = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f'Post {self.post.id} - Flagged: {self.flagged}'

############################################################
#####################################
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models import Model, OneToOneField, CASCADE, ImageField, CharField, URLField, BooleanField, \
    DateTimeField, ForeignKey, FileField, TextField, ManyToManyField, PositiveIntegerField, IntegerField
from django.urls import reverse
from datetime import timedelta

from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_pictures', default='default.jpg')
    bio = models.CharField(max_length=160, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

class Post(Model):
    POST_TYPES = [('image', 'Image Post'), ('video', 'Video Post'), ('reel', 'Reel')]
    user = ForeignKey(User, on_delete=CASCADE)
    file = FileField(upload_to='posts/')  # Rasm yoki video
    caption = TextField(blank=True, null=True)
    post_type = CharField(max_length=10, choices=POST_TYPES, default='image')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    tags = ManyToManyField('Tag', related_name='posts', blank=True)
    location = CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Post - {self.post_type}"

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class Story(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    file = FileField(upload_to='stories/')
    created_at = DateTimeField(auto_now_add=True)
    expires_at = DateTimeField()  # 24 soatdan keyin o'chadi
    viewers = ManyToManyField(User, related_name='viewed_stories', blank=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Story"

class SavedPost(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    post = ForeignKey(Post, on_delete=CASCADE)
    saved_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} saved {self.post.id}"

class Like(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    post = ForeignKey(Post, on_delete=CASCADE, related_name='likes')
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"

class Comment(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    post = ForeignKey(Post, on_delete=CASCADE, related_name='comments')
    text = TextField()
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}..."

class Follow(Model):
    follower = ForeignKey(User, related_name='following', on_delete=CASCADE)
    following = ForeignKey(User, related_name='followers', on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"



class Message(Model):
    sender = ForeignKey(User, related_name='sent_messages', on_delete=CASCADE)
    receiver = ForeignKey(User, related_name='received_messages', on_delete=CASCADE)
    text = TextField()
    file = FileField(upload_to='messages/', blank=True, null=True)
    is_read = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}"

class PostStat(Model):
    post = OneToOneField(Post, on_delete=CASCADE, related_name='stats')
    views = PositiveIntegerField(default=0)
    likes_count = PositiveIntegerField(default=0)
    comments_count = PositiveIntegerField(default=0)
    shares = PositiveIntegerField(default=0)

    def __str__(self):
        return f"Stats for Post #{self.post.id}"

class Tag(Model):
    name = CharField(max_length=50, unique=True)
    post_count = PositiveIntegerField(default=0)

    def __str__(self):
        return f"#{self.name}"

    def update_post_count(self):
        self.post_count = self.posts.count()
        self.save()

class Notification(Model):
    NOTIFICATION_TYPES = [(1, 'Like'), (2, 'Comment'), (3, 'Follow'), (4, 'Message'), (5, 'Story View') ]

    user = ForeignKey(User, on_delete=CASCADE, related_name='notifications')
    sender = ForeignKey(User, on_delete=CASCADE, related_name='sent_notifications')
    notification_type = IntegerField(choices=NOTIFICATION_TYPES)
    post = ForeignKey(Post, on_delete=CASCADE, null=True, blank=True)
    comment = ForeignKey(Comment, on_delete=CASCADE, null=True, blank=True)
    story = ForeignKey(Story, on_delete=CASCADE, null=True, blank=True)
    is_read = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} - {self.get_notification_type_display()}"

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=Post)
def create_post_stats(sender, instance, created, **kwargs):
    if created:
        PostStat.objects.create(post=instance)

@receiver(post_save, sender=Like)
def send_like_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.post.user,
            sender=instance.user,
            notification_type=1,
            post=instance.post
        )




















