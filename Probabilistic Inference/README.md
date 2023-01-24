# Bayes Nets and Enumerational Inference

Implementation of Bayes Nets with Inference and Sampling in Python.

## Features
- Implements Bayes Net for probabilistic reasoning
- Provides two inference algorithms (Enumeration Inference and Gibbs Sampling)
- Provides a user-friendly interface for configuring and running the algorithm
- Can handle Bayes Net with different types of nodes (Discrete, Continuous)
- Can handle Bayes Net with different types of edges (Directed, Undirected)
- Can handle Bayes Net with different types of distributions (Discrete, Continuous)
- Can handle Bayes Net with different types of observations (Single, Multiple)
- Can handle Bayes Net with different types of queries (Single, Multiple)
- Can handle Bayes Net with different types of Evidence (Single, Multiple)
- Can handle Bayes Net with different types of Prior Knowledge (Single, Multiple)
- Can handle Bayes Net with different types of Representations (Graphical, Tabular)




## Usage

1. ` DoInference (" ENUMERATION " , " query1 . txt " ,0)` or
    `DoInference (" GIBBS " , " query1 . txt " ,200)`
    
2. `query1.txt` should be in form 

```
[ BayesNetNodes ]
 Burglary
 Earthquake
 Alarm
 JohnCalls
 MaryCalls
 [ Paths ]
 ([ ’ Burglary ’ , ’ Earthquake ’] , ’ Alarm ’)
 ([ ’ Alarm ’] , ’ JohnCalls ’)
 ([ ’ Alarm ’] , ’ MaryCalls ’)
 [ ProbabilityTable ]
 ( ’ Burglary ’ ,[] ,{0.001 ,})
 ( ’ Earthquake ’ ,[] ,{0.002 ,})
 ( ’ JohnCalls ’ ,[ Alarm ] ,{ True : 0.90 , False : 0.05})
 ( ’ MaryCalls ’ ,[ Alarm ] ,{ True : 0.70 , False : 0.01})
 ( ’ Alarm ’ , [ ’ Burglary ’ , ’ Earthquake ’] , {( True , True ) : 0.95 ,( True , False ) : 0.94 ,
( False , True ) : 0.29 , ( False , False ) : 0.001})
 [ Query ]
 ( ’ Burglary ’ , { ’ JohnCalls ’: True , ’ MaryCalls ’: True })

```


## Contributing

1. Fork the repository
2. Create a new branch for your changes (`git checkout -b new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin new-feature`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
