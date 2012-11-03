from django.db import models
from django.contrib.auth.models import User

# Notes:
# - Django automatically creates an 'id' field as a primary key
# - I've created alright __str__ methods, but feel free to change them to
#   suit you
# - Because we use the related_name argument when defining foreign keys, you
#   can access UserProfiles and Announcements through House objects.
#   For example:
#   h = House.objects.get(name='my house')
#   h.members.all()
#   This lists all of the members of the given house.


class House(models.Model):
    name = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=9)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    birthday = models.DateField(null=True)
    # should perhaps be a ManyToManyField, but for simplicity, we'll only allow
    # one house per person for now.
    house = models.ForeignKey(
        House, related_name='members', null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.user.__str__()


class Announcement(models.Model):
    creator = models.ForeignKey(UserProfile)
    title = models.CharField(max_length=100)
    text = models.TextField()
    house = models.ForeignKey(House, related_name='announcements')

    def __str__(self):
        return self.creator.__str__() + ": " + self.title
