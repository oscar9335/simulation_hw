
import math
import numpy as np
import matplotlib.pyplot as plt
import random

# [IQ, wealth ,luck]

def create_population_birth( population:int ) -> dict[str]:

# it is a 3 * population list row: IQ, row2: wealth, row3: luck.
    people = []

# IQ value set
    # this is the statisic from Internet
    mean_iq = 100  # Mean IQ
    std_dev_iq = 15  # Standard deviation of IQ
    # Generate a sample of IQ scores from a normal distribution
    iq_scores = np.random.normal(mean_iq, std_dev_iq, population)
    iq_scores_int = [int(x) for x in iq_scores]
    people.append(iq_scores_int)

# wealth value set
    # Set the parameters for the Pareto distribution
    alpha = 2  # Shape parameter, determines the tail heaviness
    xmin = 1    # Minimum value, also called the scale parameter
    wealth_distribution = np.random.pareto(alpha, population) + xmin

    min_wealth_dollars = 1
    max_wealth_dollars = 1000000

    # Map the simulated wealth values to US dollars
    wealth_distribution_dollars = (
        wealth_distribution / np.max(wealth_distribution) *
        (max_wealth_dollars - min_wealth_dollars) + min_wealth_dollars
    )
    wealth_distribution_dollars_list = wealth_distribution_dollars.tolist()
    people.append(wealth_distribution_dollars_list)

# luck value set
    # this is the statisic from Internet
    mean_luck = 50  # Mean IQ
    std_dev_luck = 10  # Standard deviation of IQ
    # Generate a sample of IQ scores from a normal distribution
    luck_scores = np.random.normal(mean_luck, std_dev_luck, population)
    luck_scores_int = [int(x) for x in luck_scores]
    people.append(luck_scores_int)


# reshape the list
    # Convert the list to a numpy array
    people_array = np.array(people)

    # Reshape the array to a  array
    reshaped_people = people_array.transpose()
    reshaped_people_list = reshaped_people.tolist()

    return reshaped_people_list

# simulate one person: who
def event_set(people : list ,who:int) : # change the people array value
    # S: 0.1% :earn lots of money, wealth * 3 + 10000
    # A: 24.8% : earn money, wealth * 1.5 
    # B: 50%: no change *1
    # D: 24.8% : lose money / 1.5
    # F: 0.1% : lose lots money / 3 - 10000, if minus then 0

    # If the event coour probabilty < 0 then 0

    # first check wealth, every 5000 is a level
    # this value will influent the poisson process of event coming rate
    # wealth will change by the time
    wealth_level = math.ceil(people[who][1] / 5000) + 1

    # Iq influent the probabilty of event occur
    # ex: IQ = 160 then iq_influence = 60*0.1 = 6 , make A 24.8% + 6%  D: 24.8% - 6% to occur
    iq_influence = (people[who][0] - 100) * 0.1 * 0.01

    # Luck influent the event level 
    # ex: Lucky 70, (70-50) / 10 = 2, make A 24.8% + 2*2%  D: 24.8% - 2*2% to occur and make S 0.1% + 2 * 0.5 % make F 0.1% - 2 * 0.5 %
    lucky_incluence = (people[who][2] - 50) * 0.1

    # record the wealth changes and event [wealth],[event]
    whose_wealth = []
    whose_wealth.append(people[who][1])
    whose_event = []

    # give the parameter to indluent the event
    # Given list and probabilities
    values = ["S", "A", "B", "D", "F"]
    probabilities = [0.001, 0.248, 0.5, 0.248, 0.001]
    error_detect = 0.001 - lucky_incluence * 0.01
    F_occur = error_detect
    adaption = 0
    if(error_detect < 0):
        adaption = error_detect * -1
        F_occur = 0

    probabilities_who = [0.001 + lucky_incluence * 0.005, 
                         0.248 + iq_influence + lucky_incluence*0.01,
                         0.5 + adaption,
                         0.248 - iq_influence - lucky_incluence*0.01,
                         F_occur]

    # using poisson as evet occur
    # assume all people live 80 years and the live start to change from 20 years old
    t = 0
    while(t < 60):
        this_time = -np.log(random.uniform(0,1)) / math.log(wealth_level,2)
        t += this_time
        # an event occur
        random_event = random.choices(values, weights = probabilities_who, k=1)[0]
        if(random_event == "S"):
            people[who][1] = people[who][1] * 5 + 10000
        elif(random_event == "A"):
            people[who][1] = people[who][1] * 2 + 500
        elif(random_event == "B"):
            people[who][1] = people[who][1] * 1 
        elif(random_event == "D"):
            people[who][1] = people[who][1] / 2
        elif(random_event == "F"):
            people[who][1] = people[who][1] / 5
        else:
            print("error") 

        whose_wealth.append(people[who][1])
        whose_event.append(random_event)

    return whose_wealth, whose_event

def plot_distribution(people: list, column:int):
    # Plot the distribution of values in column 2
    # Extract column 2 values
    column_2_values = [row[column] for row in people]
    plt.hist(column_2_values, bins = 25, density=True)
    plt.title('Distribution of Column 2 Values')
    plt.xlabel('Column 2 Values')
    plt.ylabel('Probability Density')
    plt.show()


def main():
    people = create_population_birth(10000)
    sorted_data = sorted(people, key=lambda x: x[1])
    # for i in sorted_data:
    #     print(i[2])
    # plot_distribution(people,2)
    print(sorted_data[9000])
    w,e = event_set(sorted_data,9000)
    print(w)
    print(e)

main()