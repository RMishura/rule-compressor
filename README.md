# rule-compressor

My program uses the usefulness of individual rules and the similarity between different pairs of rules to compress the set of rules.

**Usefulness** is defined as:

$$
\text{usefulness} = \frac{\big(\text{Number of old individuals for which the rule holds}\big) - \big(\text{Number of young individuals for which the rule holds}\big)}{\sqrt{\big(\text{Number of old individuals for which the rule holds}\big) + \big(\text{Number of young individuals for which the rule holds}\big)}}
$$

**Similarity** is defined as:

$$
\text{similarity} = \frac{\text{Number of individuals for which both rule 1 and rule 2 hold}}{\text{Number of individuals for which at least one of the rules in \{1, 2\} holds}}
$$

The rules are sorted by usefulness and added one by one, from the best to the worst, to the new set of rules until a limit on the size of the new set is reached. This limit can be passed as an argument to the program. If it is not specified, the number of rules will be reduced by a factor of three. Moreover, a rule is not added to the set if it is similar to one of the already selected rules. Two rules \(R1\) and \(R2\) are considered similar if

$$
\text{similarity}(R1, R2) > \text{threshold} = 0.8.
$$
