# CQL basics

To use CQL, go to the corpus search and select the CQL option. CQL will not work anywhere else in the interface. Expert users will use CQL for the writing of Word Sketch grammars and term grammars.

## Syntax

With CQL, complex criteria can be set to find one or many tokens. Criteria for each token must be between a pair of square brackets [ ]. The format is:

    [attribute="value"]

To find the lemma teapot, use

    [lemma="teapot"]

Each token must be inside its own pair of square brackets. To search for phrase refill the teapot, use

    [lemma="refill"][lemma="the"][lemma="teapot"]

## Spaces

Spaces have no function in CQL. Feel free to use spaces to make the code more readable. This code is equivalent to the previous one.


    [ lemma = "refill" ]  [ lemma = "the" ]  [ lemma=  "teapot"  ]

## Careful in values!

There should not be any spaces inside quotes. This finds nothing because a lemma cannot start with spaces.

    [lemma="  the"]

More examples

| TASK | CQL CODE | RESULT |
| -- | -- | -- |
| find examples of “went” | [word="went"] | concordance of the word went
| find examples of all forms of go | [lemma="go"] | concordance of go, goes, going, gone, went
| find exaples of all words tagged with the tag NP | [tag="NP"] | concordance of various words tagged as NP



* Matching on token annotations (properties or attributes), using regular expressions and =, !=, !. Example: [word="bank"] (or just "bank")
* Combining criteria using &, | and !. Parentheses can also be used for grouping. Example: [lemma="bank" & pos="V"]
* Matchall pattern [] matches any token. Example: "a" [] "day"
* Regular expression operators +, *, ?, {n}, {n,m} at the token level. Example: [pos="ADJ"]+
* Sequences of token constraints. Example: [pos="ADJ"] "cow"
* Operators |, & and parentheses can be used to build complex sequence queries. Example: "happy" "dog" | "sad" cat"
* Querying with tag positions using e.g. <s> (start of sentence), </s> (end of sentence), <s/> (whole sentence) or <s> ... </s> (equivalent to <s/> containing ...). Example: <s> "The". XML attribute values may be used as well, e.g. <ne type="PERS"/> (“named entities that are persons”).
* Using within and containing operators to find hits inside another set of hits. Example: "you" "are" within <s/>
* Using an anchor to capture a token position. Example: "big" A:[]. Captured matches can be used in global constraints (see next item) or processed separately later (using the Java interface; capture information is not yet returned by BlackLab Server). Note that BlackLab can actually capture entire groups of tokens as well, similarly to regular expression engines.
* Global constraints on captured tokens, such as requiring them to contain the same word. Example: "big" A:[] "or" "small" B:[] :: A.word = B.word
