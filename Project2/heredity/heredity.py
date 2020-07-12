import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene (EX: PROBS["trait"][2])
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    # Diag
    # print("probabilities:", probabilities)
    # print("people", people)
    # print("names", names)
    # print("powerset of name", powerset(names))

    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and #None means we don't know if they have the trait
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # print("joint_probability:")
    # print("people:", people)
    # print("one_gene", one_gene) 
    # print("two_genes", two_genes)
    # print("have_trait", have_trait)
    # print("--------------")

    # Assume either we know mother and father, or none
    # If no parents, use PROBS["gene"] to determine proba they 
    #have a certain num of the gene

    # For anyone with parents, each parent passes random gene 
    #to child with proba PROBS["mutation"] that is mutates.
 
    p = 1 # where p is entire joint probability
    person_genes = 0 # per person

    # print("---------------------")
    # print(f"people, {one_gene}, {two_genes}, {have_trait}")

    for person in people:  
        # Get num genes
        person_genes = num_genes(person, one_gene, two_genes)
        
        # Calc joint probabilities

        # Get parent names
        mom = people[person]["mother"]
        dad = people[person]["father"]
        
        # If no parents. 
        if (mom == None and dad == None):
            gene_prob = PROBS["gene"][person_genes]
        
        # If parents:
        else:
            # How many genes do parents have?
            mom_genes = num_genes(mom, one_gene, two_genes)
            dad_genes = num_genes(dad, one_gene, two_genes)

            # Probabilities from each parent

            #Note: If parents has:
            #1 copy: 0.5 prob pass to child (not 0.5 - 0.01)
            #2 copies: passes 1 to child, 0.01 mutation (1 - 0.01)
            #0 copies: not passed on, 0.01 mutation (0.01)
            #Formula: abs(num_genes/2 - (PROBS["mutation"] if mom doesn't have 1 gene/dad doesn't have 1 gene))

            from_mom = abs(mom_genes/2 - (PROBS["mutation"] if mom_genes != 1 else 0))
            not_from_mom = abs(1 - from_mom)

            from_dad = abs(dad_genes/2 - (PROBS["mutation"] if dad_genes != 1 else 0))
            not_from_dad = abs(1 - from_dad)

            # Did mother and/or father give genes?
            if (person_genes == 1): #Only 1 parent contributes
                gene_prob = (not_from_mom * from_dad) + (not_from_dad * from_mom)
            elif (person_genes == 2): #2 parents contribute
                gene_prob = from_mom * from_dad
            else: #0 genes
                gene_prob = not_from_mom * not_from_dad

        # Check if has trait (for later)
        has_trait = True if (person in have_trait) else False

        # Get probability of person having trait
        trait_prob = PROBS["trait"][person_genes][has_trait]

        # Get total joint probability for this person
        new_joint_prob = gene_prob * trait_prob

        # print(f"{person}: new_join_prob = {new_joint_prob}")

        # Multiply by existing joint probability
        p *= new_joint_prob

    return p


def num_genes(person, one_gene, two_genes):
    """
    Returns how many genes someone has, depending on the set they're in/not in.
    """
    return 1 if (person in one_gene) else (2 if (person in two_genes) else (0))


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    # print("p:", p)

    # Each person should have their "gene" and "trait" distributions updated.
    for person in probabilities:
        # Update gene probability
        person_genes = num_genes(person, one_gene, two_genes)
        probabilities[person]["gene"][person_genes] += p

        # Update trait probability
        has_trait = True if (person in have_trait) else False
        probabilities[person]["trait"][has_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        normalize_helper(probabilities, person, "gene") # Normalize gene probabilities
        normalize_helper(probabilities, person, "trait") # Normalize trait probabilities
    # print(probabilities)


def normalize_helper(probabilities, person, field):
    """
    Where field is the field to get probabilities from, gene or trait
    """

    # Sum all values to get denominator for normalizing later.
    sum_prob = sum(probabilities[person][field].values())

    for value in probabilities[person][field]: #Normalize
        if (sum_prob != 0): #Check for division by 0
            probabilities[person][field][value] = probabilities[person][field][value]/sum_prob
        else:
            print("Division by 0: Probabilities summed to 0.")
   

if __name__ == "__main__":
    main()
