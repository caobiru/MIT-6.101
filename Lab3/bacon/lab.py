"""
6.101 Lab 3:
Bacon Number
"""

#!/usr/bin/env python3

import pickle

# NO ADDITIONAL IMPORTS ALLOWED!


def transform_data(raw_data):
    """
    This fucntion changes the orginal datastructure to a hashmap.
    It is a dictionary which the key is one actor's id, and the value
    is a set of actors' ids whom the actor worked with.
    """
    neighbors = {}
    for items in raw_data:
        actor_1 = items[0]
        actor_2 = items[1]
        
        if actor_1 not in neighbors:
            neighbors.update({actor_1: {actor_2}})
        else:
            neighbors[actor_1].add(actor_2)
        if actor_2 not in neighbors:
            neighbors.update({actor_2: {actor_1}})
        else:
            neighbors[actor_2].add(actor_1)

    # ignore the films in which the actor pairs with themselves
    for actor in neighbors.keys():
        neighbors[actor].discard(actor)
    
    return neighbors


def acted_together(transformed_data, actor_id_1, actor_id_2):
    """
    This fucntion checks whether two actors worked together 
    """
    if actor_id_1 == actor_id_2:
        return True 
    elif transformed_data.get(actor_id_1) is not None and actor_id_2 in transformed_data.get(actor_id_1):
        return True
    elif transformed_data.get(actor_id_2) is not None and actor_id_1 in transformed_data.get(actor_id_2):
        return True
    else:
        return False

# -----------------------------------------------------------------------------------
# def actors_with_bacon_number(transformed_data, n):
#     actors_set = {4724}
#     old_actors_set = v set()  
#     for i in range(n):
#         print(i)
#         old_actors_set.update(actors_set)
#         actors_set = actors_bacon_number_plusone(transformed_data, actors_set) - old_actors_set
#     return actors_set
     
    
# # getting the Bacon number i+1 actors from the Bacon number i actors.    
# def actors_bacon_number_plusone(transformed_data, actors_set):
#     bacon_1_set = set()
#     for actor in actors_set:
#         bacon_1_set.update(transformed_data.get(actor, set()))
#     return bacon_1_set
# -----------------------------------------------------------------------------------


def actors_with_bacon_number(transformed_data, n):
    """
    This fucntion returns all the actor ids who have a bacon number n
    """
    # Initialize a queue with Kevin Bacon's ID and his Bacon number
    queue = [(4724, 0)]
    # Initialize a set to keep track of visited actors
    visited = set()
    # Initialize a set to store actors with Bacon number n
    actors_with_bacon_n = set()
    
    while queue:
        #  Deque and actor and his bacon number from the queue 
        actor, bacon_number = queue.pop(0)
        
        if bacon_number > n:
            break

        if actor not in visited:
            # Mark the actor as visited
            visited.add(actor)
                        
            if bacon_number == n:
                actors_with_bacon_n.add(actor)
            
            #Enqueue all the actor's neighbors
            for neighbor in transformed_data.get(actor, []):
                queue.append((neighbor, bacon_number + 1))
                
    return actors_with_bacon_n


def bacon_path(transformed_data, actor_id):
    """
    This fucntion returns the path from Kevin Bacon to any actor
    """
    # Agenda: path we know about but haven't tried to extend
    possible_path = [[4724]]
    
    # Initialize a set to keep track of visited actors
    visited = set()
        
    while possible_path:
        #  Deque and actor and his bacon number from the queue 
        this_path = possible_path.pop(0)
        
        end_actor = this_path[-1]
        
        #Enqueue all the actor's neighbors
        for neighbor in transformed_data.get(end_actor, []):
            if neighbor in visited:
                pass
            else:
                if neighbor == actor_id:
                    this_path.append(neighbor)
                    return this_path
                else:
                    visited.add(neighbor)
                    new_path = list(this_path)
                    new_path.append(neighbor)
                    possible_path.append(new_path)


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    """
    This fucntion returns the shortest path from actor1 to actor 2
    """
    # if id1 equals to id2
    if actor_id_1 == actor_id_2:
        return [actor_id_1]
    
    # Agenda: path we know about but haven't tried to extend
    possible_path = [[actor_id_1]]
    
    # Initialize a set to keep track of visited actors
    visited = set()
        
    while possible_path:
        #  Deque and actor and his bacon number from the queue 
        this_path = possible_path.pop(0)
        
        end_actor = this_path[-1]
        
        #Enqueue all the actor's neighbors
        for neighbor in transformed_data.get(end_actor, []):
            if neighbor in visited:
                pass
            else:
                if neighbor == actor_id_2:
                    this_path.append(neighbor)
                    return this_path
                else:
                    visited.add(neighbor)
                    new_path = list(this_path)
                    new_path.append(neighbor)
                    possible_path.append(new_path)

    return None


def get_movie(raw_data, actor_id_1, actor_id_2):
    """
    This fucntion gives a movie ids in which actor1 and actor 2 worked together
    """
    for items in raw_data:
        if actor_id_1 in items and actor_id_2 in items:
            return items[2]
 

def actor_path(transformed_data, actor_id_1, goal_test_function):
    """
    the shortest possible path from the given actor ID to any actor that satisfies 
    the goal-test function. 
    """
    if goal_test_function(actor_id_1):
        return [actor_id_1]

    else:       
        paths = []         
        for actor_id_2 in transformed_data:
            if goal_test_function(actor_id_2):
                path = actor_to_actor_path(transformed_data, actor_id_1, actor_id_2)
                if path is not None:
                    paths.append(path)
                    
        # Return the shortest path, if any
        if paths:
            return min(paths, key=len)

    return None


def actors_connecting_films(transformed_data, film1, film2):
    """
    find chains of actors that connect one given movie to another
    """
    pass


if __name__ == "__main__":
    with open("resources/small.pickle", "rb") as f:
        smalldb = pickle.load(f)

    with open("resources/names.pickle", "rb") as g:
        namedb = pickle.load(g)
    
  
    
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    
    
        # 2.2) The Names Database Test
    # print(smalldb.get("Fernando Rubio"))
    # for key, value in smalldb.items():
    #     if value == 1100321:
    #         print(key)
    

        # 4) Acting Together test
    # Check if Chris Hogan and Dean Paraskevopoulos acted together in the small.pickle database
    # actor_1 = namedb.get("Chris Hogan")
    # actor_2 = namedb.get("Dean Paraskevopoulos")
    # actor_dict = transform_data(smalldb)
    # print(acted_together(actor_dict, actor_1, actor_2))       
    # Check if Folke Lind and Jean Schmitt acted together in the small.pickle database            
    # actor_1 = namedb.get("Folke Lind")
    # actor_2 = namedb.get("Jean Schmitt")
    # actor_dict = transform_data(smalldb)
    # print(acted_together(actor_dict, actor_1, actor_2))            
            
            
        # 5) Bacon Number test           
    # In the large.pickle database, what is the set of actors with Bacon number 6?      
    # actor_dict = transform_data(smalldb)
    # print(actors_with_bacon_number(actor_dict, 6)) 
    
             
        # 6.1.1)  Speed           
    # In the large.pickle database, check what is the path of actors from Kevin Bacon to Carmen Maura     
    # actor_dict = transform_data(smalldb)
    # path = (bacon_path(actor_dict, namedb.get("Carmen Maura"))) 
    # for id in path:
    #     for key, value in namedb.items():
    #         if value == id:
    #             print(key)   
    
    
        # 6.2) Arbitrary Paths
    # In the large.pickle database, check the minimal path of actors from George Hunter to Maggie Q?
    
    # with open("resources/large.pickle", "rb") as f:
    #     largedb = pickle.load(f)
        
    # with open("resources/names.pickle", "rb") as g:
    #     namedb = pickle.load(g)
    
    # actor_1 = namedb.get("George Hunter")
    # actor_2 = namedb.get("Maggie Q")
    # actor_dict = transform_data(largedb)
    # path = actor_to_actor_path(transform_data(largedb), actor_1, actor_2)
    
    # for id in path:
    #     for key, value in namedb.items():
    #         if value == id:
    #             print(key)  
          
                
        #7) Movie Paths
    # In the large.pickle database,, check the minimal path of movie titles connecting Adrienne King to Anton Radacic
    # with open("resources/large.pickle", "rb") as f:
    #     largedb = pickle.load(f)    
    # with open("resources/names.pickle", "rb") as g:
    #     namedb = pickle.load(g)
    # with open("resources/movies.pickle", "rb") as h:
    #     moviedb = pickle.load(h)
        
    # actor_1 = namedb.get("Adrienne King")
    # actor_2 = namedb.get("Anton Radacic")
    # actor_dict = transform_data(largedb)
    # path = actor_to_actor_path(transform_data(largedb), actor_1, actor_2)
    
    # movie_path = []
    # for i in range(len(path) - 1):
    #     movie_path.append(get_movie(largedb, path[i], path[i + 1]))
    
    # movie_path_name = []
    # for movie_id in movie_path:
    #         for key, value in moviedb.items():
    #             if value == movie_id:
    #                 movie_path_name.append(key)        
    
    # print(movie_path_name)