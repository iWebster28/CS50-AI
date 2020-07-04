#testing.py

people = {"Harry", "Lily", "James"}

probabilities = {
        person: {
            "gene": {
                2: 0.3,
                1: 1,
                0: 0.3
            },
            "trait": {
                True: 0.1,
                False: 0.3
            }
        }
        for person in people
    }

def main():
    normalize()
    

def normalize():
    for person in probabilities:
        normalize_helper(probabilities, person, "gene") # Normalize gene probabilities
        normalize_helper(probabilities, person, "trait") # Normalize trait probabilities
    print(probabilities)
    return

def normalize_helper(probabilities, person, field):
    """
    Where field is the field get probabilities from, gene or trait
    """
    sum_prob = 0

    for item in probabilities[person][field]:
        print("value:", probabilities[person][field][item])
        sum_prob += probabilities[person][field][item]
    for item in probabilities[person][field]: #Normalize
        if (sum_prob != 0):
            probabilities[person][field][item] = probabilities[person][field][item]/sum_prob

if __name__ == "__main__":
    main()