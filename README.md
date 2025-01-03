# frankenstatus
 Implementation of Bainbridge's STATUS simulation written for Python

# To Run:
python frankenstatus.py

1. Input number of "guests" to be invited to Frankenstatus' commune (e.g. 46)
2. Read initial distribution of traits and names. 
3. Input desired correlation threshold (e.g. -0.50)
4. Input desired number of attempted swaps (e.g. 20000)
5. Watch as the mad scientist uses the psychexchanger and new correlations are developed.

This program is adapted from the 'STATUS' exercise in SOCIOLOGY LABORATORY written by William Sims Bainbridge and published in 1987. The book consists of twelve exercises designed to teach students about sociological concepts and theories and develop sociological reasoning. Originally, this version of the book shipped with either a 5.25" or 3.5" floppy disk for IBM PC/IBM-compatibles or Apple computers. 

Though the software medium itself would prove difficult to implement in a classroom, I don't believe the exercise itself would be. By updating the program to be written in a contemporary programming language (in this case, Python), sociology teachers can continue to use these exercises in their classroooms and provide a deeper level of engagement (not to mention fun) in their lessons. The original book has certain questions that I adapt below:
 1. **Achieving a Negative Correlation**: Run the simulation with a target correlation of -0.99 in 1000 swaps, you can use any number of guests. Was it successuful? If so, after how many swaps? If not, how close did it get? More advanced students may try to explain the answers.
 2. **Recognizing Positive Correlations**: This activity works best with a partner. Taking turns, one as "guesser" and one as Frankenstatus' RA, follow as such: The RA will set a correlation for some number between 0.00 and 0.90 and run the simulation to get that result. Either removing or otherwise hiding the actual correlation from the compare graph, show the guesser the graph and have them guess what the actual correlation is. Then, reverse roles and repeat. Do this about 10 times, meaning each person gets 5 turns in each role. Keep a record of each guess and actualk correlation, as well as how far off the guesser is for each. The winner is the person who was closer, on average, to the correct correlations.
 3. **Hints of complexity** Start the simulation with 46 guests and aim for a correlation of 0.00 with 300-400 swaps. Observe the start and compare graphs, noting if any one guest has a strong correlation between body and mind. Do the same for a correlation of 0.98 and note if some people seem to be  "outliers". Discuss cases where for individual people, two variables may correlate stronglywhile the correlation for a total population may not be as strong or even be nonexistent.
 
