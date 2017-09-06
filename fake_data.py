from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Genre, Tvseries, User
engine = create_engine('sqlite:///tvseries.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

user1 = User(name='abcdef', email='abcdef@example.com')
session.add(user1)
session.commit()

user2 = User(name='zyxwvu', email='zyxwvu@example.com')
session.add(user2)
session.commit()

genre1 = Genre(name="Action")

session.add(genre1)
session.commit()

tvseries1 = Tvseries(name="The Defenders", rating="3", user_id=1,
                     description="""
                         Four of Marvel's biggest heroes are each
                         working individually but have one common goal
                         in mindto save New York City.""",
                     genre=genre1)

session.add(tvseries1)
session.commit()

tvseries2 = Tvseries(name="Dare Devil", rating="4", user_id=1,
                     description="""
                        The first in a planned series of shows detailing
                        the Marvel universe, Daredevil follows Matt
                        Murdock, attorney by day and vigilante by night.""",
                     genre=genre1)

session.add(tvseries2)
session.commit()

tvseries3 = Tvseries(name="The Last Ship", user_id=1, rating="3",
                     description="""
                        The crew inside the U.S. Navy missile
                        destroyer must find a cure for the global viral.""",
                     genre=genre1)

session.add(tvseries3)
session.commit()

genre2 = Genre(name="Adventure")

session.add(genre2)
session.commit()

tvseries1 = Tvseries(name="Game Of Thrones", user_id=1, rating="5",
                     description="""
                        Several royal families desire the Iron Throne to gain
                        control of Westeros. Whilst kingdoms fight each other
                        for power.""",
                     genre=genre2)

session.add(tvseries1)
session.commit()

tvseries2 = Tvseries(name="Iron Fist", user_id=1, rating="3",
                     description="""
                        When Danny Rand was 10-years old,
                        he survived a mysterious plane crash that claimed the
                        lives of his extremely wealthy parents""",
                     genre=genre2)

session.add(tvseries2)
session.commit()

tvseries3 = Tvseries(name="The Flash", user_id=1, rating="4",
                     description="""
                        Barry Allen, a forensic scientist with the
                        Central City police force, is struck by lightning in a
                        freak accident. When he wakes up after nine months.""",
                     genre=genre2)

session.add(tvseries3)
session.commit()

genre3 = Genre(name="Animation")

session.add(genre3)
session.commit()

tvseries1 = Tvseries(name="Rick And Morty", user_id=1, rating="5",
                     description="""
                        After having been missing for nearly
                        20 years, Rick Sanchez suddenly arrives at daughter
                        Beth'sdoorstep to move in with her and her family.""",
                     genre=genre3)

session.add(tvseries1)
session.commit()

tvseries2 = Tvseries(name="Family Guy", user_id=1, rating="4",
                     description="""
                        Peter Griffin and his family of two teenagers, a smart
                        dog, a devilish baby and his wife find themselves
                        in some of the most hilarious scenarios.""",
                     genre=genre3)

session.add(tvseries2)
session.commit()

tvseries3 = Tvseries(name="The Simpson", user_id=1, rating="4",
                     description="""
                        Homer Simpson and his dysfunctional family come across
                        comical situations in the city of Springfield.""",
                     genre=genre3)

session.add(tvseries3)
session.commit()

genre4 = Genre(name="Comedy")

session.add(genre4)
session.commit()

tvseries1 = Tvseries(name="Suits", user_id=2, rating="4",
                     description="""
                        Suits is set at a fictional law firm in
                        New York City. The focal point of the show follows
                        talented college dropout Mike Ross""",
                     genre=genre4)

session.add(tvseries1)
session.commit()

tvseries2 = Tvseries(name="Friends", user_id=2, rating="5",
                     description="""
                        Take a look at some of the best episodes
                        of 'Friends', the story of six friends
                        living in Manhattan.""",
                     genre=genre4)

session.add(tvseries2)
session.commit()

tvseries3 = Tvseries(name="How I Met Your Mother", user_id=2, rating="4",
                     description="""
                        Ted Mosby, an architect, recounts to his children
                        the events that led him to meet their mother.""",
                     genre=genre4)

session.add(tvseries3)
session.commit()

genre5 = Genre(name="Crime")

session.add(genre5)
session.commit()

tvseries1 = Tvseries(name="Ozark", rating="4", user_id=2,
                     description="""
                        This drama series stars Jason Bateman as Marty Byrde,
                        a financial planner who relocates his family from
                        Chicago to a summer resort community in the Ozarks""",
                     genre=genre5)

session.add(tvseries1)
session.commit()

tvseries2 = Tvseries(name="Ray Donovan", rating="5", user_id=2,
                     description="""
                        Ray Donovan works as a 'fixer' for a law firm that
                        handles celebrities and wealthy clients. While Ray is
                        an expert in solving other people's problems""",
                     genre=genre5)

session.add(tvseries2)
session.commit()

tvseries3 = Tvseries(name="Jessica James", rating="4", user_id=2,
                     description="""
                        This Netflix original chronicles the life of one of
                        the darker Marvel characters, the mysterious
                        Jessica Jones.""",
                     genre=genre5)

session.add(tvseries3)
session.commit()
