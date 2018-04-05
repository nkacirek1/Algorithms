import json
import sys
from Gale_Shapley.helpers import generate_problems


def read_json(filename):
    with open(filename) as f:
        return json.load(f)


def write_json(obj, filename):
    with open(filename, mode='w') as f:
        json.dump(obj, f)


def GS(preferences):
    pairs = {}
    # two dictionaries that contain the preferences for each of the groups
    # Example:
    # {'a0': ['b0', 'b1'], 'a1': ['b1', 'b0']}
    # {'b0': ['a0', 'a1'], 'b1': ['a1', 'a0']}

    group1Dict = preferences[0]
    group2Dict = preferences[1]

    group1 = list(group1Dict.keys())

    # initally all men and women are free
    # while there is a man m who is free and hasn't proposed to every women:
    while len(group1) is not 0:
        # choose such a man m
        man = group1[0]
        # let w be the highest ranked woman in m's preference list to whom m has not yet proposed to
        manPref = group1Dict[man]
        w = manPref[0]
        if w in pairs:
            # w is currently engaged to other man o
            o = pairs[w]
            # if w prefers o to m:
                # need to look at who has the smaller index in her preference list
            manHigher = False
            oHigher = False
            womanPref = group2Dict[w]
            for i in range (0, len(group2Dict)):
                if womanPref[i] == man:
                    manHigher = True
                    break
                if womanPref[i] == o:
                    oHigher = True
                    break
            if oHigher is True:
                # then m remains free
                # need to remove her from her preference
                group1Dict[man].remove(w);
                continue
            elif manHigher is True:
                # else w prefers m to o
                # (m, w) become engaged
                pairs[w] = man
                group1.remove(man)
                # o becomes free
                group1.append(o)
        else:
            # if w is free, then (m, w) become engaged
            #add the couple to the pairs dictionary
            pairs[w] = man
            #remove the man from the group of suitors
            group1.remove(man)

    # return the set S of engaged pairs
    return pairs


if __name__ == "__main__":
    # first argument sys.argv[1] is the name of a json text
        # file containing a list of stable matching problem specifications
    # JSON file is a list of pairs of dictionaries that represent matching problems
        # two dictionaries containing the preferences of the proposers and the acceptors
    # the people in the first dictionary must do the asking during the algorithm
    # preferences as given as most to least preferred

    # second argument sys.argv[2] is the name of the JSON file to write the output to
    # file should be a list of dictionaries of matchings corresponding to the Gale Shapley
    # matching for each problem
    # Ex: Array with an object for each final matching
    # [{"a0": "b0", "a1": "b1"},
    #        {"j0": "k1", "j1": "k0"}]

    # read in JSON file
    inputList = read_json(sys.argv[1]);

    #implement the Gale Shapely
    forOutput = []
    for x in range (0, len(inputList)):
        finalPairs = GS(inputList[x])
        finalPairs = generate_problems.helpers.inverse_dict(finalPairs)
        forOutput.append(finalPairs)

    write_json(forOutput, sys.argv[2])

