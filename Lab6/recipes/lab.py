"""
6.101 Lab 6:
Recipes
"""

import pickle
import sys

sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!


def make_recipe_book(recipes):
    """
    Given recipes, a list containing compound and atomic food items, make and
    return a dictionary that maps each compound food item name to a list
    of all the ingredient lists associated with that name.
    """
    recipe_book = {}
    for item in recipes:
        if item[0] == "compound":
            if item[1] not in recipe_book:
                recipe_book[item[1]] = [item[2]]
            else:
                recipe_book[item[1]].append(item[2])
    return recipe_book

def make_atomic_costs(recipes):
    """
    Given a recipes list, make and return a dictionary mapping each atomic food item
    name to its cost.
    """
    atomic_cost = {}
    for item in recipes:
        if item[0] == "atomic":
            atomic_cost[item[1]] = item[2]
    return atomic_cost

def lowest_cost(recipes, food_item, excluded_items = None):
    """
    Given a recipes list and the name of a food item, return the lowest cost of
    a full recipe for the given food item.
    """
    if excluded_items is None:
        excluded_items = []
    recipe_book = make_recipe_book(recipes)
    atomic_costs = make_atomic_costs(recipes)

    # if the food_item is an atomic already, return its single cost
    if food_item in atomic_costs and food_item not in excluded_items:
        return atomic_costs[food_item]
    # if the food_item is not a compund or it belongs to excluded_items
    elif food_item not in recipe_book or food_item in excluded_items:
        return None

    # recursive function calculates the cost of one recipe list
    # such as {'burger', [('bread', 2), ('cheese', 1), ('lettuce', 1), ('protein', 1)]}
    def ingredient_list_cost(ingredient_list):
        total_cost = 0
        for ingredient, quantity in ingredient_list:
            # if an ingredient not in the database,or should be excluded, return None
            if ingredient not in atomic_costs and ingredient not in recipe_book or ingredient in excluded_items:
                return None
            # if an ingredient is an atomic, it multiplies its cost by its quantity.
            elif ingredient in atomic_costs:
                total_cost += atomic_costs[ingredient] * quantity
            # if an ingredient is a compound, it recursively calculates the minimum cost of all its recipes.
            else:
                # the cost of all the recipe of making the ingredient's sub component
                ingredient_costs = [ingredient_list_cost(recipe) for recipe in recipe_book[ingredient]]
                # If any recipe for a compound ingredient cannot be made, return None
                if all(cost is None for cost in ingredient_costs):
                    return None
                total_cost += min(cost for cost in ingredient_costs if cost is not None) * quantity
        return total_cost

    costs = [ingredient_list_cost(recipe) for recipe in recipe_book[food_item]]
    # If all recipes for the food item cannot be made, return None
    if all(cost is None for cost in costs):
        return None

    # Otherwise, return the minimum cost among the recipes that can be made
    return min(cost for cost in costs if cost is not None)

def scale_recipe(flat_recipe, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
    scaled_recipe = {}
    flat_recipe_dict = dict(flat_recipe)
    for item, quantity in flat_recipe_dict.items():
        scaled_recipe[item] = n * quantity
    return scaled_recipe

def make_grocery_list(flat_recipes):
    """
    Given a list of flat_recipe dictionaries that map food items to quantities,
    return a new overall 'grocery list' dictionary that maps each ingredient name
    to the sum of its quantities across the given flat recipes.

    For example,
        make_grocery_list([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}])
    should return:
        {'milk':3, 'chocolate': 1, 'sugar': 1}
    """
    grocery_list = {}
    for flat_recipe in flat_recipes:
        for item, quantity in flat_recipe.items():
            if item not in grocery_list:
                grocery_list[item] = quantity
            else:
                grocery_list[item] += quantity
    return grocery_list


def cheapest_flat_recipe(recipes, food_item, excluded_items = None):
    """
    Given a recipes list and the name of a food item, return a dictionary
    (mapping atomic food items to quantities) representing the cheapest full
    recipe for the given food item.

    Returns None if there is no possible recipe.
    """
    if excluded_items is None:
        excluded_items = []
    recipe_book = make_recipe_book(recipes)
    atomic_costs = make_atomic_costs(recipes)

    # returns a tuple of the minimum cost and the corresponding flat recipe
    def cost_flat_recipe(food_item):
        # if the food_item is an atomic already
        if food_item in atomic_costs and food_item not in excluded_items:
            return atomic_costs[food_item], {food_item: 1}
        # if the food_item is not a compund or it belongs to excluded_items
        elif food_item not in recipe_book or food_item in excluded_items:
            return float("inf"), {}
        # if the food_item is a compund
        min_cost = float("inf")
        min_recipe = {}
        for recipe in recipe_book[food_item]:
            total_cost = 0
            total_recipe = {}
            for ingredient, quantity in recipe:
                # the cost and flat recipe for making one ingredient
                cost, flat_recipe = cost_flat_recipe(ingredient)
                # the ingredient can't be made
                if cost == float("inf"):
                    break
                # update the total cost
                total_cost += cost * quantity
                scaled_recipe = scale_recipe(flat_recipe, quantity)
                total_recipe = make_grocery_list([scaled_recipe, total_recipe])
            # check if this recipe is the cheapest
            else:
                if total_cost < min_cost:
                    min_cost = total_cost
                    min_recipe = total_recipe
        return min_cost, min_recipe

    cost, flat_recipe = cost_flat_recipe(food_item)
    return flat_recipe if cost != float("inf") else None

def ingredient_mixes(flat_recipes):
    """
    Given a list of lists of dictionaries, where each inner list represents all
    the flat recipes for a certain ingredient, compute and return a list of flat
    recipe dictionaries that represent all the possible combinations of 
    ingredient recipes.
    """
    ingredient_mix = [{}]
    for recipe in flat_recipes:
        new_mix = []
        for recipe1 in ingredient_mix:
            # for one possibility
            for recipe2 in recipe:
                combined_recipe = dict(recipe1)
                for ingredient, quantity in recipe2.items():
                    if ingredient in combined_recipe:
                        combined_recipe[ingredient] += quantity
                    else:
                        combined_recipe[ingredient] = quantity
                # Add the combined recipe to the new result list
                new_mix.append(combined_recipe)
        ingredient_mix = new_mix
    return ingredient_mix

def all_flat_recipes(recipes, food_item, excluded_items = None):
    """
    Given a list of recipes and the name of a food item, produce a list (in any
    order) of all possible flat recipes for that category.

    Returns an empty list if there are no possible recipes
    """
    if excluded_items is None:
        excluded_items = []

    recipe_book = make_recipe_book(recipes)
    atomic_costs = make_atomic_costs(recipes)

    def helper(food_item):
        # Base case: if the food item is atomic and not excluded
        if food_item in atomic_costs and food_item not in excluded_items:
            return [{food_item: 1}]

        # Base case: if the food item is not in the recipe book or is excluded
        elif food_item not in recipe_book or food_item in excluded_items:
            return []

        # Recursive case: if the food item is compound
        else:
            # Initialize the result list
            result = []

            # Iterate over each recipe for the food item
            for recipe in recipe_book[food_item]:
                flat_recipes_for_current_recipe = [{}]

                for ingredient, quantity in recipe:
                    # get all flat recipes for the ingredient
                    flat_recipes_for_ingredient = helper(ingredient)

                    # scale each flat recipe by the quantity
                    scaled_flat_recipes_for_ingredient = [scale_recipe(flat_recipe, quantity) for flat_recipe in flat_recipes_for_ingredient]

                    # get all possible combinations of flat recipes
                    flat_recipes_for_current_recipe = ingredient_mixes([flat_recipes_for_current_recipe, scaled_flat_recipes_for_ingredient])

                # add the flat recipes for the current recipe to the result list
                result.extend(flat_recipes_for_current_recipe)

            return result

    return helper(food_item)


if __name__ == "__main__":
    # load example recipes from section 3 of the write-up
    with open("test_recipes/example_recipes.pickle", "rb") as f:
        example_recipes = pickle.load(f)
    # you are free to add additional testing code here!
    #
    # Test 4
    # what is the total cost of buying 1 of every atomic food item?
    # atomic_costs = make_atomic_costs(example_recipes)
    # total_cost = sum(atomic_costs.values())
    # print(total_cost)
    # # how many compound food items can be made multiple ways?
    # recipe_book = make_recipe_book(example_recipes)
    # count = 0
    # for ingredients in recipe_book.values():
    #     if len(ingredients) > 1:
    #         count += 1
    #         print(ingredients)
    # print(count)
    #
    # Test falt_recipes
    # flat_recipes = [
    #     [{"cake": 1}, {"gluten free cake": 1}],
    #     [{"vanilla icing": 1}, {"cream cheese icing": 1}],
    #     [{"sprinkles": 20}]
    # ]
    # print(ingredient_mixes(flat_recipes))
    