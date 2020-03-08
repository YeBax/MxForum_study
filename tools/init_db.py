from apps.users.models import User
from apps.community.models import CommentLike,CommunityGroup,CommunityGroupMember,Post,PostComment
from peewee import MySQLDatabase

database = MySQLDatabase(
    host='test_db',
    port=3306,
    user="bioinfo",
    password="laso_bioinfo",
    database="webserver",
)


def init():
    # database.create_tables(User)
    database.create_tables([ CommentLike,CommunityGroup,CommunityGroupMember,Post,PostComment])


if __name__ == '__main__':
    init()
