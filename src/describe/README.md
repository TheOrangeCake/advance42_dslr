# Describe

Contain part 0: Setup and part1: Data Analysis



## std

std is standard deviation (écart type in frence)

$$
\sigma = \sqrt{\frac{\sum_{i=1}^{n}(x_i-\mu)^2}{n - 1}}
$$

- $\sigma$ = standard deviation
- $\mu$ = mean of the dataset (cal_mean)
- $x_i$ = the $i$-th value in the dataset
- $n$ = number of values (cal_count)

**Population:** You have the complete dataset and only care about describing it exactly. Use n for the denominator.

**Sample**: You have a subset and want to generalize your findings to a larger population. Use n-1 for the denominator.

https://fr.khanacademy.org/math/agroalimentaire-4e-annee-maths/x3a983cebc5b97c17:statistique-a-une-variable/x3a983cebc5b97c17:parametres-de-dispersion/a/calculating-standard-deviation-step-by-step