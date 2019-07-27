from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from models import Category, Base, CategoryItem
 
engine = create_engine('sqlite:///Catalog.db')
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


#Items for Snowboarding
category1 = Category(name = "Snowboarding")
session.add(category1)
session.commit()


menuItem1 = CategoryItem(title = "Goggles", description = "Ski goggles are an important piece of kit. They protect your eyes from the elements, such as snow, wind, and harmful UV rays, while improving your vision so that you get to see the mountain as well as possible. The functions and features that goggles can have are often overlooked, with a lot of people just buying the cheapest pair they can find. Yet the difference between a cheap pair of goggles and a good pair, can be vast, and can make a huge difference to how well they work, and how comfortable they are.", category = category1)
session.add(menuItem1)
session.commit()

menuItem2 = CategoryItem(title = "Snowboard", 
description = "Best for any terrain conditions. All-mountain snowboards perform anywhere on a mountain-groomed runs, backcountry, even park and pipe. They may be directional (meaning downhill only) or twin-tip (for riding switch, meaning either direction). Most boarders ride all-mountain boards. Because of their versatility, all-mountain boards are good for beginners who are still learning what terrain they like.", category = category1)
session.add(menuItem2)
session.commit()



#Items for Soccer
category2 = Category(name = "Soccer")
session.add(category1)
session.commit()


menuItem1 = CategoryItem(title = "Shin Guards", description = "A shin guard is a thick piece of material that you wear inside your socks to protect the lower part of your leg when you are playing a game such as soccer. Shin guards are likely the most important piece of equipment a soccer player will buy. Why? Because EVERYONE on the field — no matter the level of play — must wear them.", category = category2)
session.add(menuItem1)
session.commit()

menuItem2 = CategoryItem(title = "Soccer Ball", description = "The soccer ball is the only essential piece of equipment in the game of soccer. The ball's spherical shape, as well as its size, weight, and material composition, are specified by Law 2 of the Laws of the Game maintained by the International Football Association Board. Additional, more stringent, standards are specified by FIFA and subordinate governing bodies for the balls used in the competitions they sanction.", category = category2)
session.add(menuItem2)
session.commit()

# Items for BasketBall
category3 = Category(name = "BasketBall")
session.add(category1)
session.commit()


menuItem1 = CategoryItem(title = "Basketball shoes", description = "Basketball shoes are specifically designed for the intensity of the game. Sports scientists at the University of Utah point out that on average, basketball players switch direction every two seconds and run 105 short sprints every game. With constant jumping, starting and stopping, basketball shoes are designed to act as shock absorbers and provide ankle stability with the flexibility to allow players to move laterally. As such, basketball shoes are much bulkier than running shoes.", category = category3)
session.add(menuItem1)
session.commit()

# Other Categories
category4 = Category(name = "BaseBall")
session.add(category4)
session.commit()

category5 = Category(name = "Frisbee")
session.add(category5)
session.commit()


category6 = Category(name = "Rock Climbing")
session.add(category6)
session.commit()

category7 = Category(name = "FoosBall")
session.add(category7)
session.commit()


category8 = Category(name = "Skating")
session.add(category8)
session.commit()

category9 = Category(name = "Hockey")
session.add(category9)
session.commit()

category10 = Category(name = "Swimming")
session.add(category10)
session.commit()

category11 = Category(name = "Diving")
session.add(category11)
session.commit()

category12 = Category(name = "Other")
session.add(category12)
session.commit()


print ("Data Added")