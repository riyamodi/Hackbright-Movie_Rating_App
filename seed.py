import model
import csv
print "imported model"

# General Outline:
# 1. open file
# 2. read a line
# 3. parse a line
# 4. create an object
# 5. add the object to a session
# 6. commit
# 7. repeat until done

# id=row[0],age=row[1],gender=row[2],profession=row[3],zipcode=row[4]

def load_users(session):
    # use u.user
    user_list = open("seed_data/u.user")
    user_list_content = csv.reader(user_list, delimiter="|")
    
    users = []

    for row in user_list_content:
        print "before making an object"
        print row
        a = model.User(id=row[0],age=row[1],gender=row[2],occupation=row[3],zipcode=row[4])
        users.append(a)

    # add to session, which is first step in adding to db
    for a in users:
        session.add(a)

    session.commit()

    return "I've added new users."


def load_movies(session):
    # use u.item
    
    movie_list = open("seed_data/u.item")

    movie_list_content = csv.reader(movie_list, delimiter="|")
    print movie_list_content

    movies = []
    counter = 0
    for movie in movie_list_content :

        # if len(row) > 1:
        #     for i in range(1, len(row)-1):
        #         row[0]=row[0]+row[i]

        # print row
        # print row[0].split('|')


        m = model.Movie(id=movie[0],movie_title=movie[1].decode("latin-1"),release_date=movie[2],video_release_date=movie[3],imdb_url=movie[4], unknown=movie[5], action=movie[6],adventure=movie[7],
                         animation=movie[8], childrens=movie[9], comedy=movie[10],crime=movie[11],documentary=movie[12],drama=movie[13],fantasy=movie[14],film_noir=movie[15],
                        horror=movie[16],musical=movie[17],mystery=movie[18],romance=movie[19],sci_fi=movie[20],thriller=movie[21],war=movie[22],western=movie[23])
        movies.append(m)

        counter+=1

    for m in movies:
        session.add(m)

    session.commit()

def load_ratings(session):
    # use u.data
    
    ratings_list = open("seed_data/u.data")
    ratings_list_content = csv.reader(ratings_list,delimiter="\t")

    ratings = []

    for row in ratings_list_content:
        print "Row is:" , row
        d = model.Rating(user_id=row[0],movie_id=row[1],rating=row[2],timestamp=row[3])
        ratings.append(d)

    for d in ratings:
        session.add(d)

    session.commit()

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(s)
    load_movies(s)
    load_ratings(s)


if __name__ == "__main__":
    s= model.connect()
    main(s)
